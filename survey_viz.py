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
type_ = []
for replies in submission:
    for questions in replies['answers']:
        try:
            text   = replies['answers'][questions]['text']
            tp = replies['answers'][questions]['type']
            type_.append(tp)
            answer = replies['answers'][questions]['answer']
            if tp == 'control_matrix':
                content = pd.DataFrame([]).from_dict(answer,orient='index')
            elif tp == 'control_fullname':
                "-".join([answer['first'],answer['middle'],answer['last']])
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



#data = pd.DataFrame([]).from_dict(dct,orient='index')


    #for form in forms:
    #    print form["title"]

#if __name__ == "__main__":
#    main()

# Read obtained file


# Clean data set


# 
