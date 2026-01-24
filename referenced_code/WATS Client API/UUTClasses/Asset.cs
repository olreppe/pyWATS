using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using Virinco.WATS.Schemas.WRML;

namespace Virinco.WATS.Interface
{
    /// <summary>
    /// Represents an asset to track the use of.
    /// </summary>
    public class Asset
    {
        private readonly Asset_type assetRow;

        private readonly UUTReport report;

        internal Asset(UUTReport uut, WATSReport reportRow, string assetSerialNumber, int usageCount)
        {
            report = uut;
            assetRow = new Asset_type();

            AssetSerialNumber = assetSerialNumber;
            UsageCount = usageCount;
            
            reportRow.Assets.Add(assetRow);
        }

        internal Asset(Asset_type assetRow, UUTReport uut)
        {
            report = uut;
            this.assetRow = assetRow;
        }

        /// <summary>
        /// Serial number of the asset.
        /// </summary>
        public string AssetSerialNumber 
        {
            get => assetRow.AssetSN;
            set => assetRow.AssetSN = report.api.SetPropertyValidated<Asset_type>(nameof(Asset_type.AssetSN), value, nameof(AssetSerialNumber));
        }

        /// <summary>
        /// How much the asset was used.
        /// </summary>
        public int UsageCount 
        {
            get => assetRow.UsageCount;
            set
            {
                if (value < 0)
                    throw new ArgumentException($"{nameof(UsageCount)} cannot be negative");
                assetRow.UsageCount = value;
            }
        }

        /// <summary>
        /// The number format for the usage count. See <see cref="NumericLimitTest.NumericValueFormat"/> for more info.
        /// </summary>
        public string UsageCountFormat
        {
            get => assetRow.UsageCountFormat;
            set => assetRow.UsageCountFormat = value;
        }
    }
}
