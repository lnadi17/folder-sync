from zipfile import ZipFile
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive
import os



def main():
    # Authenticate
    print("Authenticating...")
    gauth = GoogleAuth()
    scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secrets.json', scope)
    drive = GoogleDrive(gauth)
    print("Authenticated.")

    user_input = input("1. Download latest version\n2. Upload this version as latest\nInput: ")

    if (user_input == '1'):
        download(drive)
    if (user_input == '2'):
        delete_all(get_file_list(drive))
        upload(drive)
     
    print("Exiting...")

def download(drive):
    # changed = None

    # for file in get_file_list(drive):     
        # if (file['title'] == 'changed'):
            # changed = file        

    # if (changed is not None):
    for file in get_file_list(drive):
        if (file['title'] == 'data.zip'):
            print("Getting file...")
            file.GetContentFile('data.zip')

            # Extract all the contents of zip file in current directory
            print("Extracting archive...")
            with ZipFile('data.zip', 'r') as zipObj:
                zipObj.extractall()

            print("Removing archive...")
            os.remove('data.zip')
             
            # print("Deleting control file...")
            # changed.Delete()


def upload(drive):
    print("Compressing...")
    # Create zip file
    with ZipFile('data.zip', 'w') as zipObj:
       # Iterate over all the files in directory
       for folderName, subfolders, filenames in os.walk('./'):
           for filename in filenames:
               if (filter_name(filename)):
                   # Create complete filepath of file in directory
                   filePath = os.path.join(folderName, filename)
                   # Add file to zip
                   zipObj.write(filePath)
    
    print("Uploading...")
    data_file = drive.CreateFile()
    data_file.SetContentFile('data.zip')
    data_file.Upload()

    # control_file = drive.CreateFile({'title': 'changed'})
    # control_file.Upload()

    os.remove('data.zip')


def delete_all(list):
    print('Deleting everything...')
    for file in list:
        print('Deleting %s, id: %s' % (file['title'], file['id']))
        file.Delete()


def filter_name(filename):
    return (".py" not in filename
            and ".c" not in filename
            and ".git" not in filename
            and ".json" not in filename
            and ".zip" not in filename
           )


def get_file_list(drive, parent_id='root'):
    file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % parent_id}).GetList()
    return file_list


main()
