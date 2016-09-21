# -*- coding: utf-8 -*-

# Imports
from __future__ import print_function
import re
import pandas as pd
import numpy  as np
from sklearn.cross_validation import train_test_split
from drive_functions import insert_file, check_duplicate_files, insert_folder, find_parent_id

def generar_muestra(url_bdd,nombre,n_sample):
    """
    Generar documento de muestra en carpeta de Drive con el nombre de la empresa.
    """    
    bdd_empresa = pd.read_csv(url_bdd) # Leer formulario de todos los empleados
    
    nombre = '-'.join(re.findall(r"[\w']+",str(nombre)))
    filename = 'cedulas-'+nombre+'.csv' 
    print(len(bdd_empresa))
    try:     
        pop,sample = train_test_split(np.array(bdd_empresa.cedula),test_size=n_sample,stratify=np.array(bdd_empresa.department))
        sample.tofile('Files/'+filename,sep=',')
    except ValueError:
        with open('Files/'+filename, "w") as text_file:
            text_file.write('ERROR: EL TAMAÑO DE LA MUESTRA DEBERÍA SER MENOR AL TAMAÑO DE LA POBLACIÓN')

    # Insert file in folder, and create folder if needed    
    parent_id = '0B3D2VjgtkabkSVh4d0I2RzZ0LWc' # '0Bz78HNrCokDoc3RQTWYyWk94RG8'
    title = filename
    description = 'Cedulas a encuestar en empresa '+str(nombre)+'.'
    mime_type = ''
    if check_duplicate_files(nombre)==False:
        folder_id = insert_folder(parent_id,nombre)    
        insert_file(title, description, folder_id, mime_type, 'Files/'+filename) 
    else:
        folder_id = find_parent_id(nombre)
        insert_file(title, description, folder_id, mime_type, 'Files/'+filename)   