#!/home/saf537/anaconda2/lib/python2.7/
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:26:47 2016

@author: saf537
"""
import pandas as pd

def calcular_puntajes(data):
    """
    Aqui se implementan las "funciones" de probabilidad de usar cada uno de los modos.
    """    
    df = data[['Edad','Pendiente','Distancia']] #'18. Salario'
    df= 1./dfca
    df -= df.min() 
    df /= df.max()  
    data['Puntaje_bici'] = df.sum(axis=1)/len(df.columns)
    return data

def asignar_grupos(data):
    grupo_bici_1 = data.query('(Edad<40.) & (Distancia < 7000) ')
    """
    Quiénes tienen acceso a una bicicleta? 
    Saben andar en bicicleta? 
    Número de personas que tienen nivel de satisfacción bajo de su modo de transporte
    Número de personas que estarían dispuestas de cambiar su modo hacia la bicicleta
    Percepción buena de bicicleta en cuanto a la seguridad y comodidad
    """
    grupo_bici_2 = data
    
    """
    Porcentaje de personas dispuestas a montar en bicicleta
    """
    
    
    
    return None
    