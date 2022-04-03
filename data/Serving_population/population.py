## When we call this script we get two csv files - updated population for each county and 
## for each health institute the sum of population and area they cover

## It has to be done manually


import requests
import csv 
import pandas as pd

def call(this):
  r = requests.post('https://pxweb.stat.si:443/SiStatData/api/v1/sl/Data/05C4010S.px', json=
  {
    "query": [
      {
        "code": "OBČINE",
        "selection": {
          "filter": "all",
          "values": [ "*" ]
        }
      },
      {
        "code": "MERITVE",
        "selection": {
          "filter": "item",
          "values": [
            "1"
          ]
        }
      },
      {
        "code": "POLLETJE",
        "selection": {
          "filter": "item",
          "values": [
            this
          ]
        }
      }
    ],
    "response": {
      "format": "json-stat"
    }
  }
  )
  return r


# this should cover calls untill the end of 2025
this = ["2025H2", "2025H1", "2024H2", "2024H1", "2023H2", "2023H1", "2022H2", "2022H1", "2021H2"]
for year in this:
  r = call(year)
  # print(r.status_code)
  if r.status_code == 200:
    dataset = r.json()
    break

# r = call("2022H2")

# print(f"Status Code: {r.status_code}, Response: {r.json()}")

dataset = r.json()
values = dataset['dataset']['value']
labels = dataset['dataset']['dimension']['OBČINE']['category']['label']
switch_labels = dict([(value, int(key)) for key, value in labels.items()])

# get the population for each county and save it into dictionary
result, counter = dict(), 0
for key in switch_labels: 
  result[key] = values[counter]
  counter += 1

df = pd.read_csv("data/population/preb.csv", sep=',',encoding='utf8')
df['index'] = df['obcina'].map(switch_labels)

# we update the number of citizens with the values from the request
df['st_preb'] = df['obcina'].map(result)

preb = df[["obcina", "enota_nmp", "povrsina", "st_preb"]]

# we write this to csv and to xlsx
preb.to_csv("data/population/preb.csv", index = False, sep=',', encoding='utf8')
preb.to_excel("data/population/preb.xlsx", index=False)

zd = df[["obcina", "enota_nmp", "povrsina"]]

povrsine = dict()
for i in range(len(zd)):
  obcina = zd.loc[i][0]
  povrsine[obcina] = zd.loc[i][2]

enote_nmp = dict()
for i in range(len(zd)):
  nmp = zd.loc[i][1]
  if nmp not in enote_nmp:
    enote_nmp[nmp] = [zd.loc[i][0]] # save the name of the county
  else:
    enote_nmp[nmp].append(zd.loc[i][0])

nmp_st = dict()
nmp_povrsina = dict()
for enota in enote_nmp:
  obcine = enote_nmp[enota]
  st, pov = 0, 0
  for obcina in obcine:
    st += result[obcina]
    p = povrsine[obcina]
    # p = p.replace(",", ".")
    pov += float(p)
  nmp_st[enota] = st
  nmp_povrsina[enota] = pov

final = []
for enota in enote_nmp:
  d = {"zd": enota, "st": nmp_st[enota], "povrsina": nmp_povrsina[enota]}
  final.append(d)

fields = ['zd', 'st', 'povrsina'] 
    
# writing to csv file 
with open("data/population/enote_nmp.csv", 'w', encoding="utf-8") as csvfile: 
    writer = csv.DictWriter(csvfile, fieldnames = fields, lineterminator = '\n') 
    writer.writeheader() 
    writer.writerows(final) 

# convert to excel
# pip install openpyxl
df_new = pd.read_csv('data/population/enote_nmp.csv')
df_new.to_excel('data/population/enote_nmp.xlsx', index=False)
    
