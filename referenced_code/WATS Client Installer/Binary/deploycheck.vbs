Const CommonAppData = &H23&  ' the second & denotes a long integer '
Dim osh, fld, fso, path
Set osh = CreateObject("Shell.Application")
Set fld = osh.Namespace(CommonAppData)
path = fld.Self.Path & "\Virinco\WATS"
Set fso = CreateObject("Scripting.FileSystemObject")
If (fso.FolderExists(path)) Then
    If (fso.FileExists(path & "\Deploy.xml")) Then
        Set objXML = CreateObject("MSXML2.DOMDocument.6.0")
        With objXML
            .SetProperty "SelectionLanguage", "XPath"
            .ValidateOnParse = True
            .Async = False
            .Load path & "\Deploy.xml"
        End With

        Set elements = objXML.SelectNodes("//*[name()='Product'][(@Id='TS3.1' or @Id='TS3.5' or @Id='TS4.0' or @Id='TS4.1' or @Id='TS4.1.1' or @Id='TS4.2' or @Id='TS4.2.1' or @Id='TS2010' or @Id='TS2010SP1' or @Id='TS2012' or @Id='TS2013' or @Id='TS2014x86' or @Id='TS2014x64' or @Id='TS2016x86' or @Id='TS2016x64' or @Id='TS2017x86' or @Id='TS2017x64' or @Id='TS2018x86' or @Id='TS2018x64' or @Id='TS2019x86' or @Id='TS2019x64' or @Id='TS2020x86' or @Id='TS2020x64') and @State='Installed']")
        If (elements.length > 0) Then
            Dim names        
            For i = 0 to elements.length-1
                names = names & elements(i).getAttribute("Name")
                If (i < elements.length-1) Then
                    names = names & ", "
                End If
            Next
            Session.Property("UNSUPPORTED_TESTSTAND_VERSIONS") = names
            Session.Property("ARE_UNSUPPORTED_TESTSTAND_VERSIONS_INSTALLED") = "1"
        End If
    End If 
End If