import plotly.graph_objects as go
import random

# Imena
si = "Emergency call admission" #"sprejem intervencij"
pni = "Emergency intervention report"  #"poročilo/protokol nujne intervencije"
pnrv = "Emergency protocol of the out-of-hospital EMS" # "protokol nujnega reševalnega vozila"
ppo = "Out-of-hospital CPR" #"predbolnišnično oživljanje"
utst = "Supplementary Utstein protocol"
nijz = "National Institute of Public Health" #"NIJZ (v primeru smrti)"
hosp = "Hospitals" # Večinoma v obliki protokola triaže,statusa/anamneze/rezultatov diagnostike in odpustnice
disp = "Dispatch service"
ppp = "First responders"
comp = "IT system provider" #"Computel"
api = "API"
api_csv = "API/CSV"
db = "Utstein database"



def random_color_generator():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)
    return [r, g, b]
    #"rgba(" + str(r) + "," + str(g) + "," + str(b) + "," + str(opacity) + ")"

colors, colors_conn = [], []
for i in range(20):
    [r, g, b] = random_color_generator()
    colors.append("rgba(" + str(r) + "," + str(g) + "," + str(b) + "," + str(0.9) + ")")
    colors_conn.append("rgba(" + str(r) + "," + str(g) + "," + str(b) + "," + str(0.5) + ")")



elements = [si, pni, pnrv, ppo, utst, nijz, hosp, disp, ppp, comp, api, api_csv, db]
labels, counter = dict(), 0
for elt in elements:
    labels[elt] = counter
    counter += 1

protocols, rest = [si, pni, pnrv, ppo, utst], [nijz, hosp, disp, ppp]
connections = dict()
for protocol in protocols:
    connections[(labels[protocol], labels[comp])] = 1
for elt in rest:
    connections[(labels[elt], labels[api_csv])] = 1
connections[(labels[comp], labels[api])] = len(protocols)
connections[(labels[api_csv], labels[db])] = len(rest)
connections[(labels[api], labels[db])] = len(protocols)


label = list(labels.keys())
sources, targets, values = [], [], []
for key in connections:
    sources.append(key[0])
    targets.append(key[1])
    values.append(connections[key])

fig = go.Figure(data = [go.Sankey(
    node = dict(pad = 15,
            thickness = 20,
            line = dict(color="black", width = 0.5),
            label = label,
            color = colors),
    link = dict(source = sources,
            target = targets,
            value = values,
            #label = 'label',
            color = colors_conn))]) # 'rgb(220,220,220)'

fig.update_layout(title_text="Representation of data flow for the Slovenian OHCA registry based on the Utstein protocol.", font_size=10)

fig.show()
