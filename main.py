#!/home/saf537/anaconda2/lib/python2.7/
# -*- coding: utf-8 -*-
"""
Author: sarangof
"""

"""
Imports, etc.
"""
from jotform import JotformAPIClient
import filecmp
from shutil import copyfile
from sampling import generar_muestra
from generar_bdd import create_db
import pandas as pd
from generar_visualizaciones import vis_answers, crear_compendios
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
form_list  = [FORM_1,FORM_2]
jotFormKey = '33dcf578e3523959b282e1bebff1f581'
jotformAPIClient = JotformAPIClient(jotFormKey)

def update_submissions():
    """
    Creates a log on the last submission for each of the forms and alerts new submissions.
    """
    n = 1
    bool_dict = {} # Stores truth values to indicate new submissions in any of the forms
    for form_op in form_list:
        submission = jotformAPIClient.get_form_submissions(form_op,limit=5,order_by="created_at")
        log_file_name = str('logs/form'+str(n)+'.log')
        with open("logs/temp.txt", "w") as text_file:
            for sub in submission:            
                text_file.write('Timestamp : {}'.format(sub['updated_at']))
                if form_op == FORM_1:
                    # OJO
                    text_file.write('Empresa: '+'/n')
        try: 
            # -- In case there is already a log file
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
    new_form_1,new_form_2 = bool_dict.values()
    new_submission = sum(bool_dict.values())>0
    return new_submission,new_form_1,new_form_2

def return_submission(form_option):
    """
    Returns the last submission of the request forms
    """
    submission = jotformAPIClient.get_form_submissions(form_option,order_by="created_at")
    submission = submission[0] # last submission
    return submission
    
def generar_analisis(data,folder_id, nombre_empresa):
    viz_folder = vis_answers(data, folder_id, folder_name='Visualizaciones') 
    data = calcular_puntajes(data)    
    asignar_grupos(data, folder_id, nombre_empresa, viz_folder)
    crear_compendios(data, nombre_empresa, folder_id, viz_folder)

new_submission,new_form_1,new_form_2  = update_submissions()

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

        sample_id, folder_id = generar_muestra(url_bdd,nombre_empresa,n_sample) 
        
        # -- Saving sample_id and folder_id in logs
        with open('logs/file_ids.log', "w") as txt_f:
            txt_f.write(format(sample_id)+'/'+format(folder_id))
            txt_f.close()
        del(sample_id,folder_id)
    """
    Second request form:
    Se hizo un request para analizar resultados de una encuesta existente.
    """
    if new_form_2:
        # TIENE QUE HABER UNA FORMA DE ENCONTRAR UN MATCH
        submission = return_submission(FORM_2)
        file = open('logs/file_ids.log', 'r')
        sample_id, folder_id = file.read().split('/')
        nombre_empresa = '-'.join(re.findall(r"[\w']+",str(submission['answers']['12']['answer'])))
        if nombre_empresa != 'Total':
            long_submission  = jotformAPIClient.get_form_submissions('62284736240152',limit=2000000)
            short_submission = jotformAPIClient.get_form_submissions('63025286426152') 
            data, folder_id = create_db(long_submission, short_submission, sample_id, folder_id, name=nombre_empresa) 
            generar_analisis(data,folder_id,nombre_empresa)
        else:
            TOT_folder_id = insert_folder('0B3D2VjgtkabkSVh4d0I2RzZ0LWc','Total')
            TOT_data = pd.read_csv('BDD_PEMS_agregada.csv')
            generar_analisis(TOT_data,TOT_folder_id,'Total')  
 