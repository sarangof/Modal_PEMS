#!/home/saf537/anaconda2/lib/python2.7/
# -*- coding: utf-8 -*-

import pandas as pd
from  datetime import datetime
from drive_functions import insert_file,check_duplicate_files, find_parent_id, load_file, update_file
import requests
import json
import re
import numpy as np

googleKey = 'AIzaSyBvuKUfCCTNzc8etkAuaU-16uzl3N4f6Vw' # Google Maps API for georeferencing

def create_keys(dct,indexer,content):
    """
    Checks if the key "indexer" is in dictionary "dct"
    Appends "content" to that key or creates key.
    """
    if indexer in dct.keys():
        dct[indexer].append(content)
    else:
        dct[indexer] = [content]
    return dct
    

"""
for k in answer.keys():
content = answer[k]
indexer = 'p'+str(questions)+'_'+text+str(k)
if indexer in dct.keys():
dct[indexer].append(content)
else:
dct[indexer] = [content]
"""

def fill_empty_answer(answer):
    content = None
    if answer == unicode('') or answer == [unicode('')]:
        content = np.nan
    return content

def submission_to_dict(submission,googleKey=googleKey):
    """
    Creates a simple dictionary from the submission.
    Keys: questions
    Values: answers
    """
    dct = {}
    for replies in submission:
        dict_bool = False
        for questions in replies['answers']:
            text   = replies['answers'][questions]['text']
            tp = replies['answers'][questions]['type']
            try:
                answer = int(replies['answers'][questions]['answer'])
            except (ValueError, TypeError):
                answer = replies['answers'][questions]['answer']
            except KeyError:
                answer = np.nan
            try:
                content = fill_empty_answer(answer)
                if tp == 'control_matrix':
                    if content == None:
                        content = answer
                        dict_bool = True
                elif tp == 'control_fullname':
                    if content == None:
                        content = " ".join([answer['first'],answer['middle'],answer['last']])
                elif tp == 'control_address':
                    if content == None:
                        dr = answer['addr_line1']
                        direc = '+'.join(re.findall(r"[\w']+",dr))
                        munici = replies['answers']['22']['answer']
                        call = 'https://maps.googleapis.com/maps/api/geocode/json?address='+direc+'+'+munici+'+'+'+Colombia'+'&key='+googleKey
                        request = requests.get(call)
                        
                        d = json.loads(request.content)
                        if d['status']=='OK':
                            lon,lat = d['results'][0]['geometry']['location']['lng'],d['results'][0]['geometry']['location']['lat']
                        else:
                            lon,lat = 'NA','NA'
                        content = (lon,lat)
                elif tp in ['control_dropdown','control_textbox','control_spinner','control_scale','control_number','control_radio']:
                    if content == None:
                        content = answer
                elif tp == 'control_datetime':
                    if content == None:
                        text = 'Edad'
                        b = datetime.strptime(answer['day']+answer['month']+answer['year'],'%d%M%Y')
                        a = datetime.now()  
                        content = (a-b).days/365.
                elif tp == 'control_time':
                    if content == None:
                        content = datetime.strptime(answer['hourSelect']+answer['minuteSelect']+answer['ampm'],'%H%M%p')
                else:
                    content = np.nan   
                if dict_bool:
                    try:
                        for k in answer.keys():
                            content = answer[k]
                            indexer = 'p'+str(questions)+' '+text+'. '+str(k)+''
                            if indexer in dct.keys():
                                dct[indexer].append(content)
                            else:
                                dct[indexer] = [content]
                        dict_bool = False
                    except AttributeError: # not sure if this is the right error
                        dict_bool = False
                        content = np.nan
                        if 'p'+str(questions)+' '+text in dct.keys():
                            dct['p'+str(questions)+' '+text].append(content)
                        else:
                            dct['p'+str(questions)+' '+text] = [content]
                else:
                    if 'p'+str(questions)+' '+text in dct.keys():
                        dct['p'+str(questions)+' '+text].append(content)
                    else:
                        dct['p'+str(questions)+' '+text] = [content]
                # HAVE TWO TYPES OF CONTENT: a list and an element   
                # Use a boolean
                    

            except KeyError:
                continue
    return dct

def update_main_db(data,folder_id):
    """
    Function that decides how and where to create or update the aggregated data base for all companies.
    """
    try: 
        new_ag_db = pd.read_csv('BDD_PEMS_agregada.csv',index_col='p8 2. Número de cédula').join(data, how='outer',rsuffix='_b')
        filter_col = [col for col in list(new_ag_db) if col.endswith('_b')==False]
        new_ag_db = new_ag_db[filter_col]
        new_ag_db.to_csv('BDD_PEMS_agregada.csv')
    except IOError:
        data.to_csv('BDD_PEMS_agregada.csv')
    if check_duplicate_files('BDD_PEMS_agregada.csv',folder_id)[0]==False:
        insert_file('BDD_PEMS_agregada.csv',
                    'Base de datos agregada. Toma la ultima respuesta por numero de cedula.', 
                    '0B3D2VjgtkabkSVh4d0I2RzZ0LWc', 'BDD_PEMS_agregada.csv') 
    else:
        update_file('BDD_PEMS_agregada.csv',
            'Base de datos agregada. Toma la ultima respuesta por numero de cedula.', 
            '0B3D2VjgtkabkSVh4d0I2RzZ0LWc', 'BDD_PEMS_agregada.csv') 
            

def create_db(long_submission,short_submission,sample_id,name):
    """
    Creates a pandas data frame that includes both surveys and exports it to Google Drive.
    """

    # This will have to change when everything is unified
    emissions_mode = {u'Bus/Buseta/Bus/Buseta/Microbus/Bus intermunicipal': 0.00018,
                      u'Bus/Buseta/Microbus/Bus intermunicipal': 0.00018,
                    u'Metro/Metroplus/Integrados/Tranvia/Ruta con tarifa integrada': 0.00010,
                    u'Taxi/Taxi colectivo Vehículo compartido pertenenciente a la empresa/entidad Vehículo privado perteneciente a la empresa/entidad': 0.00083903045,
                     u'Taxi/Taxi colectivo':  0.00083903045,
                     u'Vehículo compartido pertenenciente a la empresa/entidad': 0.00083903045,
                     u'Veh\xedculo privado perteneciente a la empresa/entidad': 0.00083903045,
                    u'Auto (Conductor o Acompañante)': 0.00083903045,
                    u'Moto (Conductor o Acompañante)': 0.0007393045,
                    u'Bicicleta': 0.000021,
                    u'A pie': 0.000005,
                    u'A pie\u201d': 0.000005,
                    u'A Pie': 0.000005
                    }
                    # Dividir por occupancy rate?.    
    
    sample_list = load_file(sample_id)
    filename = str(name)+'.csv'
    title, description = filename, 'BDD '+str(name)+'.'
    folder_id = find_parent_id(name)
    if check_duplicate_files('cedulas-'+name+'.csv',folder_id)[0]==True:
        data_long = pd.DataFrame([]).from_dict(submission_to_dict(long_submission))
        data_short = pd.DataFrame([]).from_dict(submission_to_dict(short_submission))                 
        data = pd.concat([data_short,data_long])
        data = data.set_index(u'p8 2. Número de cédula') 
        
        # Create a variable that accounts for terrain elevation
        elevation_list = []
        distance_list = []
        for pair in data[u'p9 6. Dirección'] :
            try:
                lon1,lat1 = pair
                lat2,lon2 = '6.2430', '-75.5715'
                path = str(lat1)+','+str(lon1)+'|'+lat2+','+lon2
                call_topo = 'https://maps.googleapis.com/maps/api/elevation/json?locations='+path+'&path='+path+'&samples=5&key='+googleKey
                call_dist = 'https://maps.googleapis.com/maps/api/distancematrix/json?origins='+str(lat1)+','+str(lon1)+'&destinations='+lat2+','+lon2+'&key='+googleKey
                d_topo = json.loads(requests.get(call_topo).content) 
                d_dist = json.loads(requests.get(call_dist).content) 
                if d_topo['status'] == 'OK':
                    ele_dots = [punto['elevation'] for punto in d_topo['results']]
                    temp_list = np.array(ele_dots+ele_dots[-1:]) -  np.array(ele_dots[:1]+ele_dots) 
                    elevation_list.append(float(np.abs(temp_list).sum()/4.))
                if d_dist['status'] == 'OK': 
                    distance_list.append(float(d_dist['rows'][0]['elements'][0]['distance']['value']))
            except (TypeError, KeyError) as e:
                elevation_list.append(np.nan)
                distance_list.append(np.nan)
        data['Pendiente'] = elevation_list
        data['Distancia'] = distance_list
        emissions_list = [emissions_mode[unicode(element)] for element in data[u'p68 33. ¿Cuál es su medio habitual (más frecuente y que utiliza por más tiempo en cada viaje) para regresar del trabajo?']]
        data['Emisiones'] = emissions_list*data.Distancia
       # Create DB file and insert it to Drive                 
        data.to_csv(filename)
        update_main_db(data,folder_id)
        insert_file(title, description, folder_id, filename) 
        
        # Calculate percentage of match and report it on a file.
        match = 200.0 * len(set(sample_list) & set(data_long[u'p8 2. Número de cédula'])) / (
                len(sample_list) + len(data_long[u'p8 2. Número de cédula']))
        with open('Detalles-muestreo.csv', "w") as text_file:
            text_file.write('Porcentaje de encuesta larga completada: '+str(float(match)))
            description = 'Detalles sobre el muestreo.'
        insert_file('Detalles-muestreo', description, folder_id,'Detalles-muestreo.csv')  
        
        return data, folder_id        
    else:
        with open(filename, "w") as text_file:
            text_file.write('No hay muestra generada para esta empresa')
        insert_file(title, description, folder_id, filename) 
        return None

