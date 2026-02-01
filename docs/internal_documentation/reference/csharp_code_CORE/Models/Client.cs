using System;

namespace Virinco.WATS.Interface.Models
{
    internal class Client
    {
        public int Client_ID { get; set; }

        public string Name { get; set; }
        public Guid? GUID { get; set; }

        public DateTime RegDate { get; set; }

        public int Status { get; set; }
        public int? Parent_ID { get; set; }
        public int ClientGroup_ID { get; set; }
        public string MiscInfo { get; set; }
        public DateTime? MiscInfo_Updated { get; set; }
        public string Location { get; set; }
        public string Purpose { get; set; }
        public ClientType ClientType { get; set; }
        public decimal UTCOffset { get; set; }
        public string Description { get; set; }
        public DateTime? LastPing { get; set; }
        public string StatusText { get; set; }
        public string MachineAccountId { get; set; }
        public string SiteCode { get; set; }
    }
    public enum ClientType
    {
        /*LegacyClient=0,*/
        LocalServer = 1,
        MasterServer = 2,
        TestStation = 5,
        WebClient = 6,
        VirtualLevel = 7
    }
}