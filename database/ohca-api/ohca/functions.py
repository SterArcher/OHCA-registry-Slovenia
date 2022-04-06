from ohca.models import *

def to_CaseReport(json, caseKey):
    entry = None
    if caseKey == 'dispatchID':
        entry = CaseReport.objects.filter(dispatchID__exact=json['dispatchID'])[0]
    elif caseKey == 'caseID':
        entry = CaseReport.objects.filter(caseID__exact=json['caseID'])[0]
    return entry.update(**json)

def to_Locale(json):
    entry = None
    if id == 'localID':
        entry = CaseReport.objects.filter(localID__exact=json['localID'])[0]
    elif id == 'friendlyName':
        entry = CaseReport.objects.filter(friendly__exact=json['friendlyName'])[0]
    return entry.update(**json)

def to_System(json, id):
    entry = None
    if id == 'systemID':
        entry = CaseReport.objects.filter(systemID__exact=json['systemID'])[0]
    elif id == 'friendlyName':
        entry = CaseReport.objects.filter(friendly__exact=json['friendlyName'])[0]
    return entry.update(**json)

def validate_post(request):
    return request.method == 'POST'