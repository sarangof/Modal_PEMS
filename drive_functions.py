#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 17:43:54 2016

@author: saf537
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


try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

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
                                   'creds.json')
    # If modifying these scopes, delete your previously saved credentials
    # at ~/.credentials/drive-python-quickstart.json   
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

def insert_file(title, description, parent_id, mime_type, filename):
  """Insert new file.

  Args:
    title: Title of the file to insert, including the extension.
    description: Description of the file to insert.
    parent_id: Parent folder's ID.
    mime_type: MIME type of the file to insert.
    filename: Filename of the file to insert.
  Returns:
    Inserted file metadata if successful, None otherwise.
  """

  credentials = get_credentials()
  http = credentials.authorize(httplib2.Http())
  service = discovery.build('drive', 'v2', http=http)
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
    return file
  except errors.HttpError, err:
      if err.resp.get('content-type', '').startswith('application/json'):
          reason = json.loads(err.content)['error']
          print(reason)
  return None


def insert_folder(parent_id,folder_name):
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    folder_id = parent_id
    file_metadata = {
      'name' : folder_name,
      'mimeType' : 'application/vnd.google-apps.folder',
      'parents': [ folder_id ]
    }
    created_folder = service.files().create(body=file_metadata,
                                        fields='id').execute()
    return str(created_folder['id'])
    # Manage error

#SCOPES =  'https://www.googleapis.com/auth/drive' 
#CLIENT_SECRET_FILE = 'client_secret.json' 
#APPLICATION_NAME = 'Drive API Python Quickstart'

