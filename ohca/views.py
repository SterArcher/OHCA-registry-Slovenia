from rest_framework.response import Response
from .functions import *

def case_by_id(request):
    if validate_post(request):
        if to_CaseReport(request.POST, 'caseID'):
            return Response({"message": "Saved case report"})
        else:
            return Response({"message": "Error saving case report"})

def case_by_id_multi(request):
    if validate_post(request):
        i = 0
        errors = []
        for caseJSON in request.POST['cases']:
            if not(to_CaseReport(caseJSON, 'caseID')):
                errors.append(i)
            i += 1
        if len(errors) == 0:
            return Response({"message": "All case reports saved successfully"})
        else:
            return Response({"message": "Error saving case reports: " + ', '.join(errors)})

def case_by_disp(request):
    if validate_post(request):
        if to_CaseReport(request.POST, 'dispatchID'):
            return Response({"message": "Saved case report"})
        else:
            return Response({"message": "Error saving case report"})

def case_by_disp_multi(request):
    if validate_post(request):
        i = 0
        errors = []
        for caseJSON in request.POST['cases']:
            if not(to_CaseReport(caseJSON, 'dispatchID')):
                errors.append(i)
            i += 1
        if len(errors) == 0:
            return Response({"message": "All case reports saved successfully"})
        else:
            return Response({"message": "Error saving case reports: " + ', '.join(errors)})

def system_view(request):
    if validate_post(request):
        if to_System(request.POST):
            return Response({"message": "System definition saved successfully"})
        else:
            return Response({"message": "Error saving system definition"})

def locale_view(request):
    if validate_post(request):
        if to_Locale(request.POST):
            return Response({"message": "Locale definition saved successfully"})
        else:
            return Response({"message": "Error saving locale definition"})

from ohca.dataSummary import summary_table
import csv
from django.http import HttpResponse

def download(request):
    "Takes the dictionary of elements and their counts and writes a csv"
    response = HttpResponse(content_type='text/csv')
    writer = csv.writer(response)

    header = ["Element", "Count"]
    rows = []
    for key in summary_table:
        row = []
        row.append(key)
        row.append(summary_table[key])
        rows.append(row)

    writer.writerow(header)
    writer.writerows(rows)

    response['Content-Disposition'] = 'attachment; filename="summary_table.csv"'
    return response

def http_response(request):
    return HttpResponse('<h1>Download summary data table</h1><a href="download/">right here</a>')
