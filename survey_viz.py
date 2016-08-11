import pandas as pd
import seaborn as sns
from jotform import JotformAPIClient
from  datetime import datetime

# API call, import, etc
myKey = '33dcf578e3523959b282e1bebff1f581'

#def main():

jotformAPIClient = JotformAPIClient(myKey)
submission_filter = {"form_id":"62214117688154"}
submission = jotformAPIClient.get_submissions(filterArray=submission_filter) 

dct = {}
plot_list = []
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
                #content = pd.DataFrame([]).from_dict(answer,orient='index')
                content = ''
            elif tp == 'control_fullname':
                content = " ".join([answer['first'],answer['middle'],answer['last']])
            elif tp == 'control_address':
                content = answer['addr_line1']
            elif tp in ['control_dropdown','control_textbox','control_spinner','control_scale','control_number','control_radio']:
                content = answer
            elif tp == 'control_datetime':
                b = datetime.strptime(answer['day']+answer['month']+answer['year'],'%d%M%Y')
                a = datetime.now()
                content = (a-b).days/365
            elif tp == 'control_time':
                content = datetime.strptime(answer['hourSelect']+answer['minuteSelect']+answer['ampm'],'%H%M%p')
            else:
                print tp
                content = ['something is missing.']
                
            print text
            print answer                
                
            if text in dct.keys():
                dct[text].append(content)
            else:
                dct[text] = [content]
        except KeyError:
            continue
        

"""

Types:

- control_texbox

"""



data = pd.DataFrame([]).from_dict(dct)
data = data.set_index([u'2. Número de cédula'])


    #for form in forms:
    #    print form["title"]

#if __name__ == "__main__":
#    main()

# Read obtained file


# Clean data set


# 
