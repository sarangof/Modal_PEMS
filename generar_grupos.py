#!/home/saf537/anaconda2/lib/python2.7/
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:26:47 2016

@author: saf537
"""
import pandas as pd
import re

def renombrar_columnas(data):
    cols_complete = data.columns
    data.columns = data.columns.map(lambda x: re.sub(r'[^a-zA-Z\d\s]', '', x))
    cols = data.columns
    cols = cols.map(lambda x: x.replace(' ', '_') if isinstance(x, (str, unicode)) else x)
    data.columns = cols 
    return cols_complete,data

def calcular_puntajes(data):
    """
    Aqui se implementan las "funciones" de probabilidad de usar cada uno de los modos.
    """    
    cols = ['p12_Edad','Pendiente','Distancia','p80_16._Salario_(mensual)']
    df = data[cols] #'18. Salario'
    df= 1./df
    df -= df.min() 
    df /= df.max()  
    data['Puntaje_bici'] = df.sum(axis=1)/len(df.columns)
    return data

def asignar_grupos(data):
    data['N_bicicletas'] = [x[u'Bicicletas'] for x in data[u'p15_29._¿De_cuántos_vehículos_disponen_en_su_hogar?']]
    grupo_bici_1 = data.query("(p12_Edad<40.) & (Distancia < 7000) & (N_bicicletas > 0) & (p82_30._¿Sabe_montar_en_bicicleta?=Sí)")
    """
    Quiénes tienen acceso a una bicicleta? 
    Saben andar en bicicleta? 
    Número de personas que tienen nivel de satisfacción bajo de su modo de transporte
    Número de personas que estarían dispuestas de cambiar su modo hacia la bicicleta
    Percepción buena de bicicleta en cuanto a la seguridad y comodidad
    """
    grupo_bici_2 = data
    
    """
    ¿Consideraría usar habitualmente un medio de transporte diferente a XX?
    ¿Si tuviera que considerar el uso habitual un medio de transporte diferente a XXcuál utilizaría?
    """
    
    grupo_bici_3 = grupo_bici_1 = data.query("(p12_Edad<40.) & (Distancia < 7000) & (N_bicicletas > 0)")
    
    #grupo_bici_4 =     
    
    #grupo_tp_1 = data
    
    #grupo_tp_2 = data
    
    """
    Porcentaje de personas dispuestas a montar en bicicleta
    """
    
    
    
    return None
    