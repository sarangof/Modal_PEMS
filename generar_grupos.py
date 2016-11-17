#!/home/saf537/anaconda2/lib/python2.7/
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:26:47 2016

@author: saf537
"""
from drive_functions import insert_file, insert_folder
from cartodb import CartoDBAPIKey, FileImport
import requests
import json
    
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
    cols = ['p12 Edad','Pendiente','Distancia','p80 16. Salario (mensual)']
    df = data[cols] #'18. Salario'
    df= 1./df
    df -= df.min() 
    df /= df.max()  
    data['Puntaje_bici'] = df.sum(axis=1)/len(df.columns)
    
    return data
    
def insertar_mapa(file_name,grupo,group_folder_id):
        carto_username = 'saf537'
        carto_key =  '17179e6a8fc54fe03857e65f1d562caf98a8d4bb'    
        cl = CartoDBAPIKey(carto_key, carto_username)  
        grupo[['Emisiones','Latitude','Longitude']].to_excel('grupos/'+file_name+'.xlsx',index=False) 
        insert_file(file_name+'.csv',' ',group_folder_id, 'grupos/'+file_name+'.xlsx',mimetype='text/csv') 
        fi = FileImport('grupos/'+file_name+'.xlsx', cl, privacy='public',content_guessing='true',create_vis='true',table_name=file_name)
        fi.run()
        
        call = 'https://'+carto_username+'.carto.com/api/v1/imports/'+str(fi.item_queue_id)+'?api_key='+carto_key
        request = requests.get(call)
#==============================================================================
#         d = json.loads(request.content)
#         if d['success'] == True:
#             if d['error_code']==None:
#                 vis_id = str(d['visualization_id'])
#         
#         #status_request = requests.get('https://'+carto_username+'.carto.com/api/v1/imports/'+str(d['id']))
#         #r = requests.post('https://'+carto_username+'.carto.com/api/v3/visualization_exports\?api_key\='+carto_key, data={'visualization_id': vis_id})
#         r = requests.post('https://saf537.carto.com/api/v3/visualization_exports\?api_key\=17179e6a8fc54fe03857e65f1d562caf98a8d4bb', data={'visualization_id': vis_id})
#         d2 = json.loads(r.content)
#==============================================================================
        
        
        
def asignar_grupos(data, folder_id,nombre_empresa):
    
    """
    Asigna grupos objetivo segun las respuestas de la encuesta (del dataframe "data").
    Graba archivos en la carpeta de Drive (folder_id).
    Utiliza el nombre de la empresa como referencia (nombre_empresa).
    """
    
    group_folder_id = insert_folder(folder_id,'Grupos')
    grupo_bici_1 = data[(data['p12 Edad']<40.) 
                    & (data['Distancia'] < 7000) 
                    & (data[u'p15 29. \xbfDe cu\xe1ntos veh\xedculos disponen en su hogar?. Bicicletas'] > 0) 
                    & (data[u'p82 30. \xbfSabe montar en bicicleta?']=='Sí'.encode('utf-8'))
                    & (data[u'p54 12. \xbfSufre de alguna discapacidad?'] =='No')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'] != 'Bicicleta')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'] != 'Bicicleta')
                    ]
                    
    if len(grupo_bici_1) > 0:
        file_name = nombre_empresa+'-grupo_bici_1'
        insertar_mapa(file_name,grupo_bici_1,group_folder_id)

    grupo_bici_2 = data[
                    (data[u'p180 41. \xbfEst\xe1 considerando utilizar un modo de transporte diferente al que ya utiliza?'] == 'Sí'.encode('utf-8'))
                    & (data[u'p165 42. Si respondi\xf3 "S\xed" en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bicicleta')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'] != 'Bicicleta')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'] != 'Bicicleta')
                    ]
    if len(grupo_bici_2) > 0:
        file_name = nombre_empresa+'-grupo_bici_2'
        insertar_mapa(file_name,grupo_bici_2,group_folder_id)
            
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
                    
    if len(grupo_bici_3) > 0:
        file_name = nombre_empresa+'-grupo_bici_3'
        insertar_mapa(file_name,grupo_bici_3,group_folder_id)
        
    grupo_bici_4 = data[
                    (data[u'p145 55. Si su empresa ofrecer\xeda siguientes incentivos \xbfusted estar\xeda dispuesto a usar la bicicleta (o usarla con m\xe1s frecuencia)?. Biciletas p\xfablicas'] == 'Sí'.encode('utf-8'))
                    & (data[u'p145 55. Si su empresa ofrecer\xeda siguientes incentivos \xbfusted estar\xeda dispuesto a usar la bicicleta (o usarla con m\xe1s frecuencia)?. D\xeda libre en la semana'] == 'Sí'.encode('utf-8'))
                    & (data[u'p145 55. Si su empresa ofrecer\xeda siguientes incentivos \xbfusted estar\xeda dispuesto a usar la bicicleta (o usarla con m\xe1s frecuencia)?. Duchas y biciparqueaderos'] == 'Sí'.encode('utf-8'))
                    & (data[u'p145 55. Si su empresa ofrecer\xeda siguientes incentivos \xbfusted estar\xeda dispuesto a usar la bicicleta (o usarla con m\xe1s frecuencia)?. incentivos monetarios'] == 'Sí'.encode('utf-8'))
                    ]
                    
    if len(grupo_bici_4) > 0:
        file_name = nombre_empresa+'-grupo_bici_4'
        insertar_mapa(file_name,grupo_bici_4,group_folder_id)
        
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
                    & (data[u'p180 41. \xbfEst\xe1 considerando utilizar un modo de transporte diferente al que ya utiliza?'] == 'Sí'.encode('utf-8'))
                    & 
                    ((data[u'p165 42. Si respondi\xf3 "S\xed" en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bus/Buseta/Microbus/Bus intermunicipal')   
                    | (data[u'p165 42. Si respondi\xf3 "S\xed" en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Metro/Metroplus/Integrados/Tranvia/Ruta con tarifa integrada')  
                    | (data[u'p165 42. Si respondi\xf3 "S\xed" en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bus/Buseta/Bus/Buseta/Microbus/Bus intermunicipal')  )
                    # Hora de entrada al trabajo
                    # Hora de salida al trabajo
                    ]
    if len(grupo_tp_1) > 0:
        file_name = nombre_empresa+'-grupo_tp_1'
        insertar_mapa(file_name,grupo_tp_1,group_folder_id)       
        
    grupo_tp_2 = data[
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
                    & (data[u'p180 41. \xbfEst\xe1 considerando utilizar un modo de transporte diferente al que ya utiliza?'] == 'Sí'.encode('utf-8'))
                    & 
                    ((data[u'p165 42. Si respondi\xf3 "S\xed" en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bus/Buseta/Microbus/Bus intermunicipal')   
                    | (data[u'p165 42. Si respondi\xf3 "S\xed" en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Metro/Metroplus/Integrados/Tranvia/Ruta con tarifa integrada')  
                    | (data[u'p165 42. Si respondi\xf3 "S\xed" en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bus/Buseta/Bus/Buseta/Microbus/Bus intermunicipal')  )
                    # Hora de entrada al trabajo
                    # Hora de salida al trabajo
                    ]
    if len(grupo_tp_2) > 0:
        file_name = nombre_empresa+'-grupo_tp_2'
        insertar_mapa(file_name,grupo_tp_2,group_folder_id)   
        
    grupo_tp_3 = data[
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
                    & (data[u'p180 41. \xbfEst\xe1 considerando utilizar un modo de transporte diferente al que ya utiliza?'] == 'Sí'.encode('utf-8'))
                    & 
                    ((data[u'p165 42. Si respondi\xf3 "S\xed" en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bus/Buseta/Microbus/Bus intermunicipal')   
                    | (data[u'p165 42. Si respondi\xf3 "S\xed" en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Metro/Metroplus/Integrados/Tranvia/Ruta con tarifa integrada')  
                    | (data[u'p165 42. Si respondi\xf3 "S\xed" en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bus/Buseta/Bus/Buseta/Microbus/Bus intermunicipal')  )
                    # Hora de entrada al trabajo
                    # Hora de salida al trabajo
                    ]
                    
    if len(grupo_tp_3) > 0:
        file_name = nombre_empresa+'-grupo_tp_3'
        insertar_mapa(file_name,grupo_tp_3,group_folder_id) 
    
    grupo_tp_4 = data[
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
                & (data[u'p180 41. \xbfEst\xe1 considerando utilizar un modo de transporte diferente al que ya utiliza?'] == 'Sí'.encode('utf-8'))
                & 
                ((data[u'p165 42. Si respondi\xf3 "S\xed" en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bus/Buseta/Microbus/Bus intermunicipal')   
                | (data[u'p165 42. Si respondi\xf3 "S\xed" en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Metro/Metroplus/Integrados/Tranvia/Ruta con tarifa integrada')  
                | (data[u'p165 42. Si respondi\xf3 "S\xed" en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bus/Buseta/Bus/Buseta/Microbus/Bus intermunicipal')  )
                # Hora de entrada al trabajo
                # Hora de salida al trabajo
                ]
    if len(grupo_tp_4) > 0:
        file_name = nombre_empresa+'-grupo_tp_4'
        insertar_mapa(file_name,grupo_tp_4,group_folder_id) 
                    
#==============================================================================
#     grupo_peaton_1 = data
#     if len(grupo_peaton_1) > 0:
#         file_name = nombre_empresa+'-grupo_peaton_1'
#         insertar_mapa(file_name,grupo_peaton_1,group_folder_id) 
#     
#     grupo_peaton_2 = data
#     if len(grupo_peaton_2) > 0:
#         file_name = nombre_empresa+'-grupo_peaton_2'
#         insertar_mapa(file_name,grupo_peaton_2,group_folder_id) 
#     
#     grupo_peaton_3 = data
#     if len(grupo_peaton_3) > 0:
#         file_name = nombre_empresa+'-grupo_peaton_3'
#         insertar_mapa(file_name,grupo_peaton_3,group_folder_id) 
#==============================================================================
        
    grupo_cc_1 = data[((data[u'p75 52. Si usted NO va en carro ni moto para ir al trabajo (ni comparte carro desde ya) \xbfestar\xeda dispuesto a hacer parte de rutas de carro compartido, a cambio de aportar colectivamente para gasolina/parqueo?'] == 'Sí'.encode('utf-8'))
                        | (data[u'p75 52. Si usted NO va en carro ni moto para ir al trabajo (ni comparte carro desde ya) \xbfestar\xeda dispuesto a hacer parte de rutas de carro compartido, a cambio de aportar colectivamente para gasolina/parqueo?'] == 'Tendría que saber más'.encode('utf-8')))]
    if len(grupo_cc_1) > 0:
        file_name = nombre_empresa+'-grupo_cc_1'
        insertar_mapa(file_name,grupo_cc_1,group_folder_id)    
    
    grupo_cc_2 = data[(data[u'p74 \xbfPodr\xeda y estar\xeda dispuesto a recoger personas en su carro de acuerdo a una ruta compartida?']=='Si')
                        | (data[u'p74 \xbfPodr\xeda y estar\xeda dispuesto a recoger personas en su carro de acuerdo a una ruta compartida?']=='Sí'.encode('utf-8'))]
    if len(grupo_cc_2) > 0:
        file_name = nombre_empresa+'-grupo_cc_2'
        insertar_mapa(file_name,grupo_cc_2,group_folder_id) 
#==============================================================================
#         
#     grupo_hf = data
#     if len(grupo_hf) > 0:
#         file_name = nombre_empresa+'-grupo_hf'
#         insertar_mapa(file_name,grupo_hf,group_folder_id) 
#==============================================================================
    
    grupo_teletrabajo = data[data[u'p32 44. Teletrabajo']=='Sí'.encode('utf-8')]
    if len(grupo_teletrabajo) > 0:
        file_name = nombre_empresa+'-grupo_teletrabajo'
        insertar_mapa(file_name,grupo_teletrabajo,group_folder_id) 
        

