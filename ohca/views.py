from rest_framework.response import Response
from .functions import *
import random

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

# =================== FOR DOWLOANDING SUMMARY DATA TABLE ==================================

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
  
from django.views.generic import TemplateView

class index(TemplateView):
    template_name = "sum.html"  


# ==================== FOR AUTO FORM ============================================

from django.shortcuts import render
from . import forms
from ohca.forms import *
from ohca.models import CaseReport, System, Locale

def new_index(request):
    return render(request, "ohca/index.html")

def form_name_view(request):
    # form = forms.MyNewFrom()
    form = MyNewFrom() 
    if request.method == "POST":
        form = MyNewFrom(request.POST)
        # print(form) 
        if form.is_valid():
            #
            print("VALIDATION SUCCESS")
            #
            first_name = (form.cleaned_data['Patient_name']).strip().split(" ")
            last_name = (form.cleaned_data['Patient_surname']).strip().split(" ")
            obcina = form.cleaned_data["localID"] # TODO da ti bo prov delal
            print(obcina) # iz forme dobimo ime obcine
            print(ems[str(obcina)]) # tole bi moral bit ZD, ki pokriva to obcino

            # poiščem id tega zdravstvenega doma v Sytems

            zdID = System.objects.all().filter(friendlyName__exact=ems[str(obcina)])[0].systemID
            print(zdID)
            # obcinaID = Locale.objects.all().filter(friendlyName__exact=str(ems[str(zdID)]))[0].localID
            # print(obcinaID)
            # print(ems[zd])
            # print(first_name, "".join([word[0] for word in first_name]))
            # print(first_name)#
            # print(last_name)#
            date = str(form.cleaned_data['Date'])
            print(date)
            date_birth = str(form.cleaned_data["Date_birth"])
            print((date, date_birth))
            # print(str(date).split("-"))#
            id = generate_id("".join(first_name), "".join(last_name), date, date_birth)
            form.instance.caseID = id #"".join([word[0] for word in first_name])
            form.instance.systemID = System.objects.all().filter(systemID__exact=int(zdID))[0] 

            # to save into database:
            # form.save(commit=True)
            # return index(request) # to mi neke errorje vrača, not sure why 
        else:
            print("form invalid")
    return render(request, "ohca/form_page.html", {"form":form})


def second_form_name_view(request):
    # form = forms.MyNewFrom()
    form = MySecondNewFrom() 
    if request.method == "POST":
        form = MySecondNewFrom(request.POST)
        # print(form) 
        if form.is_valid():
            #
            print("VALIDATION SUCCESS")
            #
            first_name = (form.cleaned_data['Patient_name']).strip().split(" ")
            last_name = (form.cleaned_data['Patient_surname']).strip().split(" ")
            obcina = form.cleaned_data["localID"] # TODO da ti bo prov delal
            print(obcina) # iz forme dobimo ime obcine
            print(ems[str(obcina)]) # tole bi moral bit ZD, ki pokriva to obcino

            # poiščem id tega zdravstvenega doma v Sytems

            zdID = System.objects.all().filter(friendlyName__exact=ems[str(obcina)])[0].systemID
            print(zdID)
            # obcinaID = Locale.objects.all().filter(friendlyName__exact=str(ems[str(zdID)]))[0].localID
            # print(obcinaID)
            # print(ems[zd])
            # print(first_name, "".join([word[0] for word in first_name]))
            # print(first_name)#
            # print(last_name)#
            date = str(form.cleaned_data['Date'])
            date_birth = str(form.cleaned_data["Date_birth"])
            print((date, date_birth))
            # print(str(date).split("-"))#
            id = generate_id("".join(first_name), "".join(last_name), date, date_birth)
            form.instance.caseID = id #"".join([word[0] for word in first_name])
            # form.instance.systemID = System.objects.all().filter(systemID__exact=int(zdID))[0] 

            # to save into database:
            # form.save(commit=True)
            # return index(request) # to mi neke errorje vrača, not sure why 
        else:
            print("form invalid")
    return render(request, "ohca/second_form_page.html", {"form":form})

####
def third_form_name_view(request):
    # form = forms.MyNewFrom()
    form = MyThirdNewFrom() 
    if request.method == "POST":
        form = MyThirdNewFrom(request.POST)
        # print(form) 
        if form.is_valid():
            #
            print("VALIDATION SUCCESS")
            #
            first_name = (form.cleaned_data['Patient_name']).strip().split(" ")
            last_name = (form.cleaned_data['Patient_surname']).strip().split(" ")
            # obcina = form.cleaned_data["localID"] # TODO da ti bo prov delal
            # print(obcina) # iz forme dobimo ime obcine
            # print(ems[str(obcina)]) # tole bi moral bit ZD, ki pokriva to obcino

            # # poiščem id tega zdravstvenega doma v Sytems

            # zdID = System.objects.all().filter(friendlyName__exact=ems[str(obcina)])[0].systemID
            # print(zdID)
            # # obcinaID = Locale.objects.all().filter(friendlyName__exact=str(ems[str(zdID)]))[0].localID
            # # print(obcinaID)
            # # print(ems[zd])
            # # print(first_name, "".join([word[0] for word in first_name]))
            # # print(first_name)#
            # # print(last_name)#
            # date = str(form.cleaned_data['Date'])
            # date_birth = str(form.cleaned_data["Date_birth"])
            # print((date, date_birth))
            # # print(str(date).split("-"))#
            # id = generate_id("".join(first_name), "".join(last_name), date, date_birth)
            # print(id)
            # print(id.digest())
            cases = CaseReport.objects.all()
            existing_ids = []
            for case in cases:
                existing_ids.append(case.caseID)
            form.instance.caseID = random.choice([i for i in range(100000, 10000000) if i not in existing_ids]) #id 
            # form.instance.systemID = System.objects.all().filter(systemID__exact=int(zdID))[0] 

            # # to save into database:
            form.save(commit=True)
            # return index(request) # to mi neke errorje vrača, not sure why 
        else:
            print("form invalid")
    return render(request, "ohca/third_form_page.html", {"form":form})