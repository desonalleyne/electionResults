import requests
import lxml.html as lh
import pandas as pd
import matplotlib.pyplot as plt
from math import floor
from messenger import Messenger


messenger = Messenger()

def findText(element, text):
    out = []
    for t in element:
        if text in t.text_content():
            out.append(t.text_content())
    return out

# Scrape data from SN
url = "https://www.stabroeknews.com/2020/03/03/news/guyana/guyana-elections-results-2020-gecom-preliminary/"
page = requests.get(url)
doc = lh.fromstring(page.content)

# extract metadata
span = doc.xpath('//span')
lastUpdated = findText(span, 'Last update')

em = doc.xpath('//em')
pollingStations = findText(em,'2,339 polling stations')

# build polling station data
stations = []
for s in pollingStations:
    stationsCounted = {}
    cnt = int(s.split(" ")[0])
    ratio = str(floor((cnt / 2339) * 100)) + "%"
    stationsCounted['cnt'] = cnt
    stationsCounted['ratio'] = ratio
    stationsCounted['text'] = s
    stationsCounted['available'] = 2339
    stations.append(stationsCounted)

# extract poll results
tr_elements = doc.xpath('//tr')

col = []
i = 0
# for each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i += 1
    name = t.text_content()
    #print('{}: {}'.format(i,name))
    col.append((name,[]))

# since our first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    #print(len(T))
    
    #If row is not of size 12, the //tr data is not from our table 
    if len(T)!=12:
        pass
        break
        td = lh.Element("td")
        td.text = "0"
        T.insert(5,td)

    i=0
    # iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content() 
        # check if row is empty
        if i>0:
        # convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        # append the data to the empty list of the i'th column
        col[i][1].append(data)
        # increment i for the next column
        i+=1

# build results dict
results = []
for x in col[1:]:
    p= {}
    p['party'] = x[0]
    p['partyTotal'] = (x[1][10])
    p['partyPct'] = str((p['partyTotal'] / col[11][1][10])*100)[:4] + "%"
    results.append(p)
body = ""
header = "EBot says: \nHere's an update on the election results..."
for r in sorted(results[:-1],key=lambda i: (i['partyTotal']),reverse=True):
    body = body + "\n{0} - {1} votes ({2})".format(r['party'],r['partyTotal'],r['partyPct'])
footer = "\n".join([
        "\n",
        "{0} of {1} polling stations ({2})".format(stations[0]['cnt'], stations[0]['available'], stations[0]['ratio']),
        "Last updated: {0}".format(lastUpdated[0].split(" ")[2].split(".")[0]),
        "Source: www.stabroeknews.com"
        ])
messenger.send("user","\n".join([header,body,footer]))
messenger.logout()
