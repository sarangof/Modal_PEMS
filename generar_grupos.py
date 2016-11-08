#!/home/saf537/anaconda2/lib/python2.7/
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:26:47 2016

@author: saf537
"""
import re
import unicodedata

def quitar_caracteres_especiales(cols):
    """
    cols_complete = data.columns
    data.columns = data.columns.map(lambda x: ''.join((c for c in unicodedata.normalize('NFD', unicode(x)) if unicodedata.category(c) != 'Mn')))
    data.columns = data.columns.map(lambda x: re.sub(r'[^a-zA-Z\d\s]', '', x))
    cols = data.columns
    data.columns = cols
    return cols_complete,data
    """
    cols = ''.join((c for c in unicodedata.normalize('NFD', unicode(cols)) if unicodedata.category(c) != 'Mn'))
    return cols
    
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
    grupo_bici_1 = data[(data.p12Edad<40.) 
                    & (data.Distancia < 7000) 
                    & (data.N_bicicletas > 0) 
                    & (data.p8230_Sabe_montar_en_bicicleta=='Sí'.encode('utf-8'))
                    & (data.p5412_Sufre_de_alguna_discapacidad =='No')
                    & (data.p6732_Cul_es_su_medio_habitual_ms_frecuente_y_que_utiliza_por_ms_tiempo_en_cada_viaje_para_ir_al_trabajo != 'Bicicleta')
                    & (data.p6833_Cul_es_su_medio_habitual_ms_frecuente_y_que_utiliza_por_ms_tiempo_en_cada_viaje_para_regresar_del_trabajo != 'Bicicleta')
                    ]
    grupo_bici_2da = data
        
    grupo_bici_3 = data[(data.p12Edad<40.) 
                & (data.Distancia < 7000) 
                & (data.N_bicicletas > 0) 
                & (data.p8230_Sabe_montar_en_bicicleta=='Sí'.encode('utf-8'))
                & (data.p5412_Sufre_de_alguna_discapacidad =='No')
                & (data.p6732_Cul_es_su_medio_habitual_ms_frecuente_y_que_utiliza_por_ms_tiempo_en_cada_viaje_para_ir_al_trabajo != 'Bicicleta')
                & (data.p6833_Cul_es_su_medio_habitual_ms_frecuente_y_que_utiliza_por_ms_tiempo_en_cada_viaje_para_regresar_del_trabajo != 'Bicicleta')
                #'p3547_En_general_cunto_le_interesara_utilizar_cada_uno_de_los_siguientes_medios_1_no_le_interesa_3_inters_promedio_5_le_interesa_mucho'
                ]
    
    grupo_bici_4 = data
    
    grupo_tp_1 = data
    
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
    
    
    return grupo_bici_1, grupo_bici_2da, grupo_bici_3, grupo_bici_4,grupo_tp_1, grupo_tp_2, grupo_tp_3, grupo_tp_4, grupo_peaton_1, grupo_peaton_2, grupo_peaton_3, grupo_cc_1, grupo_cc_2, grupo_hf, grupo_teletrabajo 
