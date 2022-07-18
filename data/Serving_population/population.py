## When we call this script we get two csv files - updated population for each county and 
## for each health institute the sum of population and area they cover

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
# this = ["2025H2", "2025H1", "2024H2", "2024H1", "2023H2", "2023H1", "2022H2", "2022H1", "2021H2"]
# for year in this:
#   r = call(year)
#   # print(r.status_code)
#   if r.status_code == 200:
#     dataset = r.json()
#     break

# current table has the following form: str(year) + 'H' + str(i) where i is 1 if it's the first half of the year or 2 of it's the second

def check_year(year):
  "Checks if there's data available for table str(year) + 'H' + str(i)"
  r = call(year)
  return r.status_code == 200

# we start with year 2022H1
year = 2022
currently = str(year) + "H1"
cont = True
while cont:
  last = currently
  
  if currently[-1] == "1": # if the last digit is 1 and data is available try replacing it with 2
    currently = currently[:-1] + "2"
    cont = check_year(currently) 
    if cont: # if data is also available += 1 year
      last = currently
      
      year += 1
      currently = str(year) + "H1"
      cont = check_year(currently)

r = call(last)
dataset = r.json()


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

df = pd.read_csv("OHCA-registry-Slovenia\data\population\population.csv", sep=',', encoding='utf-8')
df['index'] = df['obcina'].map(switch_labels)

# we update the number of citizens with the values from the request
df['st_preb'] = df['obcina'].map(result)

preb = df[["obcina", "enota_nmp", "povrsina", "st_preb"]]

# we write this to csv and to xlsx
preb.to_csv("OHCA-registry-Slovenia\data\population\population.csv", index = False, sep=',', encoding='utf-8')
preb.to_excel("OHCA-registry-Slovenia\data\population\population.xlsx", index=False)


zd = df[["obcina", "enota_nmp", "povrsina"]]

# for every municipality save the area into dictionary
povrsine = dict()
for i in range(len(zd)):
  obcina = zd.loc[i][0]
  povrsine[obcina] = zd.loc[i][2]

# for every hospital save all the municipalities it covers
enote_nmp = dict()
for i in range(len(zd)):
  nmp = zd.loc[i][1]
  if nmp[-1] == " ":
    nmp = nmp[:-1]
  if nmp not in enote_nmp:
    enote_nmp[nmp] = [zd.loc[i][0]] # save the name of the municipality
  else:
    enote_nmp[nmp].append(zd.loc[i][0])

# for every hospital calculate the are and # of people it covers
nmp_st = dict()
nmp_povrsina = dict()
for enota in enote_nmp:
  obcine = enote_nmp[enota] # all the municipalities covered by this hospital
  st, pov = 0, 0
  for obcina in obcine:
    st += result[obcina]
    p = povrsine[obcina]
    pov += round(float(p), 2)
  nmp_st[enota] = st
  nmp_povrsina[enota] = pov

final = []
for enota in enote_nmp:
  d = {"zd": enota, "st": nmp_st[enota], "povrsina": round(nmp_povrsina[enota], 3)}
  final.append(d)

final = sorted(final, key=lambda k: k["zd"])

fields = ['zd', 'st', 'povrsina'] 
    
# writing to csv file 
with open("OHCA-registry-Slovenia\data\population\hospitals.csv", 'w', encoding="utf-8") as csvfile: 
    writer = csv.DictWriter(csvfile, fieldnames = fields, lineterminator = '\n') 
    writer.writeheader() 
    writer.writerows(final) 

# convert to excel
# pip install openpyxl
df_new = pd.read_csv("OHCA-registry-Slovenia\data\population\hospitals.csv")
df_new.to_excel("OHCA-registry-Slovenia\data\population\hospitals.xlsx", index=False)


def extract():
  "Extracts population for municipalities and hospitals from created files."
  municipalities, hospitals = dict(), dict()
  with open("OHCA-registry-Slovenia\data\population\hospitals.csv", 'r', encoding="utf-8") as csvfile: 
    reader = csv.reader(csvfile)
    counter = 0
    for line in reader:
      if counter > 0:
        hospitals[line[0]] = line[1]
      counter += 1

  with open("OHCA-registry-Slovenia\data\population\population.csv", 'r', encoding="utf-8") as csvfile: 
    reader = csv.reader(csvfile)
    counter = 0
    for line in reader:
      if counter > 0:
        municipalities[line[0]] = line[-1]
      counter += 1

  return (municipalities, hospitals)

    
