using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Input;
using Virinco.WATS.Client.Configurator.Helpers;
using Virinco.WATS.Client.Configurator.ViewModel;
using Virinco.WATS.Interface.MES.Production;

namespace Virinco.WATS.Client.Configurator.Pages
{
    public class SerialNumberViewModel : ObservableObject, IPageViewModel_v2
    {
        public string Name => "Serial number handler";

        public List<SerialNumberType> SerialNumberTypes { get; private set; }

        public SerialNumberType SelectedSerialNumberType 
        {
            get => selectedSerialNumberType;
            set
            {                
                selectedSerialNumberType = value;
                SetNewHandler();
                RaisePropertyChanged(nameof(SelectedSerialNumberType));
            }
        }

        public string Status
        {
            get => status;
            set
            {
                status = value;
                RaisePropertyChanged(nameof(Status));
            }
        }        

        public bool Reuse
        {
            get => reuse;
            set
            {
                reuse = value;
                IsDirty = true;
                SetReuse(value);
                RaisePropertyChanged(nameof(Reuse));
            }
        }

        public bool ReserveOffline
        {
            get => online;
            set
            {
                online = value;
                IsDirty = true;
                RaisePropertyChanged(nameof(ReserveOffline));
            }
        }

        public bool InSequence
        {
            get => inSequence;
            set
            {
                inSequence = value;
                IsDirty = true;
                RaisePropertyChanged(nameof(InSequence));
            }
        }

        public string BatchSize
        {
            get => batchSize;
            set
            {
                batchSize = value;
                IsDirty = true;
                RaisePropertyChanged(nameof(BatchSize));
            }
        }

        public string FetchWhenLessThan
        {
            get => fetchWhenLessThan;
            set
            {
                fetchWhenLessThan = value;
                IsDirty = true;
                RaisePropertyChanged(nameof(FetchWhenLessThan));
            }
        }

        public string StartFromSerialNumber
        {
            get => startFromSerialNumber;
            set
            {
                startFromSerialNumber = value;
                IsDirty = true;
                RaisePropertyChanged(nameof(StartFromSerialNumber));
            }
        }

        public bool IsDirty
        {
            get => isDirty;
            set
            {
                isDirty = value;
                RaisePropertyChanged(nameof(IsDirty));
            }
        }

        public string InitializeButtonText
        {
            get => initializeButtonText;
            set
            {
                initializeButtonText = value;
                RaisePropertyChanged(nameof(InitializeButtonText));
            }
        }

        public bool ReuseEnabled
        {
            get => reuseEnabled;
            set
            {
                reuseEnabled = value;
                RaisePropertyChanged(nameof(ReuseEnabled));
            }
        }

        public bool CancelReservedEnabled
        {
            get => cancelReservedEnabled;
            set
            {
                cancelReservedEnabled = value;
                RaisePropertyChanged(nameof(CancelReservedEnabled));
            }
        }

        public ICommand InitializeCommand { get; }

        public ICommand CancelReservedCommand { get; }

        public IEnumerable<LocalSerialNumber> LocalSerialNumbers 
        {
            get => localSerialNumbers;
            private set
            {
                localSerialNumbers = value;
                RaisePropertyChanged(nameof(LocalSerialNumbers));
            }
        }

        private SerialNumberType selectedSerialNumberType;
        private string status;
        private bool reuse;
        private IEnumerable<LocalSerialNumber> localSerialNumbers;

        private bool online;
        private bool inSequence;
        private string batchSize;
        private string fetchWhenLessThan;
        private string startFromSerialNumber;
        private bool isDirty;

        private string initializeButtonText;

        private bool reuseEnabled;
        private bool cancelReservedEnabled;

        private SerialNumberHandler handler;

        private bool initialized = false;

        private const string token = "1C3CFC7C-1386-4219-94F4-06D2B7FD8E18";
        private const string macAddressTypeName = "MAC address";
        private const string runningSNTypeName = "RunningSN";

        public SerialNumberViewModel()
        {
            InitializeCommand = new RelayCommand(o => InitializeSerialNumberType());
            CancelReservedCommand = new RelayCommand(o => CancelReservations());           
        }

        public void Initialize()
        {
            if (initialized)
                return;

            try
            {
                SerialNumberTypes = SerialNumberHandler.GetSerialNumberTypes().ToList();
            }
            catch (Exception e)
            {
                SerialNumberTypes = new List<SerialNumberType>();
            }

            if (SerialNumberTypes.Count > 0)
            {
                var macAddressType = SerialNumberTypes.FirstOrDefault(t => t.Name == macAddressTypeName);
                if (macAddressType != null)
                    selectedSerialNumberType = macAddressType;
                else
                    selectedSerialNumberType = SerialNumberTypes.First();

                SetNewHandler();
            }

            initialized = true;
        }

        public void Uninitialize() { }

        public void InitializeSerialNumberType()
        {
            try
            {
                if (!int.TryParse(BatchSize, out int batchSize))
                    throw new ArgumentException("Batch size is not a number.");

                if (!int.TryParse(FetchWhenLessThan, out int fetchWhenLessThan))
                    throw new ArgumentException("Fetch when less than is not a number.");

                if (!string.IsNullOrEmpty(StartFromSerialNumber))
                {
                    if (!string.IsNullOrEmpty(SelectedSerialNumberType.Regex) && !Regex.IsMatch(StartFromSerialNumber, SelectedSerialNumberType.Regex))
                        throw new ArgumentException("Start from serial number is not properly formated.");
                }
                else
                    StartFromSerialNumber = null;

                handler.Initialize(null, null, ReserveOffline ? SerialNumberHandler.RequestType.Reserve : SerialNumberHandler.RequestType.Take, InSequence, batchSize, fetchWhenLessThan, StartFromSerialNumber, "", new Guid(token));
                handler.SetReuseOnDuplicateRequest(reuse);
                Status = handler.GetStatus().ToString();
                SetHandlerInfo();
                SetButtonsEnabled();

                if (ReserveOffline && !(LocalSerialNumbers?.Any() ?? false))
                    MessageBox.Show("No free serial numbers to reserve. Generate more serial numbers on the WATS server.", "Reserve offline", MessageBoxButton.OK, MessageBoxImage.Information);
            }
            catch (Virinco.WATS.REST.HttpRequestException e)
            {
                string content = e.HttpContent.ReadAsStringAsync().Result;
                MessageBox.Show($"{e.Message}: {content}", "Initialize failed", MessageBoxButton.OK, MessageBoxImage.Error);
            }
            catch (Exception e)
            {
                MessageBox.Show($"{e.Message} {e.InnerException?.Message}", "Initialize failed", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void CancelReservations()
        {
            try
            {
                var batchsize = BatchSize;

                handler.CancelReservations(new Guid(token));
                SetHandlerInfo();
                SetButtonsEnabled();
                IsDirty = true;

                BatchSize = batchsize;
            }
            catch (Exception e)
            {
                MessageBox.Show(e.Message, "Cancel reservations failed", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void SetReuse(bool on)
        {
            try
            {
                bool initialized = handler.GetStatus() == SerialNumberHandler.Status.Ready;
                if(initialized)
                    handler.SetReuseOnDuplicateRequest(on);
            }
            catch (Exception e)
            {
                MessageBox.Show(e.Message, "Setting reuse failed", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void SetNewHandler()
        {
            handler = new SerialNumberHandler(SelectedSerialNumberType.Name);
            Status = handler.GetStatus().ToString();
            SetHandlerInfo();
            SetButtonsEnabled();
        }

        private void SetHandlerInfo()
        {
            try
            {
                if(handler.GetStatus() == SerialNumberHandler.Status.Ready)
                {
                    handler.GetPoolInfo(out bool inSequence, out int batchSize, out int fetchWhenLessThan, out string startFromSerialNumber, out _, out SerialNumberHandler.RequestType requestType);
                    InSequence = inSequence;
                    BatchSize = batchSize.ToString();
                    FetchWhenLessThan = fetchWhenLessThan.ToString();
                    StartFromSerialNumber = startFromSerialNumber;
                    ReserveOffline = requestType == SerialNumberHandler.RequestType.Reserve;
                    Reuse = handler.GetResuseOnDuplicateRequest();
                    IsDirty = false;
                    LocalSerialNumbers = handler.GetLocalSerialNumbers()?.OrderBy<SerialNumbersSN, object>(s =>
                    {
                        if (double.TryParse(s.id, out double d))
                            return d;
                        else
                            return s.id;
                    }).Select(s => new LocalSerialNumber
                    {
                        SerialNumber = s.id,
                        Taken = s.takenSpecified
                    });
                }
                else
                {
                    InSequence = false;
                    BatchSize = "20";
                    FetchWhenLessThan = "10";
                    StartFromSerialNumber = GetDefaultSerialNumber();
                    ReserveOffline = false;
                    reuse = false; //Dont trigger SetReuse
                    RaisePropertyChanged(nameof(Reuse));
                    LocalSerialNumbers = null;
                }
            }
            catch { }
        }

        private void SetButtonsEnabled()
        {
            bool initialized = handler.GetStatus() == SerialNumberHandler.Status.Ready;

            InitializeButtonText = initialized ? "Re-initialize" : "Initialize";
            ReuseEnabled = true;
            CancelReservedEnabled = initialized;
        }

        private string GetDefaultSerialNumber()
        {
            if (SelectedSerialNumberType.Name == macAddressTypeName)
                return "00-00-00-00-00-00";
            else if (SelectedSerialNumberType.Name == runningSNTypeName)
                return "00000000";
            else
                return null;
        }
    }

    public class LocalSerialNumber
    {
        public string SerialNumber { get; set; }

        public bool Taken { get; set; }
    }
}
