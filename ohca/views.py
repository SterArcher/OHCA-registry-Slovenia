from dis import dis
from sys import prefix
from rest_framework.response import Response
from .functions import *
import random, time
from datetime import date, datetime
import datetime


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

from .forms import timestamps, timestamp_dict
from .functions import *

timeline = timestamps

def new_index(request):
    return render(request, "ohca/index.html")

def form_name_view(request):
    form1 = DSZ_1_DAN() 
    form2 = InterventionForm()
    context = {}
    if request.method == "POST":
        
        form1 = DSZ_1_DAN(request.POST)     
        form2 = InterventionForm(request.POST)

        

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

            # first_name = (form1.cleaned_data['name']).strip().split(" ")
            # last_name = (form1.cleaned_data['surname']).strip().split(" ")
            date = str(form1.cleaned_data['dateOfCA'])
            # date_time = str(form1.cleaned_data["reaTimestamp"])

            dispatch_id = generate_dispatch_id(str(intID), date)
            # id = generate_case_id(" ".join(first_name), " ".join(last_name), date, date_time)
            # form1.instance.caseID = id 

            birth = form1.cleaned_data['dateOfBirth']
            estimAge = form1.cleaned_data['estimatedAge']

            if birth != None: # and estimAge == None:

                calculated_age = calculate_age(str(birth), date)
                izracunana_polja.append(("age", calculated_age))
                print(calculate_age)

            elif birth != None and estimAge != None: 
                pass # TODO 

            # handle multipleselect fields separately
            # izracunana_polja.append(("drugs", form1.cleaned_data["drugs"]))
            # izracunana_polja.append(("airwayControl", form1.cleaned_data["airwayControl"]))

            # drugs = form1.cleaned_data['allDrugs']
            # drugs = list(map(lambda x: int(x), drugs))
            # print((drugs, sum(drugs)))
            # if drugs:
            #     izracunana_polja.append(("drugs", sum(drugs)))

            # airway = form1.cleaned_data['airway']
            # airway = list(map(lambda x: int(x), airway))
            # print((airway, sum(airway)))
            # if airway:
            #     izracunana_polja.append(("airwayControl", sum(airway)))


            # ca_date = form1.cleaned_data["dateOfCA"]
            y, m, d = date.split("-")

            izracunana_polja.append(("reaYr", int(y)))
            izracunana_polja.append(("reaMo", int(m)))
            izracunana_polja.append(("reaDay", int(d)))

            # izracunana_polja.append(("dispatchID", generate_dispatch_id(str(intID), date)))

            izracunana_polja.append(("reaLand", "Slovenia"))
            izracunana_polja.append(("reaRegion", str(form1.cleaned_data["localID"])))
            
            izracunana_polja.append(("localID", Locale.objects.all().filter(friendlyName__exact=form1.cleaned_data["localID"])[0]))
            izracunana_polja.append(("systemID", System.objects.all().filter(friendlyName__exact=form1.cleaned_data["systemID"])[0]))
            
            if form1.cleaned_data["ttmTemp"] == None:
                izracunana_polja.append(("ttmTemp", form1.cleaned_data["adTtmTemp"]))
            if form1.cleaned_data["targetBP"] == None:
                izracunana_polja.append(("targetBP", form1.cleaned_data["adTargetBP"]))
            if form1.cleaned_data["ph"] == None:
                izracunana_polja.append(("ph", form1.cleaned_data["adPh"]))
            if form1.cleaned_data["lactate"] == None:
                izracunana_polja.append(("lactate", form1.cleaned_data["adLactate"]))
            if form1.cleaned_data["shocks"] == None:
                izracunana_polja.append(("shocks", form1.cleaned_data["adShocks"]))
            if form1.cleaned_data["hospitalName"] == None:
                izracunana_polja.append(("hospitalName", form1.cleaned_data["adHospitalName"]))
            if form1.cleaned_data["estimatedAgeBystander"] == None:
                izracunana_polja.append(("estimatedAgeBystander", form1.cleaned_data["adBystAge"]))
            
            field_list = [(field, form1.cleaned_data[field]) for field in list(filter(lambda x: (x not in ["estimatedCAtimestamp"] + not_dcz), first_form))] + izracunana_polja
            # field_list = list(map(lambda x: (x[0], None) if x[1] == -9999 else x, field_list))
            
            print(field_list)

            case = CaseReport.objects.all().filter(dispatchID__exact=dispatch_id)
            if len(case) == 0:
                doctor_name = form1.cleaned_data["doctorName"] + " - 1.1 - " + str(datetime.now())
                CaseReport.objects.update_or_create(
                    # caseID=id,
                    dispatchID=dispatch_id, 
                    defaults=dict(list(filter(lambda x: x != "doctorName", field_list)) + [("doctorName", doctor_name)])
                )
            else:
                doctor_name = case[0].doctorName
                new_name = doctor_name + ", " + form1.cleaned_data["doctorName"] + " - 1.1 - " + str(datetime.now())
                # new_name = doctor_name + ", " + form1.cleaned_data["doctorName"] + " - 1.1 - " + str(datetime.datetime.now())
                CaseReport.objects.update_or_create(
                    # caseID=id,
                    dispatchID=dispatch_id, 
                    defaults=dict(list(filter(lambda x: x != "doctorName", field_list)) + [("doctorName", new_name)])
                ) 

            
                
        else:
            print("form invalid")

            messages.error(request, 'Nepravilno izpolnjen obrazec.')
            
            print(list(form1.errors))
            print(form1.errors)
            messages.error(request, form1.errors)
            

    final = {"form1":form1, "form2":form2}
    final.update(context)
    print(context)
    return render(request, "ohca/form_page.html", final)


def second_first_form_name_view(request):
    form1 = NDSZ_1_DAN()

    if request.method == "POST":
        form1 = NDSZ_1_DAN(request.POST)
        print(form1.errors)

        if form1.is_valid(): # and form2.is_valid():

            if form1.cleaned_data["name"] == None:
                messages.error(request, "poskus")

            else:
                print("VALIDATION SUCCESS")

                messages.success(request, 'Podatki uspešno oddani!')

                izracunana_polja = []
                
                first_name = (form1.cleaned_data['name']).strip().split(" ")
                last_name = (form1.cleaned_data['surname']).strip().split(" ")
                date = str(form1.cleaned_data['dateOfCA'])
                date_time = str(form1.cleaned_data["reaTimestamp"])

                print((date, date_time))
                print((first_name, last_name))

                id = generate_case_id(first_name, last_name, date, date_time)
                form1.instance.caseID = id 

                #======================= SAME FOR BOTH FORMS ==================================

                birth = form1.cleaned_data['dateOfBirth']
                estimAge = form1.cleaned_data['estimatedAge']

                if birth != None and estimAge == None:

                    calculated_age = calculate_age(str(birth), date)
                    izracunana_polja.append(("age", calculated_age))

                elif birth != None and estimAge != None: 
                    pass # TODO 

                # handle multipleselect fields separately
                # drugs = form1.cleaned_data['allDrugs']
                # drugs = list(map(lambda x: int(x), drugs))
                # print((drugs, sum(drugs)))
                # if drugs:
                #     izracunana_polja.append(("drugs", sum(drugs)))

                # airway = form1.cleaned_data['airway']
                # airway = list(map(lambda x: int(x), airway))
                # print((airway, sum(airway)))
                # if airway:
                #     izracunana_polja.append(("airwayControl", sum(airway)))

                y, m, d = date.split("-")

                izracunana_polja.append(("reaYr", int(y)))
                izracunana_polja.append(("reaMo", int(m)))
                izracunana_polja.append(("reaDay", int(d)))

                # izracunana_polja.append(("dispatchID", generate_dispatch_id(str(intID), date)))

                izracunana_polja.append(("reaLand", "Slovenia"))
                izracunana_polja.append(("reaRegion", str(form1.cleaned_data["localID"])))
                
                izracunana_polja.append(("localID", Locale.objects.all().filter(friendlyName__exact=form1.cleaned_data["localID"])[0]))
                izracunana_polja.append(("systemID", System.objects.all().filter(friendlyName__exact=form1.cleaned_data["systemID"])[0]))

                if form1.cleaned_data["ttmTemp"] == None:
                    izracunana_polja.append(("ttmTemp", form1.cleaned_data["adTtmTemp"]))
                if form1.cleaned_data["targetBP"] == None:
                    izracunana_polja.append(("targetBP", form1.cleaned_data["adTargetBP"]))
                if form1.cleaned_data["ph"] == None:
                    izracunana_polja.append(("ph", form1.cleaned_data["adPh"]))
                if form1.cleaned_data["lactate"] == None:
                    izracunana_polja.append(("lactate", form1.cleaned_data["adLactate"]))
                if form1.cleaned_data["shocks"] == None:
                    izracunana_polja.append(("shocks", form1.cleaned_data["adShocks"]))
                

                #========================= CALCULATE TIME INTERVALS ===================================================

                callTimestamp = form1.cleaned_data["callTimestamp"]
                timestamps = list(filter(lambda x: x != "treatmentWithdrawnTimestamp", timeline[2:])) # remove reaTimestamp and callTimestamp
                print(timestamps)
                if callTimestamp != None:
                    beginning = callTimestamp
                    for elt in timestamps:
                        time = form1.cleaned_data[elt]
                        seconds = calcSeconds(time, beginning)
                        izracunana_polja.append((timestamp_dict[elt], seconds))

                #=====================================================================


                # id = generate_case_id("".join(first_name), "".join(last_name), date, date_birth)
                print(id)
                field_list = [(field, form1.cleaned_data[field]) for field in list(filter(lambda x: (x not in ["estimatedCAtimestamp"]), first_form))] + izracunana_polja
                field_list = list(map(lambda x: (x[0], None) if x[1] == -9999 else x, field_list))
                

                case = CaseReport.objects.all().filter(caseID__exact=id)
                if len(case) == 0:
                    doctor_name = form1.cleaned_data["doctorName"] + " - 1.2 - " + str(datetime.now())
                    CaseReport.objects.update_or_create(
                        # caseID=id,
                        caseID=id, 
                        defaults=dict(list(filter(lambda x: x != "doctorName", field_list)) + [("doctorName", doctor_name)])
                    )
                else:
                    doctor_name = case[0].doctorName
                    new_name = doctor_name + ", " + form1.cleaned_data["doctorName"] + " - 1.2 - " + str(datetime.now())
                    # new_name = doctor_name + ", " + form1.cleaned_data["doctorName"] + " - 1.1 - " + str(datetime.datetime.now())
                    CaseReport.objects.update_or_create(
                        # caseID=id,
                        caseID=id, 
                        defaults=dict(list(filter(lambda x: x != "doctorName", field_list)) + [("doctorName", new_name)])
                    ) 


                # CaseReport.objects.update_or_create(
                #     caseID=id, 
                #     defaults=dict(field_list)#dict([(field, form1.cleaned_data[field]) for field in first_form] + izracunana_polja)
                # )
        else:
            print("form invalid")
            messages.error(request, 'Nepravilno izpolnjen obrazec.')
            messages.error(request, form1.errors)
    else:
        form1 = NDSZ_1_DAN() 
        # form2 = TimestampForm()
    return render(request, "ohca/second_first_formpage.html", {"form1":form1})


def second_form_name_view(request):
    form1 = MySecondNewFrom() 
    form2 = InterventionForm2()
    if request.method == "POST":

        form1 = MySecondNewFrom(request.POST)
        print(form1.errors)
        
        form2 = InterventionForm2(request.POST)

        if form1.is_valid() and form2.is_valid(): 
            
            print("VALIDATION SUCCESS")

            

            izracunana_polja = []

            f = ["i1",'i2','i3','i4','i5','i6','i7','i8','i9','i10','i11','i12',] #
            intID = '' 
            for field in f:
                if field != None:
                    intID += str(form2.cleaned_data[field])
            print(intID)

            if len(intID) != 12 and form1.cleaned_data["reaTimestamp"] == None:
                # raise ValidationError("Izpolnite ali intervencijsko številko ali naslednje podatke: ime, priimek, datum dogodka, čas dogodka")
                messages.error(request, 'Izpolnite ali intervencijsko številko ali naslednje podatke: ime, priimek, datum dogodka, čas dogodka.')
                # messages.error(request, form1.errors)
            else:
                messages.success(request, 'Podatki uspešno oddani!')
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
                if disch_date != 'None':
                    disch_date = disch_date.split("-")
                    izracunana_polja.append(("dischYear", disch_date[0]))
                    izracunana_polja.append(("dischMonth", disch_date[1]))
                    izracunana_polja.append(("dischDay", disch_date[2]))
                # form.instance.age = calculate_age(date_birth, date) # age bo že od prej

                if form1.cleaned_data["survivalDischarge"] == 1 or form1.cleaned_data["survival30d"] == 1:
                    izracunana_polja.append(("SurvivalDischarge30d", 1))
                
                # izracunana_polja.append(("localID", Locale.objects.all().filter(friendlyName__exact=form1.cleaned_data["localID"])[0]))
                # izracunana_polja.append(("systemID", System.objects.all().filter(friendlyName__exact=form1.cleaned_data["systemID"])[0]))
                
                field_list = [(field, form1.cleaned_data[field]) for field in list(filter(lambda x: (x not in ["drugs", "airwayControl", "systemID", "localID"]), second_form))] + izracunana_polja
                field_list = list(map(lambda x: (x[0], None) if x[1] == -9999 else x, field_list))
                
                print(len(intID))
                if len(intID) != 12:
                    print(str(form1.cleaned_data["reaTimestamp"]))
                    id = generate_case_id(first_name, last_name, date, str(form1.cleaned_data["reaTimestamp"]))
                    print(id)
                    case = CaseReport.objects.all().filter(caseID__exact=id)
                    print(case)
                    if len(case) == 0:
                        doctor_name = form1.cleaned_data["doctorName"] + " - 2 - " + str(datetime.now())
                        CaseReport.objects.update_or_create(
                            caseID=id,
                            # dispatchID=dispatch_id, 
                            defaults=dict(list(filter(lambda x: x != "doctorName", field_list)) + [("doctorName", doctor_name)])
                        )
                    else:
                        doctor_name = case[0].doctorName
                        new_name = doctor_name + ", " + form1.cleaned_data["doctorName"] + " - 2 - " + str(datetime.now())
                        # new_name = doctor_name + ", " + form1.cleaned_data["doctorName"] + " - 2 - " + str(datetime.datetime.now())
                        CaseReport.objects.update_or_create(
                            caseID=id,
                            # dispatchID=dispatch_id, 
                            defaults=dict(list(filter(lambda x: x != "doctorName", field_list)) + [("doctorName", new_name)])
                        ) 
                    # CaseReport.objects.update_or_create(
                    #     caseID=id, 
                    #     # dispatchID=dispatch_id,
                    #     defaults=dict(field_list)#dict([(field, form1.cleaned_data[field]) for field in second_form]+ izracunana_polja)
                    # ) # update, create
                else:
                    dispatch_id = generate_dispatch_id(str(intID), date)

                    case = CaseReport.objects.all().filter(dispatchID__exact=dispatch_id)
                    if len(case) == 0:
                        doctor_name = form1.cleaned_data["doctorName"] + " - 2 - " + str(datetime.now())
                        CaseReport.objects.update_or_create(
                            # caseID=id,
                            dispatchID=dispatch_id, 
                            defaults=dict(list(filter(lambda x: x != "doctorName", field_list)) + [("doctorName", doctor_name)])
                        )
                    else:
                        doctor_name = case[0].doctorName
                        new_name = doctor_name + ", " + form1.cleaned_data["doctorName"] + " - 2 - " + str(datetime.now())
                        # new_name = doctor_name + ", " + form1.cleaned_data["doctorName"] + " - 1.1 - " + str(datetime.datetime.now())
                        CaseReport.objects.update_or_create(
                            # caseID=id,
                            dispatchID=dispatch_id, 
                            defaults=dict(list(filter(lambda x: x != "doctorName", field_list)) + [("doctorName", new_name)])
                        ) 
                    # CaseReport.objects.update_or_create(
                    #     # caseID=id, 
                    #     dispatchID=dispatch_id,
                    #     defaults=dict(field_list)#dict([(field, form1.cleaned_data[field]) for field in second_form]+ izracunana_polja)
                    # ) # update, create
                

        else:
            print("form invalid")
            messages.error(request, 'Nepravilno izpolnjen obrazec.')
            messages.error(request, form1.errors)
    else:
        form1 = MySecondNewFrom() 
        form2 = InterventionForm2()
    return render(request, "ohca/second_form_page.html", {"form1":form1, "form2":form2})


