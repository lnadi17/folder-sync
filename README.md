# folder-sync

folder-sync is a set of Python scripts designed to synchronize files with Google Drive using the `pydrive` library. 
I created these scripts to sync my local mincraft server world with my friend. I wrote two versions of this script, then abandoned 
this project not long after that.

## Prerequisites

- Python 3.x
- Required Python libraries: `pydrive`

## server_sync.py

The `server_sync.py` script allows you to upload files and folders from your local machine to Google Drive. 
It authenticates your Google account, creates a connection to Google Drive, and uploads files recursively.  
The script also provides the option to delete all existing files on Google Drive before the upload process.

## better_sync.py

The `better_sync.py` script enhances the synchronization process with Google Drive. 
It allows you to download the latest version of files from Google Drive or upload the current version as the latest. 
The script compresses files into a zip archive before uploading and extracts files from the archive when downloading.
It provides options to delete all existing files on Google Drive during the upload process.

## More Info

Since the project served its purpose, it is now archived and no further development is expected.
