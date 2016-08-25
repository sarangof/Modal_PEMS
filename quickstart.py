#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES =  'https://www.googleapis.com/auth/drive' #'https://www.googleapis.com/auth/drive.metadata.readonly'
CLIENT_SECRET_FILE = 'client_secret.json' 
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(
        pageSize=50,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    if not items:
        print('No files found.')
    else:
        for item in items:
            #if item['id']=='0B3D2VjgtkabkaWdQcU9uMkhRaUk':
            #print('{0} ({1})'.format(item['name'], item['id']))
            print(item)
    #res = service.files().insert('cedulas.csv',bucket='0B3D2VjgtkabkaWdQcU9uMkhRaUk')
    #if res:
    #    print('success')
    
if __name__ == '__main__':
    main()
    
    
    
    
    
    
from apiclient import errors
from apiclient.http import MediaFileUpload

def insert_file(service, title, description, parent_id, mime_type, filename):
  """Insert new file.

  Args:
    service: Drive API service instance.
    title: Title of the file to insert, including the extension.
    description: Description of the file to insert.
    parent_id: Parent folder's ID.
    mime_type: MIME type of the file to insert.
    filename: Filename of the file to insert.
  Returns:
    Inserted file metadata if successful, None otherwise.
  """
  media_body = MediaFileUpload(filename, mimetype=mime_type, resumable=True)
  body = {
    'title': title,
    'description': description,
    'mimeType': mime_type
  }
  # Set the parent folder.
  if parent_id:
    body['parents'] = [{'id': parent_id}]

  try:
    file = service.files().insert(
        body=body,
        media_body=media_body).execute()

    # Uncomment the following line to print the File ID
    # print 'File ID: %s' % file['id']

    return file
  except errors.HttpError, error:
    print('An error occured: %s' % error)
    return None


credentials = get_credentials()
http = credentials.authorize(httplib2.Http())
service = discovery.build('drive', 'v2', http=http)


title = 'pachito'
description = 'pachito es bonito'
parent_id = '0B3D2VjgtkabkaWdQcU9uMkhRaUk'
mime_type = ''
filename = 'cedulas.csv'

perms = service.permissions().list(fileId=parent_id).execute()


error = insert_file(service, title, description, parent_id, mime_type, filename)





service = discovery.build('drive', 'v3', http=http)
file_metadata = {
  'name' : 'Invoices',
  'mimeType' : 'application/vnd.google-apps.folder'
}
file = service.files().create(body=file_metadata,fields='id').execute()
print('Folder ID: %s' % file.get('id'))

