# Imports
from __future__ import print_function
import re
import pandas as pd
import numpy  as np
from sklearn.cross_validation import train_test_split
from drive_functions import *


def generar_muestra(url_bdd,nombre):
    
    bdd_empresa = pd.read_csv(url_bdd) # Leer formulario de todos los empleados
    
    # How to include a measure of error? Throw an exception, perhaps
    pop,sample = train_test_split(np.array(bdd_empresa.cedula),test_size=0.1,stratify=np.array(bdd_empresa.department))
    filename = 'Files/cedulas-'+ '-'.join(re.findall(r"[\w']+",str(nombre)))+'.csv'    
    sample.tofile(filename,sep=',')

    # Insert new folder. Need to handle exceptions.    
    folder_name = 'Empleados-a-encuestar-'+str(nombre)
    parent_id = '0B3D2VjgtkabkaWdQcU9uMkhRaUk' # '0Bz78HNrCokDoc3RQTWYyWk94RG8'
    folder_id = insert_folder(parent_id,folder_name)    
    
    # Insert new file in new folder. Need to handle exceptions.    
    title = filename
    description = 'Cedulas a encuestar en empresa '+str(nombre)+'.'
    mime_type = ''
    insert_file(title, description, folder_id, mime_type, filename) 
    
    