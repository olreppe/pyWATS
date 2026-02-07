In this project we will improve the optional data loss protection safety-net.

We want to enable some new features in the client and configurator:
- Files that are dropped in a converters upload directory should optionally be stored locally for a given period or until a given max storage size.
- The storage must somehow be able to track what parameters was used when converted.
- The client converter gui should have a way to restore these files and reconvert them using a restore and reconvert tool where they can see a list of converted logs, filter them and select a set for reupload.
- The same goes for the outputed .json files. The default PPA should be a new mode "Archive" which deletes from the Done directory and archives the files in a compressed storage for a given period or until a max size it reached.
