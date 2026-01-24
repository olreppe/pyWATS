Const CommonAppData = &H23&  ' the second & denotes a long integer '
Dim osh, fld, fso, path
Set osh = CreateObject("Shell.Application")
Set fld = osh.Namespace(CommonAppData)
path = fld.Self.Path & "\Virinco\WATS"
Set fso = CreateObject("Scripting.FileSystemObject")
If (fso.FolderExists(path)) Then
    If (fso.FileExists(path & "\Deploy.xml")) Then
        fso.CopyFile path & "\Deploy.xml", path & "\Deploy.xml.bak"
    End If 
End If