extern alias newclientapi;

using System.Linq;

public class SerialNumbers
{
    private newclientapi::SerialNumbers _instance;

    internal SerialNumbers(newclientapi::SerialNumbers instance)
    {
        _instance = instance;
    }

    public SerialNumbersSN[] SN
    {
        get => _instance.SN.Select(i => new SerialNumbersSN(i)).ToArray();
        set => _instance.SN = value.Select(i => i._instance).ToArray();
    }

    /// <remarks/>
    public string requestType
    {
        get => _instance.requestType;
        set => _instance.requestType = value;
    }

    /// <remarks/>
    public string serialNumberType
    {
        get => _instance.serialNumberType;
        set => _instance.serialNumberType = value;
    }

    /// <remarks/>
    public System.DateTime reservedUTC
    {
        get => _instance.reservedUTC;
        set => _instance.reservedUTC = value;
    }

    /// <remarks/>
    public string siteName
    {
        get => _instance.siteName;
        set => _instance.siteName = value;
    }

    /// <remarks/>
    public string stationName
    {
        get => _instance.stationName;
        set => _instance.stationName = value;
    }

    /// <remarks/>
    public int batchSize
    {
        get => _instance.batchSize;
        set => _instance.batchSize = value;
    }

    /// <remarks/>
    public int fetchWhenLessThan
    {
        get => _instance.fetchWhenLessThan;
        set => _instance.fetchWhenLessThan = value;
    }

    /// <remarks/>
    public bool fetchWhenLessThanSpecified
    {
        get => _instance.fetchWhenLessThanSpecified;
        set => _instance.fetchWhenLessThanSpecified = value;
    }

    /// <remarks/>
    public string receipt
    {
        get => _instance.receipt;
        set => _instance.receipt = value;
    }

    /// <remarks/>
    public string tokenId
    {
        get => _instance.tokenId;
        set => _instance.tokenId = value;
    }

    /// <remarks/>
    public string url
    {
        get => _instance.url;
        set => _instance.url = value;
    }

    /// <remarks/>
    public bool onlyInSequence
    {
        get => _instance.onlyInSequence;
        set => _instance.onlyInSequence = value;
    }

    /// <remarks/>
    public bool onlyInSequenceSpecified
    {
        get => _instance.onlyInSequenceSpecified;
        set => _instance.onlyInSequenceSpecified = value;
    }
    /// <remarks/>

    public string refSN
    {
        get => _instance.refSN;
        set => _instance.refSN = value;
    }

    /// <remarks/>
    public string refPN
    {
        get => _instance.refPN;
        set => _instance.refPN = value;
    }

    /// <remarks/>
    public string fromSerialNumber
    {
        get => _instance.fromSerialNumber;
        set => _instance.fromSerialNumber = value;
    }

    /// <remarks/>
    public bool reuseOnDuplicateRequest
    {
        get => _instance.reuseOnDuplicateRequest;
        set => _instance.reuseOnDuplicateRequest = value;
    }

    /// <remarks/>
    public bool reuseOnDuplicateRequestSpecified
    {
        get => _instance.reuseOnDuplicateRequestSpecified;
        set => _instance.reuseOnDuplicateRequestSpecified = value;
    }
}

/// <remarks/>
public class SerialNumbersSN
{
    internal newclientapi::SerialNumbersSN _instance;

    internal SerialNumbersSN(newclientapi::SerialNumbersSN instance)
    {
        _instance = instance;
    }

    public string id
    {
        get => _instance.id;
        set => _instance.id = value;
    }

    /// <remarks/>
    public System.DateTime taken
    {
        get => _instance.taken;
        set => _instance.taken = value;
    }

    /// <remarks/>
    public bool takenSpecified
    {
        get => _instance.takenSpecified;
        set => _instance.takenSpecified = value;
    }

    /// <remarks/>
    public int seq
    {
        get => _instance.seq;
        set => _instance.seq = value;
    }

    /// <remarks/>
    public bool seqSpecified
    {
        get => _instance.seqSpecified;
        set => _instance.seqSpecified = value;
    }

    /// <remarks/>
    public string refSN
    {
        get => _instance.refSN;
        set => _instance.refSN = value;
    }

    /// <remarks/>
    public string refPN
    {
        get => _instance.refPN;
        set => _instance.refPN = value;
    }

    /// <remarks/>
    public string refStn
    {
        get => _instance.refStn;
        set => _instance.refStn = value;
    }
}
