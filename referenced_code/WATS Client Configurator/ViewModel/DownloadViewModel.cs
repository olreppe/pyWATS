using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Windows.Media;
using Virinco.WATS.Interface;
using Virinco.WATS.Interface.MES;
using System.ComponentModel;
using System.Net;
using System.IO;
using System.Diagnostics;
using System.Net.Http;
using System.Threading.Tasks;
using System.Threading;
using System.Net.Http.Headers;

namespace Virinco.WATS.Client.Configurator.ViewModel
{
    public class DownloadViewModel : Helpers.ObservableObject
    {
        #region Properties       

        public double Progress { get; private set; } = 0;

        public string ProgressText
        {
            get { return $"{FormatReadableBytes(TotalRead)} / {FormatReadableBytes(TotalBytes)}"; }
        }

        public long TotalBytes
        {
            get { return totalBytes; }
            set 
            { 
                if (totalBytes != value) 
                { 
                    totalBytes = value; 
                    Progress = ((double)TotalRead) / value; 
                    RaisePropertyChanged(nameof(TotalBytes)); 
                    RaisePropertyChanged(nameof(Progress)); 
                    RaisePropertyChanged(nameof(ProgressText)); 
                } 
            }
        }

        public long TotalRead
        {
            get { return totalRead; }
            set 
            { 
                if (totalRead != value) 
                { 
                    totalRead = value; 
                    Progress = ((double)value) / TotalBytes; 
                    RaisePropertyChanged(nameof(TotalRead));
                    RaisePropertyChanged(nameof(Progress));
                    RaisePropertyChanged(nameof(ProgressText));
                }
            }
        }

        public bool Cancelled { get; private set; }

        #region Property fields

        private long totalBytes;

        private long totalRead;

        #endregion

        #endregion

        private readonly HttpClient client;

        private CancellationTokenSource cancellationTokenSource;

        #region Constants

        private readonly string downloadDirectoryPath = Path.Combine(Env.DataDir, "Download");

        private readonly string[] byteSizeNames = { "B", "KB", "MB", "GB" };

        private const int bufferSize = 65536;

        #endregion

        public DownloadViewModel()
        {
            client = new HttpClient
            {
                Timeout = Timeout.InfiniteTimeSpan
            };

            if (!Directory.Exists(downloadDirectoryPath))
                Directory.CreateDirectory(downloadDirectoryPath);
        }

        public async Task<FileInfo> DownloadAsync(Uri uri)
        {          
            Cancelled = false;
            cancellationTokenSource = new CancellationTokenSource(ViewModel.ViewModelLocator.TDMAPIStatic.DownloadClientUpdateTimeout);

            string filePath = Path.Combine(downloadDirectoryPath, uri.AbsolutePath.Split('/').LastOrDefault());

            try
            {               
                using (var request = new HttpRequestMessage(HttpMethod.Get, uri))
                {
                    request.Headers.Authorization = new AuthenticationHeaderValue("Basic", ViewModelLocator.TDMAPIStatic.GetClientToken());

                    using (var response = await client.SendAsync(request, HttpCompletionOption.ResponseHeadersRead, cancellationTokenSource.Token))
                    {
                        response.EnsureSuccessStatusCode();

                        TotalBytes = response.Content.Headers.ContentLength ?? 0;

                        using (var responseStream = await response.Content.ReadAsStreamAsync())
                        using (var fileStream = new FileStream(filePath, FileMode.Create, FileAccess.Write))
                        {
                            int read;
                            var buffer = new byte[bufferSize];
                            while ((read = await responseStream.ReadAsync(buffer, 0, bufferSize, cancellationTokenSource.Token)) > 0)
                            {
                                await fileStream.WriteAsync(buffer, 0, read, cancellationTokenSource.Token);
                                TotalRead += read;
                            }
                        }
                    }
                }
            }
            finally
            {
                cancellationTokenSource.Dispose();
                cancellationTokenSource = null;
            }
            
            return new FileInfo(filePath);
        }      
        
        public void Cancel()
        {
            Cancelled = true;

            if (cancellationTokenSource != null && !cancellationTokenSource.IsCancellationRequested)            
                cancellationTokenSource.Cancel();            
        }

        private string FormatReadableBytes(double length)
        {
            const int baseNumber = 1024;

            int order = 0;
            if (length > 0)
            {
                order = (int)Math.Log(length, baseNumber);
                if (order > byteSizeNames.Length - 1)
                    order = byteSizeNames.Length - 1;
            }

            length /= Math.Pow(baseNumber, order);

            return $"{length:0.00} {byteSizeNames[order]}";
        }

        internal void CleanUp()
        {
            var downloadDirectory = new DirectoryInfo(downloadDirectoryPath);
            if(downloadDirectory.Exists)
            {
                foreach (var file in downloadDirectory.EnumerateFileSystemInfos()) 
                    file.Delete();
            }
        }
    }
}