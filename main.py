#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Author: @sarangof
"""

# Imports, etc.
from jotform import JotformAPIClient
import pandas as pd
from sampling import *

# Check if there are new submissions at all ()


# Check on both forms (parametros, ingresar empresa, general)
# Guardar un log del id y el tiempo de la ultima submission
# Si hay un par {id,tiempo} nuevo, proseguir.

FORM_1 = "62355313880152"
FORM_2 = "62357176330151"
FORM_3 = "62356528846163"

var = 'A'

# Jotform API call, submission
jotFormKey = '33dcf578e3523959b282e1bebff1f581'
jotformAPIClient = JotformAPIClient(jotFormKey)

def return_submission(form_option):
    submission = jotformAPIClient.get_form_submissions(form_option)
    submission = submission[len(submission)-1] # last submission
    return submission

# CASO 1

if var=='A': # Se hizo un request para pedir parámetros de una nueva encuesta    
    submission = return_submission(FORM_1)
    try:
        url_bdd = str(submission['answers'][u'5']['answer'][0])
        nombre_empresa = str(submission['answers'][u'6']['answer'])
    except KeyError:
        url_bdd = str(submission[0]['answers'][u'5']['answer'][0])
        nombre_empresa = str(submission[0]['answers'][u'6']['answer'])
    
    generar_muestra(url_bdd,nombre_empresa)
elif var=='B':
    data = create_db(submission)
    vis_answers(data)
""" 
elif var=='C':
    continue
else:
    continue
"""


# Nueva empresa()

# Analizar nueva empresa()

# Generar resultados totales()