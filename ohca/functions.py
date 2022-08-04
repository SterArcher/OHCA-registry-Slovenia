from ohca.models import *

def to_CaseReport(json, caseKey):
    entry = None
    if caseKey == 'dispatchID':
        entry = CaseReport.objects.update_or_create(dispatchID=json['dispatchID'], defaults=json)
    elif caseKey == 'caseID':
        entry = CaseReport.objects.update_or_create(caseID=json['caseID'], defaults=json)
    return entry[0]

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