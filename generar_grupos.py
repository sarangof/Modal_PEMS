#!/home/saf537/anaconda2/lib/python2.7/
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 27 15:26:47 2016

@author: saf537
"""
from drive_functions import insert_file, insert_folder
from cartodb import CartoDBAPIKey, FileImport
from generar_visualizaciones import plot_map
import requests
    
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
    grupo = grupo.reset_index()
    grupo[[u'p8 2. N\xfamero de c\xe9dula',u'p79 8. G\xe9nero',u'p12 Edad',u'p54 12. \xbfTiene alguna discapacidad?',u'p27 18. Sedes',u'p81 24. \xbfTiene un horario fijo para ir al trabajo?','Emisiones','Latitude','Longitude']].to_excel('grupos/'+file_name+'.xlsx',index=False) 
    grupo[[u'p8 2. N\xfamero de c\xe9dula',u'p79 8. G\xe9nero',u'p12 Edad',u'p54 12. \xbfTiene alguna discapacidad?',u'p27 18. Sedes',u'p81 24. \xbfTiene un horario fijo para ir al trabajo?','Emisiones','Latitude','Longitude']].to_csv('grupos/'+file_name+'.csv',index=False)
    insert_file(file_name+'.csv',' ',group_folder_id, 'grupos/'+file_name+'.csv',mimetype='text/csv') 
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
        
        
        
def asignar_grupos(data, folder_id, nombre_empresa, viz_folder):
    
    """
    Asigna grupos objetivo segun las respuestas de la encuesta (del dataframe "data").
    Graba archivos en la carpeta de Drive correspodiente a "Grupos" (folder_id).
    Utiliza el nombre de la empresa como referencia (nombre_empresa).
    """
    
    group_folder_id = insert_folder(folder_id,'Grupos')
    
    # -- Personas que no montan en bicicleta pero que tienen condiciones para hacerlo.  
    grupo_bici_1 = data[(data['p12 Edad']<40.) 
                    & (data['Distancia'] < 7000) 
                    & (data[u'p15 29. \xbfDe cu\xe1ntos veh\xedculos disponen en su hogar?. Bicicletas'] > 0) 
                    & (data[u'p82 30. \xbfSabe montar en bicicleta?']=='Sí'.encode('utf-8'))
                    & (data[u'p54 12. \xbfTiene alguna discapacidad?'] =='No')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'] != 'Bicicleta')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'] != 'Bicicleta')
                    ]
                    
    if len(grupo_bici_1) > 0:
        file_name = nombre_empresa+'-grupo_bici_1'
        insertar_mapa(file_name, grupo_bici_1, group_folder_id)
        plot_map(grupo_bici_1, group_folder_id, 'Grupo bici 1')

    # -- Personas que no montan en bicicleta pero que declaran estar pensando en hacerlo.
    grupo_bici_2 = data[
                    (data[u'p180 41. \xbfEst\xe1 considerando utilizar un modo de transporte diferente al que ya utiliza?'].astype(str) == 'Sí'.encode('utf-8'))
                    & (data[u'p165 42. Si respondi\xf3 &quot;S\xed&quot; en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bicicleta')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'] != 'Bicicleta')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'] != 'Bicicleta')
                    ]
    if len(grupo_bici_2) > 0:
        file_name = nombre_empresa+'-grupo_bici_2'
        insertar_mapa(file_name,grupo_bici_2,group_folder_id)
        plot_map(grupo_bici_2, group_folder_id, 'Grupo bici 2')
            
    # -- Personas que no montan en bicicleta, podrían hacerlo y declaran interés en hacerlo.
    grupo_bici_3 = data[(data['p12 Edad']<40.) 
                    & (data['Distancia'] < 7000) 
                    & (data[u'p15 29. \xbfDe cu\xe1ntos veh\xedculos disponen en su hogar?. Bicicletas'] > 0) 
                    & (data[u'p82 30. \xbfSabe montar en bicicleta?']=='Sí'.encode('utf-8'))
                    & (data[u'p54 12. \xbfTiene alguna discapacidad?'] =='No')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'Bicicleta')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'Bicicleta')
                    & (data[u'p35 47. En general \xbfcu\xe1nto le interesar\xeda utilizar cada uno de los siguientes medios? 1 no le interesa, 3 inter\xe9s promedio, 5 le interesa mucho.. Bicicleta'] > 2.)
                    & (data[u'p180 41. \xbfEst\xe1 considerando utilizar un modo de transporte diferente al que ya utiliza?'].astype(str) == 'Sí'.encode('utf-8'))
                    & (data[u'p165 42. Si respondi\xf3 &quot;S\xed&quot; en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bicicleta')   
                    & (data[u'p45 48. ¿Hasta qué punto valoraría que su empresa promueva la bicicleta como medio de transporte?']>2.)
                    ]
                    
    if len(grupo_bici_3) > 0:
        file_name = nombre_empresa+'-grupo_bici_3'
        insertar_mapa(file_name,grupo_bici_3,group_folder_id)
        plot_map(grupo_bici_3, group_folder_id, 'Grupo bici 3')
    
    # -- Personas que no montan en bicicleta pero que consideraria hacerlo ante ciertos incentivos de la empresa.    
    grupo_bici_4 = data[(data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'Bicicleta')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'Bicicleta')
                    &((data[u'p145 55. Si su empresa ofrecer\xeda siguientes incentivos \xbfusted estar\xeda dispuesto a usar la bicicleta (o usarla con m\xe1s frecuencia)?. Biciletas p\xfablicas'] == 'Sí'.encode('utf-8')).astype(int)
                        .add((data[u'p145 55. Si su empresa ofrecer\xeda siguientes incentivos \xbfusted estar\xeda dispuesto a usar la bicicleta (o usarla con m\xe1s frecuencia)?. D\xeda libre en la semana'].astype(str) == 'Sí'.encode('utf-8')).astype(int)
                        ).add((data[u'p145 55. Si su empresa ofrecer\xeda siguientes incentivos \xbfusted estar\xeda dispuesto a usar la bicicleta (o usarla con m\xe1s frecuencia)?. Duchas y biciparqueaderos'].astype(str) == 'Sí'.encode('utf-8')).astype(int)
                        ).add((data[u'p145 55. Si su empresa ofrecer\xeda siguientes incentivos \xbfusted estar\xeda dispuesto a usar la bicicleta (o usarla con m\xe1s frecuencia)?. incentivos monetarios'].astype(str) == 'Sí'.encode('utf-8')).astype(int))
                    > 1)
                    ]
                    
    if len(grupo_bici_4) > 0:
        file_name = nombre_empresa+'-grupo_bici_4'
        insertar_mapa(file_name,grupo_bici_4,group_folder_id)
        plot_map(grupo_bici_4, group_folder_id, 'Grupo bici 4')
    

    # -- Listado de personas propensas al uso del transporte publico.    
    grupo_tp_1 = data[
                    (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'Bus/Buseta/Microbus/Bus intermunicipal')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'Metro/Metroplus/Integrados/Tranvia/Ruta con tarifa integrada')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'Bus/Buseta/Bus/Buseta/Microbus/Bus intermunicipal')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'Bicicleta')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'A pie')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'Bus/Buseta/Microbus/Bus intermunicipal')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'Metro/Metroplus/Integrados/Tranvia/Ruta con tarifa integrada')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'Bus/Buseta/Bus/Buseta/Microbus/Bus intermunicipal')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'Bicicleta')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'A pie')
                    & (data[u'p180 41. \xbfEst\xe1 considerando utilizar un modo de transporte diferente al que ya utiliza?'].astype(str) == 'Sí'.encode('utf-8'))
                    & (data[u'p65 40. ¿Qué tan sencillo le es transportarse hacia y desde la empresa?'] < 6.)
                    & (data[u'p54 12. \xbfTiene alguna discapacidad?'].astype(str) =='No')
                    & 
                    ((data[u'p165 42. Si respondi\xf3 &quot;S\xed&quot; en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bus/Buseta/Microbus/Bus intermunicipal')   
                    | (data[u'p165 42. Si respondi\xf3 &quot;S\xed&quot; en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Metro/Metroplus/Integrados/Tranvia/Ruta con tarifa integrada')  
                    | (data[u'p165 42. Si respondi\xf3 &quot;S\xed&quot; en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bus/Buseta/Bus/Buseta/Microbus/Bus intermunicipal')  )
                    # Hora de entrada al trabajo
                    # Hora de salida al trabajo
                    ]
    if len(grupo_tp_1) > 0:
        file_name = nombre_empresa+'-grupo_tp_1'
        insertar_mapa(file_name,grupo_tp_1,group_folder_id)  
        plot_map(grupo_tp_1, group_folder_id, 'Grupo Transporte Publico 1')
    
    # -- Personas que estarian dispuestas a utilizar el transporte publico.    
    grupo_tp_2 = data[
                    (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) == 'Auto (Conductor o Acompañante)')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) == 'Moto (Conductor o Acompañante)')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) == 'Auto (Conductor o Acompañante)')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) == 'Moto (Conductor o Acompañante)')
                    & (data[u'p180 41. \xbfEst\xe1 considerando utilizar un modo de transporte diferente al que ya utiliza?'].astype(str) == 'No'.encode('utf-8'))
                    & 
                    ((data[u'p165 42. Si respondi\xf3 &quot;S\xed&quot; en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bus/Buseta/Microbus/Bus intermunicipal')   
                    | (data[u'p165 42. Si respondi\xf3 &quot;S\xed&quot; en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Metro/Metroplus/Integrados/Tranvia/Ruta con tarifa integrada')  
                    | (data[u'p165 42. Si respondi\xf3 &quot;S\xed&quot; en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bus/Buseta/Bus/Buseta/Microbus/Bus intermunicipal')  )
                    # Hora de entrada al trabajo
                    # Hora de salida al trabajo
                    ]
    if len(grupo_tp_2) > 0:
        file_name = nombre_empresa+'-grupo_tp_2'
        insertar_mapa(file_name,grupo_tp_2,group_folder_id) 
        plot_map(grupo_tp_2, group_folder_id, 'Grupo Transporte Publico 2')
        
    # -- 
    grupo_tp_3 = data[
                    (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'Bus/Buseta/Microbus/Bus intermunicipal')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'Metro/Metroplus/Integrados/Tranvia/Ruta con tarifa integrada')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'Bus/Buseta/Bus/Buseta/Microbus/Bus intermunicipal')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'Bicicleta')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'A pie')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'Bus/Buseta/Microbus/Bus intermunicipal')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'Metro/Metroplus/Integrados/Tranvia/Ruta con tarifa integrada')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'Bus/Buseta/Bus/Buseta/Microbus/Bus intermunicipal')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'Bicicleta')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'A pie')
                    & (data[u'p180 41. \xbfEst\xe1 considerando utilizar un modo de transporte diferente al que ya utiliza?'].astype(str) == 'Sí'.encode('utf-8'))
                    & (data[u'p54 12. \xbfTiene alguna discapacidad?'].astype(str) =='No')
                    & 
                    ((data[u'p165 42. Si respondi\xf3 &quot;S\xed&quot; en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bus/Buseta/Microbus/Bus intermunicipal')   
                    | (data[u'p165 42. Si respondi\xf3 &quot;S\xed&quot; en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Metro/Metroplus/Integrados/Tranvia/Ruta con tarifa integrada')  
                    | (data[u'p165 42. Si respondi\xf3 &quot;S\xed&quot; en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bus/Buseta/Bus/Buseta/Microbus/Bus intermunicipal')  )
                    # Hora de entrada al trabajo
                    # Hora de salida al trabajo
                    ]
                    
    if len(grupo_tp_3) > 0:
        file_name = nombre_empresa+'-grupo_tp_3'
        insertar_mapa(file_name,grupo_tp_3,group_folder_id) 
        plot_map(grupo_tp_3, group_folder_id, 'Grupo Transporte Publico 3')
    
    # -- Porcentaje/listado de personas que podría usar el transporte público, si cambiara una o dos variables en el entorno
    grupo_tp_4 = data[
                (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'Bus/Buseta/Microbus/Bus intermunicipal')
                & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'Metro/Metroplus/Integrados/Tranvia/Ruta con tarifa integrada')
                & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'Bus/Buseta/Bus/Buseta/Microbus/Bus intermunicipal')
                & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'Bicicleta')
                & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'A pie')
                & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'Bus/Buseta/Microbus/Bus intermunicipal')
                & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'Metro/Metroplus/Integrados/Tranvia/Ruta con tarifa integrada')
                & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'Bus/Buseta/Bus/Buseta/Microbus/Bus intermunicipal')
                & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'Bicicleta')
                & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'A pie')
                & (data[u'p180 41. \xbfEst\xe1 considerando utilizar un modo de transporte diferente al que ya utiliza?'].astype(str) == 'Sí'.encode('utf-8'))
                & 
                ((data[u'p165 42. Si respondi\xf3 &quot;S\xed&quot; en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bus/Buseta/Microbus/Bus intermunicipal')   
                | (data[u'p165 42. Si respondi\xf3 &quot;S\xed&quot; en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Metro/Metroplus/Integrados/Tranvia/Ruta con tarifa integrada')  
                | (data[u'p165 42. Si respondi\xf3 &quot;S\xed&quot; en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'Bus/Buseta/Bus/Buseta/Microbus/Bus intermunicipal')  )
                # Hora de entrada al trabajo
                # Hora de salida al trabajo
                ]
    if len(grupo_tp_4) > 0:
        file_name = nombre_empresa+'-grupo_tp_4'
        insertar_mapa(file_name,grupo_tp_4,group_folder_id) 
        plot_map(grupo_tp_4, group_folder_id, 'Grupo Transporte Publico 4')
    
    # -- Personas propensas a caminar.
    grupo_peaton_1 = data[(data['Distancia'] < 3000) 
                    & (data[u'p54 12. \xbfTiene alguna discapacidad?'].astype(str) =='No')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'A Pie')
                    & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'Bicicleta')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'A Pie')
                    & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'Bicicleta')
                    & (data[u'p180 41. \xbfEst\xe1 considerando utilizar un modo de transporte diferente al que ya utiliza?'].astype(str) == 'Sí'.encode('utf-8'))
                    & (data[u'p165 42. Si respondi\xf3 &quot;S\xed&quot; en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'A pie')   
                    & (data[u'p71 38. ¿Qué tan satisfecho está con su medio de transporte usual para ir y regresar del trabajo?'] < 7.)
                    ]    
    
    if len(grupo_peaton_1) > 0:
        file_name = nombre_empresa+'-grupo_peaton_1'
        insertar_mapa(file_name,grupo_peaton_1,group_folder_id) 
        plot_map(grupo_peaton_1, group_folder_id, 'Grupo Peaton 1')
     
    # -- Personas que muestran disposicion a caminar.
    grupo_peaton_2 = data[(data[u'p180 41. \xbfEst\xe1 considerando utilizar un modo de transporte diferente al que ya utiliza?'].astype(str) == 'Sí'.encode('utf-8'))
                    & (data[u'p165 42. Si respondi\xf3 &quot;S\xed&quot; en la pregunta anterior \xbfqu\xe9 modo de transporte est\xe1 considerando usar?'].astype(str) == 'A pie')   
                    ]  
    if len(grupo_peaton_2) > 0:
        file_name = nombre_empresa+'-grupo_peaton_2'
        insertar_mapa(file_name,grupo_peaton_2,group_folder_id) 
        plot_map(grupo_peaton_2, group_folder_id, 'Grupo Peaton 2')
     
    # -- Porcentaje/Listado de las personas que podrían usar la caminata pero no lo hacen (y estan comodos asi)
    grupo_peaton_3 = data[(data['Distancia'] < 3000) 
                & (data[u'p54 12. \xbfTiene alguna discapacidad?'] =='No')
                & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'A Pie')
                & (data[u'p67 32. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para ir al trabajo?'].astype(str) != 'Bicicleta')
                & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'A Pie')
                & (data[u'p68 33. \xbfCu\xe1l es su medio habitual (m\xe1s frecuente y que utiliza por m\xe1s tiempo en cada viaje) para regresar del trabajo?'].astype(str) != 'Bicicleta')
                & (data[u'p65 40. ¿Qué tan sencillo le es transportarse hacia y desde la empresa?'] > 6.)
                & (data[u'p71 38. ¿Qué tan satisfecho está con su medio de transporte usual para ir y regresar del trabajo?'] > 6.)
                ]  
    if len(grupo_peaton_3) > 0:
        file_name = nombre_empresa+'-grupo_peaton_3'
        insertar_mapa(file_name,grupo_peaton_3,group_folder_id) 
        plot_map(grupo_peaton_3, group_folder_id, 'Grupo Peaton 1')

    # -- Personas que estarian dispuestas a hacer parte de rutas, manejando o de pasajeros (y que utilizan modos no sostenibles)
    grupo_cc_1 = data[(data[u'p74 \xbfPodr\xeda y estar\xeda dispuesto a recoger personas en su carro de acuerdo a una ruta compartida?'].astype(str)=='Si')
                    |(data[u'p74 \xbfPodr\xeda y estar\xeda dispuesto a recoger personas en su carro de acuerdo a una ruta compartida?'].astype(str)=='Sí'.encode('utf-8'))
                    |((data[u'p75 52.  ¿Estaría dispuesto a hacer parte de rutas de carro compartido, a cambio de aportar colectivamente para gasolina/parqueo?'].astype(str) == 'Sí'.encode('utf-8'))
                    & (data[u'p65 40. ¿Qué tan sencillo le es transportarse hacia y desde la empresa?'] < 5.)
                    & (data[u'p71 38. ¿Qué tan satisfecho está con su medio de transporte usual para ir y regresar del trabajo?'] < 5.))]
    if len(grupo_cc_1) > 0:
        file_name = nombre_empresa+'-grupo_cc_1'
        insertar_mapa(file_name,grupo_cc_1,group_folder_id) 
        plot_map(grupo_cc_1, group_folder_id, 'Grupo Carro Compartido 1')
    
    # -- Personas que podrian estar dispuestas a hacer parte de rutas y que estan en riesgo de cambiar a un modo no sostenible.
    grupo_cc_2 = data[(data[u'p75 52.  ¿Estaría dispuesto a hacer parte de rutas de carro compartido, a cambio de aportar colectivamente para gasolina/parqueo?'].astype(str) == 'Tendría que saber más'.encode('utf-8'))
    ]   
    if len(grupo_cc_2) > 0:
        file_name = nombre_empresa+'-grupo_cc_2'
        insertar_mapa(file_name,grupo_cc_2,group_folder_id) 
        plot_map(grupo_cc_2, group_folder_id, 'Grupo Carro Compartido 2')

#==============================================================================
#         
#     grupo_hf = data
#     if len(grupo_hf) > 0:
#         file_name = nombre_empresa+'-grupo_hf'
#         insertar_mapa(file_name,grupo_hf,group_folder_id) 
#         plot_map(grupo_hf, group_folder_id, 'Grupo Carro Compartido 2')
#==============================================================================
    
    grupo_teletrabajo = data[data[u'p32 44. Teletrabajo'].astype(str) == 'Sí'.encode('utf-8')]
    if len(grupo_teletrabajo) > 0:
        file_name = nombre_empresa+'-grupo_teletrabajo'
        insertar_mapa(file_name,grupo_teletrabajo,group_folder_id) 
        plot_map(grupo_teletrabajo, group_folder_id, 'Grupo Teletrabajo')
        
        grupo_teletrabajo = data[data[u'p32 44. Teletrabajo'].astype(str) == 'Sí'.encode('utf-8')]
    if len(grupo_teletrabajo) > 0:
        file_name = nombre_empresa+'-grupo_teletrabajo'
        insertar_mapa(file_name,grupo_teletrabajo,group_folder_id) 
        plot_map(grupo_teletrabajo, group_folder_id, 'Grupo Teletrabajo')
        

