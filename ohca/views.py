from dis import dis
from sys import prefix
from rest_framework.response import Response
from .functions import *
import random, time
from datetime import date, datetime
import datetime
# from .auxiliary import timestamps
# from .forms import timestamp_dict

# timestamps.remove("cPREMS3Timestamp")


def case_by_id(request):
    if validate_post(request):
        if to_CaseReport(request.POST, 'caseID'):
            return Response({"message": "Saved case report"})
        else:
            return Response({"message": "Error saving case report"})

def case_by_id_multi(request): #
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

from django.shortcuts import redirect, render
from . import forms
from ohca.forms import *
from ohca.models import CaseReport, System, Locale
from django.http import HttpResponseRedirect
from django.contrib import messages

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

def calculate_time(date1, time1, date2, time2):
    """Takes two timestaps in the form "HH:MM:SS" and calculates how many second passed.
    It's assumed time1 happened before time2
    """

    print((date1, date2))
    print((time1, time2))

    date1 = date1.split("-")
    date2 = date2.split("-")

    if "+" in time1:
        time1 = time1[:time1.find("+")]
    if "+" in time2:
        time2 = time2[:time2.find("+")]

    print((time1, time2))

    time1 = time1.split(":")
    time2 = time2.split(":")

    

    datetime1 = datetime(int(date1[0]), int(date1[1]), int(date1[2]), int(time1[0]), int(time1[1]), int(time1[2]))
    datetime2 = datetime(int(date2[0]), int(date2[1]), int(date2[2]), int(time2[0]), int(time2[1]), int(time2[2]))

    duration = datetime2 - datetime1
    duration_seconds = duration.total_seconds()

    return int(duration_seconds)


def day_difference(date1, date2):
    """Calculates number of days between two days (for discharge day).
    Assumes date2 (day of discarge) happened after date1 (day of CA).
    Dates are in form: 2020-02-03 (year, month, day)"""

    date1 = date1.split("-")
    date2 = date2.split("-")

    d1 = date(int(date1[0]), int(date1[1]), int(date1[2]))
    d2 = date(int(date2[0]), int(date2[1]), int(date2[2]))

    diff = d2 - d1 

    return int(diff.days)

# ================== FOR UPLOADING DSZ DATA DUMPS ===================================

def dsz(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['document'].read().decode('utf-8-sig').replace('\r', '').replace('\n\n', '\n').split('\n')
        dataJson = dispatchDataParse(uploaded_file)
        result = None
        for block in dataJson:
            result = to_CaseReport(block, 'dispatchID')
        if result:
            messages.success(request, 'Podatki uspešno oddani!')
        else:
            messages.error(request, "Napaka pri obdelavi podatkov!")     
    return render(request, 'ohca/dsz.html')

# ================== FORMS ==========================================================

def new_index(request):
    return render(request, "ohca/index.html")

def form_name_view(request):
    form1 = MyNewFrom() 
    form2 = InterventionForm()
    if request.method == "POST":
        
        form1 = MyNewFrom(request.POST)       
        form2 = InterventionForm(request.POST)
        print(form1.errors)

        if form2.is_valid() and form1.is_valid(): 

            messages.success(request, 'Podatki uspešno oddani!')

            print("VALIDATION SUCCESS")

            izracunana_polja = []

            f = ["i1",'i2','i3','i4','i5','i6','i7','i8','i9','i10','i11','i12'] 
            intID = '' 
            for field in f:
                intID += str(form2.cleaned_data[field])
            print(intID)

            izracunana_polja.append(("interventionID", intID))
            izracunana_polja.append(("mainInterventionID", intID))

            first_name = (form1.cleaned_data['name']).strip().split(" ")
            last_name = (form1.cleaned_data['surname']).strip().split(" ")
            date = str(form1.cleaned_data['dateOfCA'])
            date_time = str(form1.cleaned_data["reaTimestamp"])

            id = generate_case_id(" ".join(first_name), " ".join(last_name), date, date_time)
            form1.instance.caseID = id 

            birth = form1.cleaned_data['dateOfBirth']
            estimAge = form1.cleaned_data['estimatedAge']

            if birth != None and estimAge == None:

                calculated_age = calculate_age(str(birth), date)
                izracunana_polja.append(("age", calculated_age))
                print(calculate_age)

            elif birth != None and estimAge != None: 
                pass # TODO 

            # izracunana_polja.append(("gender", form1.cleaned_data["gender"]))

            # ca_date = form1.cleaned_data["dateOfCA"]
            y, m, d = date.split("-")

            izracunana_polja.append(("reaYr", int(y)))
            izracunana_polja.append(("reaMo", int(m)))
            izracunana_polja.append(("reaDay", int(d)))

            izracunana_polja.append(("dispatchID", generate_dispatch_id(str(intID), date)))

            izracunana_polja.append(("reaLand", "Slovenia"))
            izracunana_polja.append(("reaRegion", str(form1.cleaned_data["localID"])))
            
            izracunana_polja.append(("localID", Locale.objects.all().filter(friendlyName__exact=form1.cleaned_data["localID"])[0]))
            izracunana_polja.append(("systemID", System.objects.all().filter(friendlyName__exact=form1.cleaned_data["systemID"])[0]))
            

            # field_dict = dict([(field, form1.cleaned_data[field]) for field in first_form] + izracunana_polja)
            # new_field_dict = dict() #dict(filter(lambda val: val[0] != None, field_dict.items()))
            # for elt in field_dict:
            #     if field_dict[elt] != None:
            #         new_field_dict[elt] = field_dict[elt]

            print(izracunana_polja)
            # print(new_field_dict)
            CaseReport.objects.update_or_create(
                caseID=id, 
                defaults=dict([(field, form1.cleaned_data[field]) for field in first_form] + izracunana_polja)
            ) 
            
        else:
            print("form invalid")
            messages.error(request, 'Nepravilno izpolnjen obrazec.')
            messages.error(request, form1.errors)
    else:
        form1 = MyNewFrom() 
        form2 = InterventionForm()
    return render(request, "ohca/form_page.html", {"form1":form1, "form2":form2})


def second_first_form_name_view(request):
    form1 = MyNewFrom()
    # form2 = TimestampForm()

    if request.method == "POST":
        form1 = MyNewFrom(request.POST)
        print(form1.errors)
        # form2 = TimestampForm(request.POST)
        # print(form2.errors)

        if form1.is_valid(): # and form2.is_valid():
            print("VALIDATION SUCCESS")

            messages.success(request, 'Podatki uspešno oddani!')

            izracunana_polja = []
            
            first_name = (form1.cleaned_data['name']).strip().split(" ")
            last_name = (form1.cleaned_data['surname']).strip().split(" ")
            date = str(form1.cleaned_data['dateOfCA'])
            date_time = str(form1.cleaned_data["reaTimestamp"])

            id = generate_case_id(" ".join(first_name), " ".join(last_name), date, date_time)
            form1.instance.caseID = id 

            birth = form1.cleaned_data['dateOfBirth']
            estimAge = form1.cleaned_data['estimatedAge']

            if birth != None and estimAge == None:

                calculated_age = calculate_age(str(birth), date)
                izracunana_polja.append(("age", calculated_age))

            elif birth != None and estimAge != None: 
                pass # TODO 



            # id = generate_case_id("".join(first_name), "".join(last_name), date, date_birth)
            print(id)
            CaseReport.objects.update_or_create(
                caseID=id, 
                defaults=dict([(field, form1.cleaned_data[field]) for field in first_form] + izracunana_polja)
            )
        else:
            print("form invalid")
            messages.error(request, 'Nepravilno izpolnjen obrazec.')
            messages.error(request, form1.errors)
    else:
        form1 = MyNewFrom() 
        # form2 = TimestampForm()
    return render(request, "ohca/second_first_formpage.html", {"form1":form1})


def second_form_name_view(request):
    form1 = MySecondNewFrom() 
    # form2 = InterventionForm()
    if request.method == "POST":

        form1 = MySecondNewFrom(request.POST)
        print(form1.errors)
        
        # form2 = InterventionForm(request.POST)

        if form1.is_valid(): # and form2.is_valid(): 
            
            print("VALIDATION SUCCESS")

            messages.success(request, 'Podatki uspešno oddani!')

            izracunana_polja = []

            # f = ["i1",'i2','i3','i4','i5','i6','i7','i8','i9','i10','i11','i12',] #
            # intID = '' 
            # for field in f:
            #     intID += str(form2.cleaned_data[field])
            # print(intID)

            # izracunana_polja.append(("interventionID", intID))
            # izracunana_polja.append(("mainInterventionID", intID))
            

            first_name = (form1.cleaned_data['name']).strip().split(" ")
            last_name = (form1.cleaned_data['surname']).strip().split(" ")

            date = str(form1.cleaned_data['dateOfCA'])
            date_birth = str(form1.cleaned_data["dateOfBirth"])
            disch_date = str(form1.cleaned_data["discDate"])
            # print((date, date_birth))
            
            print(date, disch_date)
            print(date and disch_date)
            if not (date and disch_date):
                print(day_difference(date, disch_date))
                form1.instance.dischDay = day_difference(date, disch_date)

            print((date, date_birth))
            if disch_date != None:
                disch_date = disch_date.split("-")
                izracunana_polja.append(("dischYear", disch_date[0]))
                izracunana_polja.append(("dischMonth", disch_date[1]))
                izracunana_polja.append(("dischDay", disch_date[2]))
            # form.instance.age = calculate_age(date_birth, date) # age bo že od prej

            if form1.cleaned_data["survivalDischarge"] == 1 or form1.cleaned_data["survival30d"] == 1:
                izracunana_polja.append(("SurvivalDischarge30d", 1))
            
            izracunana_polja.append(("localID", Locale.objects.all().filter(friendlyName__exact=form1.cleaned_data["localID"])[0]))
            izracunana_polja.append(("systemID", System.objects.all().filter(friendlyName__exact=form1.cleaned_data["systemID"])[0]))
           
            id = generate_case_id(" ".join(first_name), " ".join(last_name), date, date_birth)
            CaseReport.objects.update_or_create(
                caseID=id, 
                defaults=dict([(field, form1.cleaned_data[field]) for field in second_form]+ izracunana_polja)

            ) # update, create
            

        else:
            print("form invalid")
            messages.error(request, 'Nepravilno izpolnjen obrazec.')
            messages.error(request, form1.errors)
    else:
        form1 = MySecondNewFrom() 
        # form2 = InterventionForm()
    return render(request, "ohca/second_form_page.html", {"form1":form1})


