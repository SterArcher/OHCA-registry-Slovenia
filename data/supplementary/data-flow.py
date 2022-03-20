# THIS DIAGRAM WOULD REQUIRE SOME CHANGES IF WE DECIDE TO USE IT

import plotly.graph_objects as go
import csv
import pandas as pd
import random

with open("data.csv", 'r',encoding='utf8') as csvfile:
    csvreader = csv.reader(csvfile)
    all_rows = []
    for row in csvreader:
        row[0] = row[0].split(";")
        all_rows.append(row[0])

#=========================================================================================

# najprej samo utstein del (brez slovenskih podatkov)
df = pd.read_csv("data.csv", sep=';',encoding='utf8')
utstein = df[["Domain", "Element", "Elements", "values"]]
rows = []
for row in utstein:
    rows.append(row)

# shranim indekse, imena, povezave
labels, connections = dict(), dict()
counter = 0
for row in utstein.values:
    for elt in row[:-1]: # zadnji stolpec so values ki si jih ne rabimo shranit
        if elt not in labels: # dodamo ga v slovar imen
            labels[elt] = counter
            counter += 1 
    for i in range(len(row)-2): # vse pare v vsaki vrstici shranim v slovar
        connections[(labels[row[i]], labels[row[i+1]])] = row[-1] # row[-1] = 1 

# za sankey potrebujemo tri sezname:
# label ..... imena vseh ploščic v diagramu
# source .... indeksi vseh ploščic
# targert ... kam peljejo 
# value ..... kakšna je vrednost (zaenkrat povsod 1)

label = list(labels.keys())

sources, targets, values = [], [], []
for key in connections:
    sources.append(key[0])
    targets.append(key[1])
    values.append(connections[key])

# Odkomentiraj, če hočeš, da se ti pokaže samo utstein del

# fig = go.Figure(data = [go.Sankey(
#     node = dict(pad = 15,
#             thickness = 20,
#             line = dict(color="black", width = 0.5),
#             label = label,
#             color = "blue"),
#     link = dict(source = sources,
#             target = targets,
#             value = values))])

# Odkomentiraj za Utstein sankey diagram
# fig.update_layout(title_text="Utstein protokol", font_size=10)
# fig.show()

#=================================================================================================

# Za splošen sankey moramo dodati protokole
protocols = all_rows[0][3:-1] # protokoli, ki se zbirajo v ZD MB
# protocols.append("DODATEN PROTOKOL UTSTEIN")
# protocol_index = dict()
# for i in range(len(protocols)):
#     protocol_index[i] = protocols[i]

nas_protokol = "DODATEN PROTOKOL UTSTEIN"


new_rows = [all_rows[0][3:-1]]#['PNI', 'PPO', 'PNRV', 'SI', 'COMPUTEL/ZD MB', 'PPP', 'NIJZ (SMRT)', 'DISP', 'BOLNICE/LIFEPAK']
for row in all_rows[1::]: # vse razen vrhnje vrstice
    appendix = []
    # row = row[0:7] # zdej gledamo samo protokole
    for i in range(3, len(row)-1): # spet odbijem value na koncu
        if row[i] == "1":
            appendix.append(protocols[i-3])
        if row[i] == "0":
            appendix.append(None) # da bodo vse vrstice imele enako dolžino da lahko potem naredim dataframe
    new_rows.append(row[0:3] + appendix)

# >>> new_rows[16] 
# ['Patient', 'Patient core', 'Patogeneza', None, 'PPO', None, None, 'COMPUTEL/ZD MB', None, None]
# >>> new_rows[17] 
# ['Patient', 'Patient supplemental', 'Samostojno življenje', None, None, None, None, None, None, None]


for row in new_rows:
    for elt in row: 
        if elt not in labels and elt != None: # dodamo ga v slovar imen
            labels[elt] = counter # nadaljujemo od prej
            counter += 1 
labels[nas_protokol] = len(labels)
labels["API"] = len(labels)
labels["API/CSV"] = len(labels)
labels["BAZA"] = len(labels)

# najprej lahko direkt dodam povezave med protokoli in ZD MB
for protocol in protocols[:4]:
    connections[(labels[protocol], labels[protocols[4]])] = 1
connections[(labels[nas_protokol], labels[protocols[4]])] = 1
connections[(labels[protocols[4]], labels["API"])] = 1
connections[(labels["API"], labels["BAZA"])] = 1
connections[(labels["API/CSV"], labels["BAZA"])] = 1

connections[(labels["PPP"], labels["API/CSV"])] = 1
connections[(labels["NIJZ (SMRT)"], labels["API/CSV"])] = 1
connections[(labels["DISP"], labels["API/CSV"])] = 1
connections[(labels["BOLNICE/LIFEPAK"], labels["API/CSV"])] = 1


# pri povezavah bolj pazljivo
for row in new_rows[1:]:
    elt = row[2]
    row_protocols = row[3:7] # od 3-7 so protokoli, na 7 je computel, 8 dalje pa ostalo

    row = row[8::]
    # row = row[3::]
    for p in row_protocols:
        if p != None:
            connections[(labels[elt], labels[p])] = 1 
    if any(row):
        for p in row:
            if p != None:
                connections[(labels[elt], labels[p])] = 1 # pazi, če bomo spreminjali values
    else:
        if not any(row_protocols): # če se ne zbira na nobenem protokolu in nikjer drugje moramo dodat na nas protokol
            connections[(labels[elt], labels[nas_protokol])] = 1 

# zdej je treba dodati povezave med protokoli in ZD/COMPUTEL
# labels["ZD MB/COMPUTEL"] = len(labels)
# protocols.append(nas_protokol)
# for protocol in protocols:
#     connections[(labels[protocol], labels[protocols[4]])] = 1

# Zdej pa še povezave podatki z ostalimi možnostmi: PPP, NIJZ, DISP, BOLNICE

label = list(labels.keys())
sources, targets, values = [], [], []
for key in connections:
    sources.append(key[0])
    targets.append(key[1])
    values.append(connections[key])

def random_color_generator():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return [r, g, b]
    "rgba(" + str(r) + "," + str(g) + "," + str(b) + "," + str(opacity) + ")"

colors, colors_conn = [], []
for i in range(200):
    [r, g, b] = random_color_generator()
    colors.append("rgba(" + str(r) + "," + str(g) + "," + str(b) + "," + str(0.8) + ")")
    colors_conn.append("rgba(" + str(r) + "," + str(g) + "," + str(b) + "," + str(0.4) + ")")

#==========================================================================================

fig = go.Figure(data = [go.Sankey(
    node = dict(pad = 15,
            thickness = 20,
            line = dict(color="black", width = 0.5),
            label = label,
            color = colors),
    link = dict(source = sources,
            target = targets,
            value = values
            #color = colors_conn
            ))])

fig.update_layout(title_text="Utstein protokol", font_size=10)
fig.show()






# df = pd.DataFrame(columns=new_rows[0])
# for row in new_rows:
#     # print(len(row))
#     print(row)
#     df.loc[len(df.index)] = row