import requests
import lxml.html as lh
import pandas as pd
import matplotlib.pyplot as plt


url = "https://www.stabroeknews.com/2020/03/02/news/guyana/guyana-elections-results-2020-statements-of-poll/"

page = requests.get(url)

doc = lh.fromstring(page.content)
tr_elements = doc.xpath('//tr')
# print(tr_elements)


tr_elements = doc.xpath('//tr')

# Create empty list
col = []
i = 0
# For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i += 1
    name = t.text_content()
    print('{}: {}'.format(i,name))
    col.append((name,[]))

#Since out first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    
    #If row is not of size 11, the //tr data is not from our table 
    if len(T)!=11:
        break
    
    #i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content() 
        #Check if row is empty
        if i>0:
        #Convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1


Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)
df = df.drop_duplicates()
print(len(df),'DF')
#print([len(C) for (title,C) in col])
#print(df[0:60])
df = df[(df['Division #'] != 'Division # string')]
df = df[(df['Division #'] != 'Division #')]
df['region'] = df['Division #']

df['region'] = df['region'].str[0:1]
df['region'] = pd.to_numeric(df['region'])
df['ANUG'] = pd.to_numeric(df['ANUG'])
df['APNU+AFC'] = pd.to_numeric(df['APNU+AFC'])
df['CG'] = pd.to_numeric(df['CG'])
df['LJP'] = pd.to_numeric(df['LJP'])
df['PPP/C'] = pd.to_numeric(df['PPP/C'])
df['PRP'] = pd.to_numeric(df['PRP'])
df['TCI'] = pd.to_numeric(df['TCI'])
df['TNM'] = pd.to_numeric(df['TNM'])
df['URP'] = pd.to_numeric(df['URP'])
print(df)

df.groupby('region').plot(kind='bar')

x = df.region
y = df['APNU+AFC']
plt.bar(x,y)
plt.savefig('votes.png')
#print(df.dtypes)
#df2 = DataFrame(df, columns=['APNU+AFC','PPP/C','region'])
#df2.plot(kind='bar')
#df2.savefig('votes2.png')
