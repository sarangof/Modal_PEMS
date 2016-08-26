#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author: @sarangof
"""

# Imports, etc.
from jotform import JotformAPIClient
import pandas as pd
import filecmp
from shutil import copyfile
from sampling import *

# Check if there are new submissions at all ()


# Check on both forms (parametros, ingresar empresa, general)
# Guardar un log del id y el tiempo de la ultima submission
# Si hay un par {id,tiempo} nuevo, proseguir.

FORM_1 = "62355313880152"
FORM_2 = "62357176330151"
FORM_3 = "62356528846163"
form_list = [FORM_1,FORM_2,FORM_3]


# Jotform API call, submission
jotFormKey = '33dcf578e3523959b282e1bebff1f581'
jotformAPIClient = JotformAPIClient(jotFormKey)


def update_submissions():
    n = 1
    bool_dict = {}
    for form_op in form_list:
        submission = jotformAPIClient.get_form_submissions(form_op,limit=5,order_by="created_at")
        log_file_name = str('logs/form'+str(n)+'.log')
        with open("logs/temp.txt", "w") as text_file:
            for sub in submission:            
                text_file.write('Timestamp: {}'.format(sub['updated_at']))
        try: 
            if filecmp.cmp("logs/temp.txt",log_file_name)  == False:
                copyfile("logs/temp.txt",log_file_name)            
                bool_dict["new_form_{0}".format(n)] = True
            else:
                bool_dict["new_form_{0}".format(n)] = False
        except OSError:
            bool_dict["new_form_{0}".format(n)] = True
            with open(log_file_name, "w") as text_file:
                for sub in submission:            
                    text_file.write('Timestamp: {}'.format(sub['updated_at']))
        os.remove("logs/temp.txt")
        n+=1
    new_form_1,new_form_2,new_form_3 = bool_dict.values()
    new_submission = sum(bool_dict.values())>0
    return new_submission,new_form_1,new_form_2,new_form_3 

new_submission,new_form_1,new_form_2,new_form_3  = update_submissions()

def return_submission(form_option):
    submission = jotformAPIClient.get_form_submissions(form_option)[len(submission)-1] # last submission
    return submission

if new_submission:
    # CASO 1   
    if new_form_1: # Se hizo un request para pedir parámetros de una nueva encuesta    
        submission,nombre_empresa = return_submission(FORM_1)
        try:
            url_bdd = str(submission['answers'][u'5']['answer'][0])
            nombre_empresa = str(submission['answers'][u'6']['answer'])
        except KeyError:
            url_bdd = str(submission[0]['answers'][u'5']['answer'][0])
            nombre_empresa = str(submission[0]['answers'][u'6']['answer'])
        generar_muestra(url_bdd,nombre_empresa) #sample goes to Drive/Resultados/Muestras de empresas
        
    # CASO 2
    if new_form_2:
        submission = return_submission(FORM_2)
        nombre_empresa = 'Pachito'
        data = create_db(submission,name=nombre_empresa) # Se guarda en Drive/Resultados/Respuestas_empresas/nombre_empresa
        vis_answers(data,name=nombre_empresa) # Se guarda en Drive/Resultados/Respuestas_empresas/nombre_empresa/visualizaciones
    
    # CASO 3
    if new_form_3:
    

# Nueva empresa()

# Analizar nueva empresa()

# Generar resultados totales()