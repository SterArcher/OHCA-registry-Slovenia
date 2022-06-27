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

def calculate_age(birth, cardiac_arrest):
    """Calculates age from date of birth.
    Returns the age on the day of the event (so 55 years and 360 days is 55 years)"""

    # datum dobiš v obliki: 2020-01-01
    birth = birth.split("-") # [year, month, day]
    ca = cardiac_arrest.split("-")

    years = int(ca[0]) - int(birth[0])

    if int(ca[1]) == int(birth[1]): # ih it's the same month
        if int(ca[2]) < int(birth[2]):
            years -= 1

    elif int(ca[1]) < int(birth[1]):
        years -= 1
 
    return years

def calculate_time(time1, time2):
    """Takes two timestaps in the form "HH:MM:SS" and calculates how many second passed.
    It's assumed time1 happened before time2
    """

    time1 = time1.split(":")
    time2 = time2.split(":")

    seconds1 = time1[0] * 60 * 60 + time1[1] * 60 + time1[2] # convert time to seconds
    seconds2 = time2[0] * 60 * 60 + time2[1] * 60 + time2[2]

    diff = seconds2 - seconds1

    # what if time1 happens before midnight and time2 happens after midnight?
    # in that case seconds1 > seconds2

    # TODO : preveri če je ok ko boš zbrana
    if seconds1 >= seconds2:
        midnight = 24 * 3600
        diff = (midnight - seconds1) + seconds2

    # what if one of them is midnight 00:00:00 ???

    return diff


def new_index(request):
    return render(request, "ohca/index.html")

def form_name_view(request):
    form1 = MyNewFrom() 
    form2 = InterventionForm()
    if request.method == "POST":

        form1 = MyNewFrom(request.POST)
        form2 = InterventionForm(request.POST)

        if form1.is_valid() and form2.is_valid(): 
            
            print("VALIDATION SUCCESS")

            # i1 = form2.cleaned_data["i1"]
            # i2 = form2.cleaned_data["i2"]
            # i3 = form2.cleaned_data["i3"]
            # i4 = form2.cleaned_data["i4"]

            # print((i1, i2, i3, i4))
            
            first_name = (form1.cleaned_data['Patient_name']).strip().split(" ")
            last_name = (form1.cleaned_data['Patient_surname']).strip().split(" ")

            temp = request.POST['bystanderResponseTime']
            print(temp)
            print(str(form1.cleaned_data["bystanderResponseTime"]))

            date = str(form1.cleaned_data['Date'])
            date_birth = str(form1.cleaned_data["Date_birth"])
            # print((date, date_birth))


            id = generate_id("".join(first_name), "".join(last_name), date, date_birth)
            form1.instance.caseID = id #[0:32] #"".join([word[0] for word in first_name])
            form1.instance.age = calculate_age(date_birth, date)

            # form1.instance.intervention = tiste cifre

            ## Set vseh uporabljenih zdravil, dovoljena izbira vedih (kot vsota ID-jev vrednosti)
            sum = 0
            for elt in form1.cleaned_data['All_drugs']:
                options = {'Neznano': -1, 'Brez': 0, 'Adrenaline': 1,'Amiodarone': 2, 'Vasopressin': 4}
                sum += int(options[elt])
            form1.instance.drugs = str(sum)
           
            form1.instance.reaLand = "1"

            # to save into database:
            form1.save()
            # return index(request) # to mi neke errorje vrača, not sure why 

            
        else:
            print("form invalid")
    else:
        form1 = MyNewFrom() 
        form2 = InterventionForm()
    return render(request, "ohca/form_page.html", {"form1":form1, "form2":form2})


def second_form_name_view(request):
    form1 = MySecondNewFrom() 
    form2 = InterventionForm()
    if request.method == "POST":

        form1 = MySecondNewFrom(request.POST)
        form2 = InterventionForm(request.POST)

        if form1.is_valid() and form2.is_valid(): 
            
            print("VALIDATION SUCCESS")

            first_name = (form1.cleaned_data['Patient_name']).strip().split(" ")
            last_name = (form1.cleaned_data['Patient_surname']).strip().split(" ")

            date = str(form1.cleaned_data['Date'])
            date_birth = str(form1.cleaned_data["Date_birth"])

            print((date, date_birth))

            # form.instance.age = calculate_age(date_birth, date) # age bo že od prej

            id = generate_id("".join(first_name), "".join(last_name), date, date_birth)
            CaseReport.objects.update_or_create(
                caseID=id, 
                defaults=dict([(field, form1.cleaned_data[field]) for field in form2[1:]])
                # {
                #     "ecls" : form.cleaned_data["ecls"] # zgeneriraj
                # }
            ) # update, create
            form1.instance.caseID = id #[0:32] #"".join([word[0] for word in first_name])
            # form.instance.systemID = System.objects.all().filter(systemID__exact=int(zdID))[0] 

            # to save into database:
            # form.save(commit=True)
            # return index(request) # to mi neke errorje vrača, not sure why 
        else:
            print("form invalid")
    return render(request, "ohca/second_form_page.html", {"form1":form1, "form2":form2})


def third_form_name_view(request):

    form1 = MyThirdNewFrom() 
    form2 = InterventionForm()
    if request.method == "POST":

        form1 = MyThirdNewFrom(request.POST)
        form2 = InterventionForm(request.POST)

        if form1.is_valid() and form2.is_valid(): 

            print("VALIDATION SUCCESS")
            
            first_name = (form1.cleaned_data['Patient_name']).strip().split(" ")
            last_name = (form1.cleaned_data['Patient_surname']).strip().split(" ")

            date = str(form1.cleaned_data['Date'])
            date_birth = str(form1.cleaned_data["Date_birth"])

            print((date, date_birth))
            print(calculate_age(date_birth, date))
            form1.instance.age = calculate_age(date_birth, date)
            
            id = generate_id(first_name, last_name, date, date_birth)
            print(id)
            print(len(id))
            # print(id.digest())
            cases = CaseReport.objects.all()
            existing_ids = []
            for case in cases:
                existing_ids.append(case.caseID)
            form1.instance.caseID = id #[0:32] #random.choice([i for i in range(100000, 10000000) if i not in existing_ids]) #id 
            # form.instance.systemID = System.objects.all().filter(systemID__exact=int(zdID))[0] 

            ## Set vseh uporabljenih zdravil, dovoljena izbira vedih (kot vsota ID-jev vrednosti)
            sum = 0
            for elt in form1.cleaned_data['All_drugs']:
                options = {'Neznano': -1, 'Brez': 0, 'Adrenaline': 1,'Amiodarone': 2, 'Vasopressin': 4}
                sum += int(options[elt])
            form1.instance.drugs = str(sum)
            form1.instance.reaLand = "1"
            # # to save into database:
            form1.save(commit=True) #
            # return index(request) # to mi neke errorje vrača, not sure why 
        else:
            print("form invalid")
    return render(request, "ohca/third_form_page.html", {"form1":form1, "form2":form2})