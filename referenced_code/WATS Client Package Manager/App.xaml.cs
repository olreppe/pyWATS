using CommandLine;
using CommandLine.Text;
using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Runtime.InteropServices;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Interop;
using Virinco.WATS.Service.MES.Contract;
using Process = System.Diagnostics.Process;

namespace Virinco.WATS.Client.PackageManager
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        //[DllImport("kernel32.dll")]
        //public static extern Boolean AllocConsole();


        [DllImport("kernel32.dll")]
        static extern bool FreeConsole();

        [DllImport("kernel32.dll")]//, SetLastError = true, ExactSpelling = true)]
        private static extern bool AttachConsole(int processId);

        //[DllImport("user32.dll")]
        //static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

        //public static void HideConsoleWindow()
        //{
        //    IntPtr hWnd = System.Diagnostics.Process.GetCurrentProcess().MainWindowHandle;

        //    if (hWnd != IntPtr.Zero)
        //    {
        //        ShowWindow(hWnd, 0); // 0 = SW_HIDE
        //    }
        //}

        //protected override void OnStartup(StartupEventArgs e)
        //{
        //   // HideConsoleWindow();

        //    base.OnStartup(e);


        //}

        void App_Startup(object sender, StartupEventArgs e)
        {
            //HideConsoleWindow();            
            //IntPtr hWnd = System.Diagnostics.Process.GetCurrentProcess().MainWindowHandle;
            bool console = AttachConsole(-1);
            bool startHidden = e.Args.Length == 1 && e.Args[0] == "/start-hidden";

            //Console.WriteLine("Starting");
            if (!startHidden && (console || e.Args.Length > 0))
            {
                Virinco.WATS.Interface.MES.MesInterface mes = new Virinco.WATS.Interface.MES.MesInterface();
                Package[] availablePackages = new Package[0];
                int packageStatus = (int)StatusEnum.Released;

                var options = new Options(); //todo: fix
                //if (CommandLine.Parser.Default.ParseArguments(e.Args, options))
                //{
                //    Console.WriteLine("");

                //    //if (e.Args.Length == 0)//print help if no parameters and run from console
                //    //    Console.WriteLine(options.GetUsage());// options.Help = true;

                //    // Values are available here
                //    if (options.Verbose)
                //    {
                //        Console.WriteLine("Verbose output:");
                //        Console.WriteLine("");

                //        Console.WriteLine("Filter: {0}", options.Filter);
                //        Console.WriteLine("ForceInstall: {0}", options.Install);
                //        Console.WriteLine("PackageStatus: {0}", options.PackageStatus);
                //        Console.WriteLine("");
                //    }
                //    //if (options.Help)
                //    //    Console.WriteLine(options.GetUsage());

                //    if (options.PackageStatus != packageStatus)
                //        packageStatus = options.PackageStatus;

                //    if (!string.IsNullOrEmpty(options.Filter))
                //    {
                //        //List<string> tagNames = new List<string>();
                //        //List<string> tagValues = new List<string>();
                //        string xpath = Utils.getXpath(options.Filter);

                //        List<FileInfo> ExecuteFiles;
                //        List<FileInfo> TopLevelSequences;

                //        if (!string.IsNullOrEmpty(xpath))
                //            availablePackages = mes.Software.GetPackagesByTag(xpath, out ExecuteFiles, out TopLevelSequences, false, false, true, (StatusEnum)packageStatus);

                //        //if (tagNames.Count > 0)
                //        //    availablePackages = mes.Software.GetPackagesByTag(tagNames.ToArray(), tagValues.ToArray(), false, false, true, out ExecuteFiles, out TopLevelSequences, (StatusEnum)packageStatus);

                //        long? totSize = availablePackages.Sum(pa => pa.DownloadSize);
                //        Console.WriteLine("");
                //        Console.WriteLine($"Matching packages: {availablePackages.Length}, {totSize} bytes");
                //        Console.WriteLine("");

                //        foreach (Package p in availablePackages)
                //        {
                //            Console.WriteLine($"{p.Name} - v{p.Version} - {p.Description}, {p.DownloadSize ?? 0} bytes");
                //        }

                //        if (!options.Install)
                //        {
                //            Console.WriteLine("");
                //            Console.WriteLine("Install package(s) with the install parameter ( -i )");
                //        }

                //    }

                //    if (options.Install && availablePackages.Length>0)
                //    {
                //        Console.WriteLine("");
                //        Console.WriteLine("Installing {0} package(s), please wait...", availablePackages.Length);
                //        mes.Software.InstallPackage(availablePackages, false, true);
                //        Console.WriteLine("");
                //        Console.WriteLine("{0} package(s) installed.", availablePackages.Length);
                //    }
                //}

                //FreeConsole();
                System.Windows.Forms.SendKeys.SendWait("{ENTER}");
                //Console.WriteLine("Press Enter to exit.");

                Application.Current.Shutdown();
                Environment.Exit(0);
                //return;
            }
            else
            {
                var mainWindow = new MainWindow();
                AddWindowHook(mainWindow);

                if(!startHidden)
                    mainWindow.Show();
            }
        }

        /// <summary>
        /// Respond to WM_SHOWWINDOW message that has status 5 (custom stauts)
        /// </summary>
        /// <param name="sender"></param>
        /// <param name="e"></param>
        private void AddWindowHook(Window window)
        {
            HwndSource source = HwndSource.FromHwnd(new WindowInteropHelper(window).EnsureHandle());
            source.AddHook(Hook);

            IntPtr Hook(IntPtr windowHandle, int message, IntPtr wordParamPointer, IntPtr longParamPointer, ref bool handled)
            {
                if(message == 0x0018)
                {
                    int wordParam = wordParamPointer.ToInt32();
                    int longParam = longParamPointer.ToInt32();
                    if(longParam == 5 && wordParam == 1)
                    {
                        window.Show();
                        window.Activate();

                        handled = true;
                        return new IntPtr(1);
                    }
                }

                return IntPtr.Zero;
            }
        }

        protected override void OnExit(ExitEventArgs e)
        {
            var processes = Process.GetProcessesByName("Virinco.WATS.Client.PackageManager").ToList();

            if (processes.Count > 1)
            {
                Process originalProcess = null;

                foreach (var process in processes)
                {
                    if (originalProcess == null)
                    {
                        originalProcess = process;
                        continue;
                    }
                    else if (process.StartTime < originalProcess.StartTime)
                    {
                        originalProcess.Kill();
                        originalProcess.WaitForExit();
                        originalProcess = null;
                        originalProcess = process;
                    }
                }
                var currentProcess = Process.GetCurrentProcess();

                if (!currentProcess.Equals(originalProcess))
                {
                    Environment.Exit(0);
                }
            }

            base.OnExit(e);
        }

    }


    class Options
    {
        [Option('f', "filter", Required = false, HelpText = "Filter - string with package filter (tags and values)")]
        public string Filter { get; set; }

        [Option('v', "verbose", HelpText = "Prints all messages to standard output.")]
        public bool Verbose { get; set; }

        [Option('i', "install", HelpText = "Install all matching packages")]
        public bool Install { get; set; }

        [Option('s', "status", Required = false, HelpText = "Package Status - 0=Draft, 1=Pending, 2=Released, 3=Revoked")]
        public int PackageStatus { get; set; }


        //[Option('?', "help", HelpText = "Print help text")]
        //public bool Help { get; set; }


        //todo: fix
        //[ParserState]
        //public IParserState LastParserState { get; set; }

        //[HelpOption]
        //public string GetUsage()
        //{
        //    return HelpText.AutoBuild(this,
        //      (HelpText current) => HelpText.DefaultParsingErrorsHandler(this, current));
        //}
    }

}
