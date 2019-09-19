from pydrive.drive import GoogleDrive
from pydrive.auth import GoogleAuth, ServiceAccountCredentials
from pydrive.drive import GoogleDrive
import sys
import os



# Global stuff
drive = None

def main():
    # Authenticate
    print("Authenticating...")
    gauth = GoogleAuth()
    scope = ['https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/drive.file']
    gauth.credentials = ServiceAccountCredentials.from_json_keyfile_name('client_secrets.json', scope)
    
    # Initialize drive
    global drive
    drive = GoogleDrive(gauth)

    delete_all(get_file_list())

    upload_recursive()

    # Add a file which marks dir as changed
    control_file = drive.CreateFile({'title': 'changed'})
    control_file.Upload()

    # for file in get_file_list():
    #     print(file['title'], file['id'])

    print("Done")


def upload_recursive(folder_id='root', path='.'):
    filename_list = []
    foldername_list = []

    for name in os.listdir(path):
        if (".git" not in name and ".py" not in name and ".c" not in name and ".json" not in name):
            if (os.path.isfile(os.path.join(path, name))):
                filename_list.append(name)
            if (os.path.isdir(os.path.join(path, name))):
                foldername_list.append(name)
    
    upload_files(path, filename_list, folder_id)
    
    for name in foldername_list:
        new_path = os.path.join(path, name)
        print("New path %s" % new_path)
        folder = createFolder(name, folder_id)
        folder_id = folder['id']
        upload_recursive(folder_id, os.path.join(path, name))


def get_file_list(parent_id='root'):
    file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % parent_id}).GetList()
    return file_list


def delete_all(list):
    print('Deleting everything...')
    for file in list:
        # print('Deleting %s, id: %s' % (file['title'], file['id']))
        file.Delete()
    print('Deleting done')


def upload_files(path, name_list, parent_id='root'):
    print(name_list)
    for name in name_list:
        file = drive.CreateFile({"title": name, "kind": "drive#fileLink", "parent": parent_id})

        # Read file and set it as a content of this instance
        file.SetContentFile(os.path.join(path, name))
        file.Upload()

        print("Uploaded %s" % os.path.join(path, name))


def createFolder(name, parent_id='root'):
    folder_metadata = {
        'title': name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [{"kind": "drive#fileLink", "id": parent_id}]
    }

    folder = drive.CreateFile(folder_metadata)
    folder.Upload()

    return folder


# def is_folder(file):
#     return (file['mimeType'] == 'application/vnd.google-apps.folder')


main()
