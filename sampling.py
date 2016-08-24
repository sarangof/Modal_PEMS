# Imports
from __future__ import print_function
import pandas as pd
import numpy  as np
from sklearn.cross_validation import train_test_split
#from main import *
import httplib2
import os
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools


# Google Drive API interaction
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
    
    

# Need Google Drive API to send the test

def generar_muestra(url_bdd,nombre):
    
    bdd_empresa = pd.read_csv(url_bdd)
    
    # How to include a measure of error?
    pop,sample = train_test_split(np.array(bdd_empresa.cedula),test_size=0.1,stratify=np.array(bdd_empresa.department))
    
    # Return ids of employees. SAVE IT IN GOOGLE DRIVE.
    
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)
    file_metadata = {
      'name' : 'Invoices',
      'mimeType' : 'application/vnd.google-apps.folder'
    }
    file = service.files().create(body=file_metadata,fields='id').execute()
    print('Folder ID: %s' % file.get('id'))
 
    
    sample.tofile('cedulas'+str(nombre)+'.csv',sep=',')