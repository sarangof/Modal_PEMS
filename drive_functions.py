#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 17:43:54 2016

@author: sarangof. Sources from Google developers.
"""
from __future__ import print_function
import httplib2
import os
import json
import oauth2client
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from apiclient import errors
from apiclient.http import MediaFileUpload

def get_service(version):
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    try:
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'creds.json')
    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/drive-python-quickstart.json   
    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        SCOPES =  'https://www.googleapis.com/auth/drive' 
        CLIENT_SECRET_FILE = 'client_secret.json' 
        APPLICATION_NAME = 'Drive API Python Quickstart'
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', version, http=http)
    return service

def insert_file(title, description, parent_id, filename, mimetype = 'text/csv'):
  """
  Insert new file.

  Args:
    title: Title of the file to insert, including the extension.
    description: Description of the file to insert.
    parent_id: Parent folder's ID.
    mime_type: MIME type of the file to insert.
    filename: Filename of the file to insert.
  Returns:
    Inserted file metadata if successful, None otherwise.
    
  """
  service = get_service('v2')
  duplicate, file_id = check_duplicate_files(title, parent_id)
  if duplicate == False:
      try:
          media_body = MediaFileUpload(filename, mimetype, resumable=True)
          body = {
            'title': title,
            'description': description,
            'mimeType': mimetype
          }
          # Set the parent folder.
          body['parents'] = [{'id': parent_id}]
          file = service.files().insert(
              body=body,
              media_body=media_body).execute()
          file_id = str(file['id'])
      except errors.HttpError, err:
          if err.resp.get('content-type', '').startswith('application/json'):
              reason = json.loads(err.content)['error']
              print(reason)
              return None
  else:   
      update_file(file_id, title, description, filename)
  return file_id

def insert_folder(parent_id, folder_name):
    """
    Inserts the folder "folder_name" into the folder with the given "parent_id"
    """
    service = get_service('v3')
    folder_id = parent_id
    file_metadata = {
      'name' : folder_name,
      'mimeType' : 'application/vnd.google-apps.folder',
      'parents': [ folder_id ]
    }
    duplicate_folder,new_folder_id = check_duplicate_files(folder_name,folder_id)
    if duplicate_folder==False:
        created_folder = service.files().create(body=file_metadata,
                                            fields='id').execute()
        new_folder_id = str(created_folder['id'])    
    return new_folder_id
    # Manage error
    
def check_duplicate_files(file_name, parent_id):
    """
    Checks for files with the name "file_name" inside the folder with the given "parent_id".
    """    
    duplicate = False
    file_id = None
    service = get_service('v2')
    query = str("'"+parent_id+"' in parents and trashed = false")
    for files in service.files().list(q=query).execute()['items']:
        if files['title'].encode('utf-8') == file_name.encode('utf-8'):
            duplicate=True
            file_id = str(files['id'])
            break
    return duplicate, file_id
    
def find_file_id(file_name):
    """
    Find id of the file or folder with the given name.
    * file_name
    """
    file_id = ''
    parent_id = ''
    service = get_service('v2')
    for files in service.files().list(q="trashed = false").execute()['items']:
        if files['title'].encode('utf-8') == file_name.encode('utf-8'):
            file_id = str(files['id'])
            parent_id = str(files['parents'][0]['id'])
            break
    return file_id,parent_id
    
def load_file(file_id):
    service = get_service('v2')
    #service.files().list(q="name contains 'cedulas-Buena-Nota'").execute()
    for files in service.files().list(q="trashed = false").execute()['items']:
        if files['id'] == file_id:
            imp = files
            break          
    download_url = str(imp['downloadUrl'])
    del(imp)
    resp, content = service._http.request(download_url)
    id_list =  content.split(",")
    
    return id_list
    

def update_file(file_id, title, description, filename):
  """
  Update an existing file's metadata and content.
  Args:
    service: Drive API service instance.
    file_id: ID of the file to update.
    new_title: New title for the file.
    new_description: New description for the file.
    new_mime_type: New MIME type for the file.
    new_filename: Filename of the new content to upload.
    new_revision: Whether or not to create a new revision for this file.
  Returns:
    Updated file metadata if successful, None otherwise.
  """
  service = get_service('v2')
  try:
    # First retrieve the file from the API.
    file = service.files().get(fileId=file_id).execute()

    # File's new metadata.
    body = {
    'title': title,
    'description': description,
    'mimeType': 'text/csv'
    }  
    
    # File's new content.
    media_body = MediaFileUpload(filename, mimetype='text/csv', resumable=True)
    

    # Send the request to the API.
    updated_file = service.files().update(
        fileId=file_id,
        body=body, #body=file
        media_body=media_body).execute()
  except errors.HttpError, error:
    print('An error occurred: %s' % error)

def insert_new(nombre, parent_id, title, description, filename):
    """
    Insert new file if it does not exist, or 
    """
    if check_duplicate_files(nombre,parent_id)[0]==False:
        folder_id = insert_folder(parent_id,nombre)    
        file_id   = insert_file(title, description, folder_id, 'Files/'+filename) 
    else:
        file_id, parent_id = find_file_id(filename)     
        update_file(file_id, title, description, 'Files/'+filename)#insert_file(title, description, folder_id,  'Files/'+filename) 
    return folder_id, file_id
