#!/home/saf537/anaconda2/lib/python2.7/
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:26:47 2016

@author: saf537
"""
import re
import unicodedata
from generar_visualizaciones import quitar_caracteres_especiales
    
def quitar_espacios(data):
    cols_complete = data.columns
    cols = data.columns
    cols = cols.map(lambda x: x.replace(' ', '_') if isinstance(x, (str, unicode)) else x)
    data.columns = cols 
    return cols_complete,data

def calcular_puntajes(data):
    """
    Aqui se implementan las "funciones" de probabilidad de usar cada uno de los modos.
    """    
    cols = ['p12Edad','Pendiente','Distancia','p8016_Salario_mensual']
    df = data[cols] #'18. Salario'
    df= 1./df
    df -= df.min() 
    df /= df.max()  
    data['Puntaje_bici'] = df.sum(axis=1)/len(df.columns)
    return data

def asignar_grupos(data):
    grupo_bici_1 = data[(data['p12 Edad']<40.) 
                    & (data['Distancia'] < 7000) 
                    & (data[u'p15 29. \xbfDe cu\xe1ntos veh\xedculos disponen en su hogar?. Bicicletas'] > 0) 
                    & (data[u'p82 30. \xbfSabe montar en bicicleta?']=='Sí'.encode('utf-8'))
                    & (data[u'p54 12. \xbfSufre de alguna discapacidad?'] =='No')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'] != 'Bicicleta')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'] != 'Bicicleta')
                    ]
    grupo_bici_2 = data[
                    (data[u'p180 41. \xbfEst\xe1 considerando utilizar un modo de transporte diferente al que ya utiliza?'] == 'Sí'.encode('utf-8'))
                    & (data[u'p165 42. Si respondi\xf3 "S\xed" en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bicicleta')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'] != 'Bicicleta')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'] != 'Bicicleta')
                    ]
        
    grupo_bici_3 = data[(data['p12 Edad']<40.) 
                    & (data['Distancia'] < 7000) 
                    & (data[u'p15 29. \xbfDe cu\xe1ntos veh\xedculos disponen en su hogar?. Bicicletas'] > 0) 
                    & (data[u'p82 30. \xbfSabe montar en bicicleta?']=='Sí'.encode('utf-8'))
                    & (data[u'p54 12. \xbfSufre de alguna discapacidad?'] =='No')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'] != 'Bicicleta')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'] != 'Bicicleta')
                    & (data[u'p35 47. En general \xbfcu\xe1nto le interesar\xeda utilizar cada uno de los siguientes medios? 1 no le interesa, 3 inter\xe9s promedio, 5 le interesa mucho.. Bicicleta'] > 2)
                    & (data[u'p180 41. \xbfEst\xe1 considerando utilizar un modo de transporte diferente al que ya utiliza?'] == 'Sí'.encode('utf-8'))
                    & (data[u'p165 42. Si respondi\xf3 "S\xed" en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bicicleta')   
                    ]
    
    grupo_bici_4 = data[
                    (data[u'p145 55. Si su empresa ofrecer\xeda siguientes incentivos \xbfusted estar\xeda dispuesto a usar la bicicleta (o usarla con m\xe1s frecuencia)?. Biciletas p\xfablicas'] == 'Sí'.encode('utf-8'))
                    & (data[u'p145 55. Si su empresa ofrecer\xeda siguientes incentivos \xbfusted estar\xeda dispuesto a usar la bicicleta (o usarla con m\xe1s frecuencia)?. D\xeda libre en la semana'] == 'Sí'.encode('utf-8'))
                    & (data[u'p145 55. Si su empresa ofrecer\xeda siguientes incentivos \xbfusted estar\xeda dispuesto a usar la bicicleta (o usarla con m\xe1s frecuencia)?. Duchas y biciparqueaderos'] == 'Sí'.encode('utf-8'))
                    & (data[u'p145 55. Si su empresa ofrecer\xeda siguientes incentivos \xbfusted estar\xeda dispuesto a usar la bicicleta (o usarla con m\xe1s frecuencia)?. incentivos monetarios'] == 'Sí'.encode('utf-8'))
                    ]
    
    grupo_tp_1 = data[
                    (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'] != 'Bus/Buseta/Microbus/Bus intermunicipal')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'] != 'Metro/Metroplus/Integrados/Tranvia/Ruta con tarifa integrada')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'] != 'Bus/Buseta/Bus/Buseta/Microbus/Bus intermunicipal')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'] != 'Bicicleta')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'] != 'A pie')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'] != 'Bus/Buseta/Microbus/Bus intermunicipal')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'] != 'Metro/Metroplus/Integrados/Tranvia/Ruta con tarifa integrada')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'] != 'Bus/Buseta/Bus/Buseta/Microbus/Bus intermunicipal')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'] != 'Bicicleta')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'] != 'A pie')
                    ]
    
    grupo_tp_2 = data
    
    grupo_tp_3 = data
    
    grupo_tp_4 = data
    
    grupo_peaton_1 = data
    
    grupo_peaton_2 = data
    
    grupo_peaton_3 = data
    
    grupo_cc_1 = data
    
    grupo_cc_2 = data
    
    grupo_hf = data
    
    grupo_teletrabajo = data[data['p3244_Teletrabajo']=='Sí'.encode('utf-8')]
    
    
    return grupo_bici_1, grupo_bici_2, grupo_bici_3, grupo_bici_4,grupo_tp_1, grupo_tp_2, grupo_tp_3, grupo_tp_4, grupo_peaton_1, grupo_peaton_2, grupo_peaton_3, grupo_cc_1, grupo_cc_2, grupo_hf, grupo_teletrabajo 

