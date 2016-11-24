# -*- coding: utf-8 -*-

# Imports
from __future__ import print_function
import re
import pandas as pd
from numpy import array
from sklearn.cross_validation import train_test_split
from drive_functions import insert_file, insert_folder

def generar_muestra(url_bdd,nombre,n_sample):
    """
    Generar documento de muestra en carpeta de Drive con el nombre de la empresa.
    """    
    bdd_empresa = pd.read_csv(url_bdd) # Leer formulario de todos los empleados
    
    nombre = '-'.join(re.findall(r"[\w']+",str(nombre)))
    filename = 'cedulas-'+nombre+'.csv' 
    print(len(bdd_empresa))
    try:     
        pop,sample = train_test_split(array(bdd_empresa.cedula),test_size=n_sample) # stratify=np.array(bdd_empresa.departamento)
        sample.tofile('Files/'+filename,sep=',')
    except ValueError:
        with open('Files/'+filename, "w") as text_file:
            text_file.write('ERROR: EL TAMAÑO DE LA MUESTRA DEBERÍA SER MENOR AL TAMAÑO DE LA POBLACIÓN')

    # Insert file in folder, and create folder if needed    
    parent_id = '0B3D2VjgtkabkSVh4d0I2RzZ0LWc' 
    title = filename
    description = 'Cedulas a encuestar en empresa '+str(nombre)+'.'
    new_parent = insert_folder(parent_id,nombre)
    sample_id = insert_file(title, description, new_parent, 'Files/'+filename, mimetype = 'text/csv')
        
    return sample_id, new_parent