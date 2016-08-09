import pandas as pd
from jotform import JotformAPIClient

# API call, import, etc
myKey = '33dcf578e3523959b282e1bebff1f581'

#def main():

#jotformAPIClient = JotformAPIClient(myKey)
#submission_filter = {"form_id":"62214117688154"}
#submission = jotformAPIClient.get_submissions(filterArray=submission_filter) 

dct = {}
for replies in submission:
    for questions in replies['answers']:
        print 
        text = replies['answers'][questions]['text']
        answer = replies['answers'][questions]['answer']
        dct[text]=answer
        

data = pd.DataFrame([]).from_dict(dct,orient='index')

    #for form in forms:
    #    print form["title"]

#if __name__ == "__main__":
#    main()

# Read obtained file


# Clean data set


# 
