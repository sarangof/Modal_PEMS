import pandas as pd
from jotform import JotformAPIClient

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
            type_.append(replies['answers'][questions]['type'])
            answer = replies['answers'][questions]['answer']
            if text in dct.keys():
                #print str(text.encode("utf-8"))
                dct[text].append(answer)
            else:
                dct[text] = [answer]
        except KeyError:
            continue
        
    
print(set(type_))

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
