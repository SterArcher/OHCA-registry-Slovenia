from ohca.forms import generate_dispatch_id
from ohca.models import *
import csv
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

def parseTime(time: str):
    timestampFormat1 = '%Y-%m-%d %H:%M:%S.%f'
    timestampFormat2 = '%d.%m.%Y %H:%M'
    if time != None:
        try:
            timestamp = datetime.strptime(time, timestampFormat1)
        except:
            try:
               timestamp = datetime.strptime(time, timestampFormat2)
            except:
                return None
        return timestamp
    
    return None

def parseHelperCPR(data):
    if data != None:
        try:
            parseTime(data)
            return 1
        except:
            return 0
    return 0

def calcSeconds(time, beginning):
    timestamp = time
    if timestamp != None and beginning != None:
        delta = timestamp - beginning
        return int(delta.total_seconds())

def dispatchDataParse(data):
    output = []
    reader = csv.DictReader(data, delimiter=';', quotechar='"')
    for row in reader:
        if len(row) == 0:
            continue

        for key,val in row.items():
            if "NULL" in val:
                row[key] = None

        item = dict()
        item['dispatchID'] = generate_dispatch_id(
            row['ID_Prevoza'],
            str('20' + row['ID_Prevoza'][2:3] + '-' + row['ID_Prevoza'][4:5] + '-' + row['ID_Prevoza'][6:7]
        ))
        item["interventionID"] = '0' + row['ID_Prevoza']
        item["mainInterventionID"] = '0' + row['ID_Osnovnega_prevoza']
        # item["reaTime"]
        item["callTimestamp"] = parseTime(row['Dvig'])
        time0 = item["callTimestamp"]
        item["dispProvidedCPRinst"] = int(not parseTime(row['Zacetek_TPO']))
        item["timestampTCPR"] = parseTime(row['Zacetek_TPO'])
        item["timeTCPR"] = calcSeconds(item['timestampTCPR'], time0)
        # item["CPRbystander3Time"]
        item["helperCPR"] = parseHelperCPR(parseTime(row['Aktivacija_PP']))
        item["helperWho"] = 3
        # item["CPRhelper3Time"]
        item["responseTimestamp"] = parseTime(row['Na_kraju_dogodka'])
        item["responseTime"] = calcSeconds(item["responseTimestamp"], time0)
        #item["AEDconn"] = int(not parseTime(row['Na_kraju_AED']))
        item["AEDshock"] = int(not parseTime(row['Zacetek_AED']))
        item["defibTimestamp"] = parseTime(row['Zacetek_AED'])
        item["defibTime"] = calcSeconds(item["defibTimestamp"], time0)
        item["leftScene5Timestamp"] = parseTime(row['S_kraja_dogodka'])
        item["leftScene5Time"] = calcSeconds(item["leftScene5Timestamp"], time0)
        item["hospitalArrival6Timestamp"] = parseTime(row['Na_cilju'])
        item["hospitalArrival6Time"] = calcSeconds(item["hospitalArrival6Timestamp"], time0)

        output.append(item)

    return output