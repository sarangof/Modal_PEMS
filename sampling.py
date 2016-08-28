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
    nombre = '-'.join(re.findall(r"[\w']+",str(nombre)))
    pop,sample = train_test_split(np.array(bdd_empresa.cedula),test_size=0.1,stratify=np.array(bdd_empresa.department))
    filename = 'cedulas-'+nombre+'.csv'    
    sample.tofile('Files/'+filename,sep=',')

    # Insert new folder. Need to handle exceptions.    
    parent_id = '    ' # '0Bz78HNrCokDoc3RQTWYyWk94RG8'
    if check_duplicate_files(nombre)==False:
        folder_id = insert_folder(parent_id,folder_name)    
        title = filename
        description = 'Cedulas a encuestar en empresa '+str(nombre)+'.'
        mime_type = ''
        insert_file(title, description, folder_id, mime_type, filename) 
    else:
        folder_id = find_parent_id(nombre)
        insert_file(title, description, folder_id, mime_type, filename) 
            
    # Insert new file in new folder. Need to handle exceptions.    