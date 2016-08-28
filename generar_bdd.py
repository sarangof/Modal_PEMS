#!/usr/bin/python
# -*- coding: utf-8 -*-

import pandas as pd
import seaborn as sns
from jotform import JotformAPIClient
from  datetime import datetime
import matplotlib.pyplot as plt
from drive_functions import insert_folder,insert_file,check_duplicate_files
import requests
import json
import re

# Google Maps API for georeferencing
googleKey = 'AIzaSyBvuKUfCCTNzc8etkAuaU-16uzl3N4f6Vw'

def create_db(submission,name):
    
    # Fill out a dictionary with the right formats for each answer
    dct = {}
    #plot_list = []
    for replies in submission:
        for questions in replies['answers']:
            text   = replies['answers'][questions]['text']
            tp = replies['answers'][questions]['type']
            try:
                answer = replies['answers'][questions]['answer']
            except KeyError:
                answer = 'NA'
            try:
                if tp == 'control_matrix':
                    #print answer
                    content = answer
                elif tp == 'control_fullname':
                    content = " ".join([answer['first'],answer['middle'],answer['last']])
                elif tp == 'control_address':
                    dr = answer['addr_line1']
                    direc = '+'.join(re.findall(r"[\w']+",dr))
                    munici = replies['answers']['22']['answer']
                    #add = '1600+Amphitheatre+Parkway,+Mountain+View,+CA'
                    call = 'https://maps.googleapis.com/maps/api/geocode/json?address='+direc+'+'+munici+'+'+'+Colombia'+'&key='+googleKey
                    request = requests.get(call)
                    
                    d = json.loads(request.content)
                    if d['status']=='OK':
                        lon,lat = d['results'][0]['geometry']['location']['lng'],d['results'][0]['geometry']['location']['lat']
                    else:
                        print('api NO')
                        lon,lat = 'NA','NA'
                    content = (lon,lat)
                elif tp in ['control_dropdown','control_textbox','control_spinner','control_scale','control_number','control_radio']:
                    content = answer
                elif tp == 'control_datetime':
                    b = datetime.strptime(answer['day']+answer['month']+answer['year'],'%d%M%Y')
                    a = datetime.now()
                    content = (a-b).days/365
                elif tp == 'control_time':
                    content = datetime.strptime(answer['hourSelect']+answer['minuteSelect']+answer['ampm'],'%H%M%p')
                else:
                    #print tp
                    content = ['something is missing.']           
                if text in dct.keys():
                    dct[text].append(content)
                else:
                    dct[text] = [content]
            except KeyError:
                continue
            
    # consolidate everything into a single data frame
    data = pd.DataFrame([]).from_dict(dct)
    data = data.set_index(u'2. Número de cédula')
    data.to_csv('Files/'+str(name)+'.csv')
    parent_id = '0B3D2VjgtkabkaWdQcU9uMkhRaUk'
    duplicate, p_id = check_duplicate_files(name)
    insert_file(name,parent_id)
    return data




    

"""
plot_instructions = {u'10. Número de hijos':'bar', 
       u'11. Estado civil',
       u'12. ¿Sufre de alguna discapacidad?',
       u'13. Indique cuál es su discapacidad',
       u'14. Su discapacidad es',
       u'15. Requiere el uso de',
       u'16. Último nivel de estudios aprobados',
       u'17. ¿Actualmente cursa algún tipo de estudio? De ser así ¿a qué nivel corresponde?',
       u'18. Salario', 
       u'19. Número de sedes de su empresa en las que trabaja',
       u'20. Sedes',
       u'21. Si normalmente trabaja en más de una sede durante la semana ¿cuántos viajes hace semanalmente hacia la sede que más visita?',
       u'22. Si normalmente trabaja en más de una sede durante la semana ¿cuántos viajes hace semanalmente hacia la segunda sede que más visita?',
       u'23. Número habitual de viajes diarios (en día habil, incluyendo viajes hacia y desde su lugar de trabajo)',
       u'24. Entrada usual al trabajo',
       u'25. Salida usual del trabajo',
       u'28. ¿Es su vivienda su destino habitual después del trabajo?',
       u'29. ¿De cuántos vehículos disponen en su hogar?',
       u'3. ¿En qué empresa trabaja?',
       u'30. ¿Normalmente utiliza el mismo medio de transporte para ir al trabajo y para regresar?',
       u'31. ¿Cuál es su medio habitual (más frecuente) para ir al trabajo?',
       u'32. ¿Cuál es su medio habitual (más frecuente) para regresar del trabajo?',
       u'33. ¿Con qué frecuencia utiliza los siguientes medios de transporte en una semana promedio para ir al trabajo?',
       u'34. ¿Con qué frecuencia utiliza los siguientes medios de transporte para regresar del trabajo?',
       u'35. Si realiza viajes entre sedes durante el día, ¿con qué frecuencia utiliza los siguientes medios de transporte?',
       u'36. ¿Combina su medio de transporte principal con algún otro medio (por más de 5 minutos)?',
       u'37. Si respondió "Sí" en la pregunta anterior ¿qué modo de transporte utiliza en ese caso?',
       u'38. ¿Utiliza de vez en cuándo otro medio de transporte para ir al trabajo?',
       u'39. Si respondió "Sí" en la pregunta anterior ¿qué modo de transporte utiliza en ese caso?',
       u'4. ¿En qué municipio vive?',
       u'40. ¿Qué tan sencillo le es transportarse hacia la empresa?',
       u'41. ¿Cuánto tiempo se demora para llegar al trabajo?',
       u'42. ¿Cuánto tiempo se demora para regresar del trabajo a su casa?',
       u'43. ¿Qué tan satisfecho está con la facilidad para acceder a la empresa?',
       u'44. ¿Qué tan satisfecho está con su tiempo de desplazamiento al trabajo?',
       u'45. ¿Cuál cree que es la principal razón por la que usted puede tener problemas de desplazamiento hacia su trabajo?',
       u'46. Teletrabajo', 
       u'47. Teletrabajo - frecuencia',
       u'48. En general ¿cuánto le interesaría utilizar cada uno de los siguientes medios? 1 no le interesa, 3 interés promedio, 5 le interesa mucho.',
       u'49. Ordene qué modos de transporte le interesaría más usar si las condiciones se dieran. 1 es el que más le interesa y 10 es el que menos le interesa.',
       u'5. Dirección',
       u'50. ¿Hasta qué punto valoraría que su empresa promueva la bicicleta como medio de transporte?',
       u'51. Si usted NO utiliza el bus como medio de transporte principal, ¿Qué condición se debería dar para que usted decidiera utilizar el bus como medio de transporte o para utilizarlo con más frecuencia? Seleccione la opción que más importante le parezca',
       u'52. Si usted NO utiliza el sistema metro como medio de transporte principal, ¿Qué condición se debería dar para que usted decidiera utilizarlo como medio de transporte o para utilizarlo con más frecuencia? Seleccione la opción que más importante le parezca',
       u'53. Si usted NO utiliza la bicicleta como medio de transporte principal, ¿Qué condición se debería dar para que usted decidiera utilizar  la bicicleta como medio de transporte o para utilizarla con más frecuencia? Seleccione la opción que más importante le parezca',
       u'54. Si usted NO maneja carro ni moto para ir al trabajo (ni comparte carro desde ya) ¿estaría dispuesto a hacer parte de rutas de carro compartido, a cambio de aportar colectivamente para gasolina/parqueo?',
       u'55. Si las condiciones fueran apropiadas ¿qué tan dispuesto estaría a cambiar de modo de transporte?',
       u'56. Si hubiera una ruta guiada de bicicletas que pasara por su casa hacia el trabajo ¿consideraría la opción de utilizar este modo con más frecuencia?',
       u'6. Comuna', 
       u'7. Estrato',
       u'8. Número de personas que habitualmente viven en su hogar',
       u'9. Fecha de nacimiento',
       u'¿Podría y estaría dispuesto a recoger personas en su carro de acuerdo a una ruta compartida?'

}

question_type = {'barplot_simple'}

"""

# Interesting plots


