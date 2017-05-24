#!/usr/bin/python
# -*- coding: utf-8 -*-
"""

@author: sarangof

See: http://www.raosoft.com/samplesize.html
"""

# Imports
from __future__ import print_function
import re
import pandas as pd
from numpy import array
from sklearn.model_selection import train_test_split
from drive_functions import insert_file, insert_folder

def generar_muestra(url_bdd,nombre,n_sample):

	"""
	Generar documento de muestra en carpeta de Drive con el nombre de la empresa.
	"""    
	try:
		bdd_empresa = pd.read_csv(url_bdd) # Leer formulario de todos los empleados
	except:
		bdd_empresa = pd.read_excel(url_bdd)

	nombre = '-'.join(re.findall(r"[\w']+",str(nombre)))
	filename = 'cedulas-'+nombre+'.csv' 
	try:
		bdd_empresa = bdd_empresa.reindex(bdd_empresa['Cédula'])
	except:
		try: 
			bdd_empresa = bdd_empresa.reindex(bdd_empresa['Cédulas'])
		except:
			try:
				bdd_empresa = bdd_empresa.reindex(bdd_empresa['Cedula'])
			except:
				try:
					bdd_empresa = bdd_empresa.reindex(bdd_empresa['Cedulas'])    
				except:
					pass

	try:
		pop,sample = train_test_split(array(bdd_empresa.index),test_size=n_sample) 
		bdd_empresa.ix[sample].to_csv('Files/'+filename,sep=',')
	except ValueError:
	    with open('Files/'+filename, "w") as text_file:
	        text_file.write('ERROR: EL TAMAÑO DE LA MUESTRA DEBERÍA SER MENOR AL TAMAÑO DE LA POBLACIÓN')

	# Insert file in folder, and create folder if needed    
	parent_id = '0B3D2VjgtkabkSVh4d0I2RzZ0LWc' 
	title = filename
	description = 'Personas a encuestar en empresa '+str(nombre)+'.'
	new_parent = insert_folder(parent_id,nombre)
	sample_id = insert_file(title, description, new_parent, 'Files/'+filename)
	    
	return sample_id, new_parent