using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Globalization;
using System.Linq;
using System.Reflection;
using System.Runtime.CompilerServices;
using System.Runtime.Versioning;
using System.Text;
using System.Threading.Tasks;
//#if NET8_0_OR_GREATER
using Windows.Devices.Geolocation;
//#endif

namespace Virinco.WATS
{
#if NET8_0_OR_GREATER
    [SupportedOSPlatform("windows10.0.10240")]
#endif
    public static class WindowsLocationService
    {
        public static async Task<Coordinates> GetCoordinates()
        {
            var locator = new Geolocator();
            var position = (await locator.GetGeopositionAsync()).Coordinate;

            return new Coordinates { Latitude = position.Point.Position.Latitude, Longitude = position.Point.Position.Longitude };
        }

        public static async Task<bool> IsAvailable()
        {
            try
            {
                await ActuallIsAvailable();
                return true;
            }
            catch
            {
                return false;
            }
        }

        [MethodImpl(MethodImplOptions.NoInlining)]
        private static async Task ActuallIsAvailable()
        {
            await Geolocator.RequestAccessAsync();
        }

        public static async Task<bool> IsEnabled()
        {
            return (await Geolocator.RequestAccessAsync()) == GeolocationAccessStatus.Allowed;
        }

        public static void OpenLocationSettings()
        {
            var process = new Process();
            process.StartInfo.FileName = "ms-settings:privacy-location";
            process.StartInfo.UseShellExecute = true;
            process.Start();
            //Process.Start("ms-settings:privacy-location");
        }

        public struct Coordinates
        {
            public double Longitude { get; set; }

            public double Latitude { get; set; }            

            public override string ToString()
            {
                return $"{Latitude.ToString(CultureInfo.InvariantCulture)}, {Longitude.ToString(CultureInfo.InvariantCulture)}";
            }
        }
    }
}
