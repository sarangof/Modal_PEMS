#!/home/saf537/anaconda2/lib/python2.7/
# -*- coding: utf-8 -*-
"""
Author: @sarangof
"""

"""
Imports, etc.
"""
from jotform import JotformAPIClient
import filecmp
from shutil import copyfile
from sampling import generar_muestra
from generar_bdd import create_db
from generar_visualizaciones import vis_answers
from drive_functions import find_parent_id
from generar_grupos import *
import unicodedata
import sys
import os
import re

reload(sys)  
sys.setdefaultencoding('utf8')

"""
Jotform API call, submission ids, etc.
"""
FORM_1 = "62355313880152" # Interfaz de usuario
FORM_2 = "62357176330151" # Generar análisis por empresa
FORM_3 = "62356528846163" # Generar datos a partir del consolidado
form_list  = [FORM_1,FORM_2,FORM_3]
jotFormKey = '33dcf578e3523959b282e1bebff1f581'
jotformAPIClient = JotformAPIClient(jotFormKey)

def update_submissions():
    """
    Creates a temporal file to compare with the submissions.
    """
    n = 1
    bool_dict = {} # Stores truth values to indicate new submissions in any of the forms
    for form_op in form_list:
        submission = jotformAPIClient.get_form_submissions(form_op,limit=5,order_by="created_at")
        log_file_name = str('logs/form'+str(n)+'.log')
        with open("logs/temp.txt", "w") as text_file:
            for sub in submission:            
                text_file.write('Timestamp: {}'.format(sub['updated_at']))
                if form_op == FORM_1:
                    # OJO
                    text_file.write('NUMERO DE PERSONAS')
        try: 
        # Case that there is already a log file
            if filecmp.cmp("logs/temp.txt",log_file_name)  == False:
                copyfile("logs/temp.txt",log_file_name)            
                bool_dict["new_form_{0}".format(n)] = True
            else:
                bool_dict["new_form_{0}".format(n)] = False
        
        except OSError:
        # Case that there were no log files
            bool_dict["new_form_{0}".format(n)] = True
            with open(log_file_name, "w") as text_file:
                for sub in submission:            
                    text_file.write('Timestamp: {}'.format(sub['updated_at']))
        os.remove("logs/temp.txt")
        n+=1
    new_form_1,new_form_2,new_form_3 = bool_dict.values()
    new_submission = sum(bool_dict.values())>0
    return new_submission,new_form_1,new_form_2,new_form_3 

def return_submission(form_option):
    """
    Returns the last submission of the request forms
    """
    submission = jotformAPIClient.get_form_submissions(form_option,order_by="created_at")
    submission = submission[0] # last submission
    return submission

new_submission,new_form_1,new_form_2,new_form_3  = update_submissions()

if new_submission:
    
    """
    First request form: 
    Se hizo un request para pedir parámetros de una nueva encuesta.
    """
    if new_form_1: 
        submission = return_submission(FORM_1)
        try:
            url_bdd        = str(submission['answers'][u'5']['answer'][0])
            nombre_empresa = str(submission['answers'][u'6']['answer'])
            n_sample       = int(submission['answers'][u'7']['answer'])
        except KeyError:
            url_bdd        = str(submission[0]['answers'][u'5']['answer'][0])
            nombre_empresa = str(submission[0]['answers'][u'6']['answer'])
            n_sample       = int(submission[0]['answers'][u'7']['answer'])
        sample_id = generar_muestra(url_bdd,nombre_empresa,n_sample) #sample goes to Drive/Resultados/Muestras de empresas
        
    """
    Second request form:
    Se hizo un request para analizar resultados de una encuesta existente.
    """
    if new_form_2:
        # FIX PREREQUISITES.
        
        submission = return_submission(FORM_2)
        nombre_empresa = '-'.join(re.findall(r"[\w']+",str(submission['answers']['12']['answer'])))   
        long_submission  = jotformAPIClient.get_form_submissions('62284736240152',limit=2000000)
        short_submission = jotformAPIClient.get_form_submissions('63025286426152')  # change survey ID
        # Generar para largo y para corto
        data, folder_id = create_db(long_submission,short_submission,sample_id,name=nombre_empresa) # Se guarda en Drive/Resultados/Respuestas_empresas/nombre_empresa
        #cols_complete, data = quitar_caracteres_especiales(data)
        vis_answers(data,nombre_empresa,parent_id = folder_id) # Se guarda en Drive/Resultados/Respuestas_empresas/nombre_empresa/visualizaciones
       
        #data = calcular_puntajes(data)                    
        #data = asignar_grupos(data)
        # OJO: NUEVAS COLUMNAS
        #data.columns = cols_complete
    
    """
    Third request form:
    Se pide analizar todos los resultados existentes.
    """
    if new_form_3:
        # generar_grupos para todas las BDD
        # data: BDD consolidada.
        pass
    