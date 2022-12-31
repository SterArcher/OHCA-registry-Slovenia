from ohca.forms import generate_dispatch_id
from ohca.models import *
import pandas as pd
from datetime import datetime

def to_CaseReport(json, caseKey):
    try:
        if caseKey == 'dispatchID':
            CaseReport.objects.update_or_create(dispatchID=json['dispatchID'], defaults=json)
        elif caseKey == 'caseID':
            CaseReport.objects.update_or_create(caseID=json['caseID'], defaults=json)
        return True
    except:
        return False

def update_CaseReport(json, caseKey):
    try:
        i = 0
        if caseKey == 'dispatchID':
            i = CaseReport.objects.filter(dispatchID=json['dispatchID']).update(**json)
            if i == 0:
                return 2
        elif caseKey == 'caseID':
            i = CaseReport.objects.filter(caseID=json['caseID']).update(**json)
            if i == 0:
                return 2
        return 1
    except:
        return 0

def to_Locale(json):
    entry = None
    if id == 'localID':
        entry = CaseReport.objects.update_or_create(localID=json['localID'], defaults=json)
    elif id == 'friendlyName':
        entry = CaseReport.objects.update_or_create(friendly=json['friendlyName'], defaults=json)
    return entry[0]

def to_System(json, id):
    entry = None
    if id == 'systemID':
        entry = CaseReport.objects.update_or_create(systemID=json['systemID'], defaults=json)
    elif id == 'friendlyName':
        entry = CaseReport.objects.update_or_create(friendly=json['friendlyName'], defaults=json)
    return entry[0]

def validate_post(request):
    return request.method == 'POST'

def calcSeconds(time, beginning):
    timestamp = time
    if timestamp != None and beginning != None:
        delta = timestamp - beginning
        return int(delta.total_seconds())

rowNames = {
    'interventionID': 'ID_Prevoza',
    'mainInterventionID': 'ID_Osnovnega_prevoza',
    'callTimestamp': 'Čas sprejema klica v dispečerski center (dvig telefona)',
    'dispIdentifiedCA': 'Dispečer je prepoznal prisotnost zastoja srca pred prihodom NMP',
    'dispProvidedCPRinst': 'Ali je dispečer/NMP dal navodila po telefonu za oživljanje/TPO?',
    'timestampTCPR': 'Čas, ko je dispečer dal navodila za oživljanje po telefonu',
    'responseTimestamp': 'Čas prihoda NMP na kraj dogodka',
    'cPRbystander3Timestamp': 'Čas, ko je očividec pričel z oživljanjem (TPO)',
    'leftScene5Timestamp': 'Čas odhoda s kraja dogodka',
    'hospitalArrival6Timestamp': 'čas prihoda v bolnišnico',
    'firstResponder': 'Ali je bil na kraj zastoja poslana oseba, da nudi pomoč/oživljanje (npr. prvi posredovalec)?',
    'reaTimestamp': 'Čas nastanka srčnega zastoja iz klica',
    'AEDconn': 'Na_kraju_AED',
    'AEDshock': 'Zacetek_AED (1.,def)'
}

timestampsDSZ = {
    'timestampTCPR': 'timeTCPR',
    'responseTimestamp': 'responseTime',
    'cPRbystander3Timestamp': 'cPRbystander3Time',
    'leftScene5Timestamp': 'leftScene5Time',
    'hospitalArrival6Timestamp': 'hospitalArrival6Time',
    'reaTimestamp': 'reaTime'
}

copyDSZ = [
    'dispIdentifiedCA',
    'dispProvidedCPRinst'
]

implicitTrueDSZ = [
    'firstResponder',
    'AEDconn', 'AEDshock'
]

def implicitTrue(value):
    if value in [0, -1, -2]:
        return value
    else:
        return 1

def dispatchDataParse(data):
    output = []
    reader = pd.read_excel(data, header=1, usecols="A:N", na_values=[" ", '\xa0'])
    for i, row in reader.iterrows():
        item = dict()

        # Calculate and store identifiers
        item["interventionID"] = f'0{row[rowNames["interventionID"]]}'
        item["mainInterventionID"] = f'0{row[rowNames["mainInterventionID"]]}'
        item['dispatchID'] = generate_dispatch_id(
            item["interventionID"],
            f'20{item["interventionID"][2:4]}-{item["interventionID"][4:6]}-{item["interventionID"][6:8]}'
        )
        
        # helperWho is a constant for DSZ cases
        item["helperWho"] = 3
        
        # Take care of the fields that should just be copied
        for name in copyDSZ:
            value = row[rowNames[name]]
            if pd.notnull(reader.loc[i, rowNames[name]]):
                item[name] = int(value)

        # Convert timestamp into implicit true
        for name in implicitTrueDSZ:
            value = row[rowNames[name]]
            if pd.notnull(reader.loc[i, rowNames[name]]):
                item[name] = implicitTrue(value)
        
        # Take care of all the timestamps
        for name in ['callTimestamp'] + list(timestampsDSZ.keys()):
            time = row[rowNames[name]] #.to_pydatetime()
            if pd.notnull(reader.loc[i, rowNames[name]]):
                item[name] = time

        # Calculate all the times
        if "callTimestamp" in item:
            time0 = item["callTimestamp"]
            for timestamp, time in timestampsDSZ.items():
                value = row[rowNames[timestamp]]
                if pd.notnull(reader.loc[i, rowNames[timestamp]]) and isinstance(value, datetime) and isinstance(time0, datetime):
                    delta = value - time0
                    item[time] = int(delta.total_seconds())

        print(item)
        output.append(item)

    return output