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

            # we need to store values for fields that are not filled in the form but calculated
            izracunana_polja = []

            # --------------- intervention ID & dispatch ID ---------------------------------
            f = ["i1",'i2','i3','i4','i5','i6','i7','i8','i9','i10','i11','i12'] 
            intID = '' 
            for field in f:
                intID += str(form2.cleaned_data[field])
            print(intID)

            izracunana_polja.append(("interventionID", intID))
            izracunana_polja.append(("mainInterventionID", intID))

            date = str(form1.cleaned_data['dateOfCA'])

            # ids in this form are identified by dispatch id
            dispatch_id = generate_dispatch_id(str(intID), date)

            # If possible calculate a caseID as well
            missingNonIdData = form1.cleaned_data["name"] == None or form1.cleaned_data["surname"] == None or form1.cleaned_data["reaTimestamp"] == None or form1.cleaned_data["dateOfCA"] == None
            if not missingNonIdData:
                first_name = (form1.cleaned_data['name']).title().strip().split(" ")
                last_name = (form1.cleaned_data['surname']).title().strip().split(" ")
                izracunana_polja.append(
                    ("caseID", generate_case_id(first_name, last_name, date, str(form1.cleaned_data["reaTimestamp"])))
                )
            
            # -------------- age -------------------------------
            birth = form1.cleaned_data['dateOfBirth']
            estimAge = form1.cleaned_data['estimatedAge']

            if birth != None: # and estimAge == None:
                calculated_age = calculate_age(str(birth), date)
                izracunana_polja.append(("age", calculated_age))

            elif birth != None and estimAge != None: 
                pass # will not happen because we handled this in formValidation.js

            # ----------------- trivial info -----------------------
            y, m, d = date.split("-")

            izracunana_polja.append(("reaYr", int(y)))
            izracunana_polja.append(("reaMo", int(m)))
            izracunana_polja.append(("reaDay", int(d)))

            izracunana_polja.append(("reaLand", "Slovenia"))
            izracunana_polja.append(("reaRegion", str(form1.cleaned_data["localID"])))
            
            izracunana_polja.append(("localID", Locale.objects.all().filter(friendlyName__exact=form1.cleaned_data["localID"])[0]))
            izracunana_polja.append(("systemID", System.objects.all().filter(friendlyName__exact=form1.cleaned_data["systemID"])[0]))
            
            # --------------- string fields with extra radio options ----------------------

            # we know that either the string field will be filled or one of the radio options
            # both can't happen because formValidation.js prevents it
            # if form1.cleaned_data["ttmTemp"] == None:
            #     izracunana_polja.append(("ttmTemp", form1.cleaned_data["adTtmTemp"]))
            # if form1.cleaned_data["targetBP"] == None:
            #     izracunana_polja.append(("targetBP", form1.cleaned_data["adTargetBP"]))
            # if form1.cleaned_data["ph"] == None:
            #     izracunana_polja.append(("ph", form1.cleaned_data["adPh"]))
            # if form1.cleaned_data["lactate"] == None:
            #     izracunana_polja.append(("lactate", form1.cleaned_data["adLactate"]))
            if form1.cleaned_data["shocks"] == None:
                izracunana_polja.append(("shocks", form1.cleaned_data["adShocks"]))
            if form1.cleaned_data["hospitalName"] == None:
                izracunana_polja.append(("hospitalName", form1.cleaned_data["adHospitalName"]))
            if form1.cleaned_data["estimatedAgeBystander"] == None:
                izracunana_polja.append(("estimatedAgeBystander", form1.cleaned_data["adBystAge"]))
            
            # ---------------- saving the form -----------------------------------------
            field_list = [(field, form1.cleaned_data[field]) for field in list(filter(lambda x: (x not in ["estimatedCAtimestamp"] + not_dcz), first_form))] + izracunana_polja

            # we want to know who and when filled out the form and also which form
            # we save this in the doctorName variable - they fill out their name, we add timestamp + (1.1) for this form

            case = CaseReport.objects.all().filter(dispatchID__exact=dispatch_id)
            # we have to check if any of the cases already exist
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
    return render(request, "ohca/form_page.html", final)


def second_first_form_name_view(request):
    form1 = NDSZ_1_DAN()

    if request.method == "POST":
        form1 = NDSZ_1_DAN(request.POST)
        print(form1.errors)

        if form1.is_valid(): # and form2.is_valid():

            print("VALIDATION SUCCESS")

            messages.success(request, 'Podatki uspešno oddani!')

            izracunana_polja = []

            # ------------ generating case id -------------------------
            
            first_name = (form1.cleaned_data['name']).title().strip().split(" ")
            last_name = (form1.cleaned_data['surname']).title().strip().split(" ")
            date = str(form1.cleaned_data['dateOfCA'])
            date_time = str(form1.cleaned_data["reaTimestamp"])

            id = generate_case_id(first_name, last_name, date, date_time)
            form1.instance.caseID = id 

            # ------------- calculating age ---------------------------

            birth = form1.cleaned_data['dateOfBirth']
            estimAge = form1.cleaned_data['estimatedAge']

            if birth != None:
                calculated_age = calculate_age(str(birth), date)
                izracunana_polja.append(("age", calculated_age))

            # ---------------- trivial ---------------------

            y, m, d = date.split("-")

            izracunana_polja.append(("reaYr", int(y)))
            izracunana_polja.append(("reaMo", int(m)))
            izracunana_polja.append(("reaDay", int(d)))

            izracunana_polja.append(("reaLand", "Slovenia"))
            izracunana_polja.append(("reaRegion", str(form1.cleaned_data["localID"])))
            
            izracunana_polja.append(("localID", Locale.objects.all().filter(friendlyName__exact=form1.cleaned_data["localID"])[0]))
            izracunana_polja.append(("systemID", System.objects.all().filter(friendlyName__exact=form1.cleaned_data["systemID"])[0]))

            # -------------------- string fields with extra radio buttons ----------------------------
            # if form1.cleaned_data["ttmTemp"] == None:
            #     izracunana_polja.append(("ttmTemp", form1.cleaned_data["adTtmTemp"]))
            # if form1.cleaned_data["targetBP"] == None:
            #     izracunana_polja.append(("targetBP", form1.cleaned_data["adTargetBP"]))
            # if form1.cleaned_data["ph"] == None:
            #     izracunana_polja.append(("ph", form1.cleaned_data["adPh"]))
            # if form1.cleaned_data["lactate"] == None:
            #     izracunana_polja.append(("lactate", form1.cleaned_data["adLactate"]))
            if form1.cleaned_data["shocks"] == None:
                izracunana_polja.append(("shocks", form1.cleaned_data["adShocks"]))
            if form1.cleaned_data["hospitalName"] == None:
                izracunana_polja.append(("hospitalName", form1.cleaned_data["adHospitalName"]))
            if form1.cleaned_data["estimatedAgeBystander"] == None:
                izracunana_polja.append(("estimatedAgeBystander", form1.cleaned_data["adBystAge"]))
            

            #========================= CALCULATE TIME INTERVALS ===================================================

            # everything is dependent on the time of call recieved
            callTimestamp = form1.cleaned_data["callTimestamp"]
            timestamps = list(filter(lambda x: x not in ["treatmentWithdrawnTimestamp", "reaTimestamp", "callTimestamp"], timeline[2:])) # remove reaTimestamp and callTimestamp
            # print(timestamps)
            if callTimestamp != None:
                beginning = callTimestamp
                for elt in timestamps:
                    time = form1.cleaned_data[elt]
                    if time != None:
                        seconds = calcSeconds(time, beginning)
                        izracunana_polja.append((timestamp_dict[elt], seconds))

           #------------------ saving the form ---------------------------
            
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
                CaseReport.objects.update_or_create(
                    # caseID=id,
                    caseID=id, 
                    defaults=dict(list(filter(lambda x: x != "doctorName", field_list)) + [("doctorName", new_name)])
                ) 

        else:
            print("form invalid")
            messages.error(request, 'Nepravilno izpolnjen obrazec.')
            messages.error(request, form1.errors)
    else:
        form1 = NDSZ_1_DAN() 
        
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
                messages.error(request, 'Izpolnite ali intervencijsko številko ali naslednje podatke: ime, priimek, datum dogodka, čas dogodka.')
                
            else:
                messages.success(request, 'Podatki uspešno oddani!')
                
                
                first_name = (form1.cleaned_data['name']).strip().split(" ")
                last_name = (form1.cleaned_data['surname']).strip().split(" ")

                date = str(form1.cleaned_data['dateOfCA'])
                date_birth = str(form1.cleaned_data["dateOfBirth"])
                disch_date = str(form1.cleaned_data["discDate"])

                # if not (date and disch_date):
                # if date != None and disch_date != None:
                #     print(day_difference(date, disch_date))
                #     form1.instance.dischDay = day_difference(date, disch_date)

                if form1.cleaned_data["ttmTemp"] == None:
                    izracunana_polja.append(("ttmTemp", form1.cleaned_data["adTtmTemp"]))
                if form1.cleaned_data["targetBP"] == None:
                    izracunana_polja.append(("targetBP", form1.cleaned_data["adTargetBP"]))
                if form1.cleaned_data["ph"] == None:
                    izracunana_polja.append(("ph", form1.cleaned_data["adPh"]))
                if form1.cleaned_data["lactate"] == None:
                    izracunana_polja.append(("lactate", form1.cleaned_data["adLactate"]))

                print((date, date_birth))
                if disch_date != 'None':
                    disch_date = disch_date.split("-")
                    izracunana_polja.append(("dischYear", disch_date[0]))
                    izracunana_polja.append(("dischMonth", disch_date[1]))
                    izracunana_polja.append(("dischDay", disch_date[2]))
                
                if form1.cleaned_data["survivalDischarge"] == 1 or form1.cleaned_data["survival30d"] == 1:
                    izracunana_polja.append(("SurvivalDischarge30d", 1))
                
                if form1.cleaned_data["treatmentWithdrawnTimestamp"] == None:
                    izracunana_polja.append(("treatmentWithdrawnTimestamp", form1.cleaned_data["adWithdraw"]))

                field_list = [(field, form1.cleaned_data[field]) for field in list(filter(lambda x: (x not in ["drugs", "airwayControl", "systemID", "localID"]), second_form))] + izracunana_polja
                field_list = list(map(lambda x: (x[0], None) if x[1] == -9999 else x, field_list))
                
                if len(intID) != 12:
                    
                    id = generate_case_id(first_name, last_name, date, str(form1.cleaned_data["reaTimestamp"]))
                    
                    case = CaseReport.objects.all().filter(caseID__exact=id)
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
                        CaseReport.objects.update_or_create(
                            caseID=id,
                            # dispatchID=dispatch_id, 
                            defaults=dict(list(filter(lambda x: x != "doctorName", field_list)) + [("doctorName", new_name)])
                        ) 

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
                        CaseReport.objects.update_or_create(
                            # caseID=id,
                            dispatchID=dispatch_id, 
                            defaults=dict(list(filter(lambda x: x != "doctorName", field_list)) + [("doctorName", new_name)])
                        ) 

        else:
            print("form invalid")
            messages.error(request, 'Nepravilno izpolnjen obrazec.')
            messages.error(request, form1.errors)
    else:
        form1 = MySecondNewFrom() 
        form2 = InterventionForm2()
    return render(request, "ohca/second_form_page.html", {"form1":form1, "form2":form2})


def error_form_view(request):
    form1 = ErrorForm() 
    form2 = InterventionForm2()
    if request.method == "POST":

        form1 = ErrorForm(request.POST)
        print(form1.errors)
        
        form2 = InterventionForm2(request.POST)

        if form1.is_valid() and form2.is_valid(): 
            
            izracunana_polja = []

            # intervention ID
            f = ["i1",'i2','i3','i4','i5','i6','i7','i8','i9','i10','i11','i12',] #
            intID = '' 
            for field in f:
                if field != None:
                    intID += str(form2.cleaned_data[field])
            print(intID)


            # ------------- calculating age ---------------------------

            birth = form1.cleaned_data['dateOfBirth']

            date = str(form1.cleaned_data['dateOfCA'])
            if date != "None":
                if birth != None:
                    calculated_age = calculate_age(str(birth), date)
                    izracunana_polja.append(("age", calculated_age))

                y, m, d = date.split("-")

                izracunana_polja.append(("reaYr", int(y)))
                izracunana_polja.append(("reaMo", int(m)))
                izracunana_polja.append(("reaDay", int(d)))

            # izracunana_polja.append(("reaLand", "Slovenia"))

            if form1.cleaned_data["localID"] != None:
                izracunana_polja.append(("reaRegion", str(form1.cleaned_data["localID"])))
                obcina = form1.cleaned_data["localID"]
                if obcina != None:
                    izracunana_polja.append(("localID", Locale.objects.all().filter(friendlyName__exact=form1.cleaned_data["localID"])[0]))
            if form1.cleaned_data["systemID"] != None:
                system = form1.cleaned_data["systemID"]
                if system != None:
                    izracunana_polja.append(("systemID", System.objects.all().filter(friendlyName__exact=form1.cleaned_data["systemID"])[0]))
            

            # -------- rabimo ali podatek za intervention ID ali za case ID (ime, priimek, cas zastoja) ------------
            
            missingNonIdData = form1.cleaned_data["name"] == None or form1.cleaned_data["surname"] == None or form1.cleaned_data["reaTimestamp"] == None or form1.cleaned_data["dateOfCA"] == None
            
            cases = []
            if len(intID) != 12 and not missingNonIdData:
                first_name = (form1.cleaned_data['name']).strip().split(" ")
                last_name = (form1.cleaned_data['surname']).strip().split(" ")
                id = generate_case_id(first_name, last_name, str(form1.cleaned_data["dateOfCA"]), str(form1.cleaned_data["reaTimestamp"]))
                cases = CaseReport.objects.all().filter(caseID__exact=id)#[0]
            else:
                if form1.cleaned_data["dateOfCA"] == None:
                    date = "20" + str(intID)[2] + str(intID)[3] + "-" + str(intID)[4] + str(intID)[5] + "-" + str(intID)[6] + str(intID)[7]
                dispatch_id = generate_dispatch_id(str(intID), str(date))
                cases = CaseReport.objects.all().filter(dispatchID__exact=dispatch_id)#[0]

        
            if len(intID) != 12 and missingNonIdData:
                messages.error(request, 'Izpolnite ali intervencijsko številko ali naslednje podatke: ime, priimek, datum dogodka, čas dogodka.')

            #--------- posebej primer ko so polja izpolnjena in se zračuna ID ampak ID-ja ni v bazi -----------
            elif len(cases) == 0:
                messages.error(request, 'Tega primera ni v bazi! Preverite ali ste pravilno vnesli podatke!')
  
            else:
                messages.success(request, 'Podatki uspešno oddani!')

                if form1.cleaned_data['name'] != None:
                    first_name = (form1.cleaned_data['name']).title().strip().split(" ")
                if form1.cleaned_data['surname'] != None:
                    last_name = (form1.cleaned_data['surname']).title().strip().split(" ")
                
                if form1.cleaned_data['dateOfCA'] != None:
                    date = str(form1.cleaned_data['dateOfCA'])
                if form1.cleaned_data['dateOfBirth'] != None:
                    date_birth = str(form1.cleaned_data["dateOfBirth"])
                if form1.cleaned_data['discDate'] != None:
                    disch_date = str(form1.cleaned_data["discDate"])

            # ----------- vprašanja kjer je textfield in radio options ---------------
            # če je textfield izpolnjen se bo shranil, če pa je namesto textfielda obkljukan en od radio buttonov je treba to posebej shranit
            # hkrati ne more bit ker tega ne dovoli javascript
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
                
                # print((date, date_birth))
                if form1.cleaned_data['discDate'] != None:
                    disch_date = disch_date.split("-")
                    izracunana_polja.append(("dischYear", disch_date[0]))
                    izracunana_polja.append(("dischMonth", disch_date[1]))
                    izracunana_polja.append(("dischDay", disch_date[2]))
                
                if form1.cleaned_data["survivalDischarge"] == 1 or form1.cleaned_data["survival30d"] == 1:
                    izracunana_polja.append(("SurvivalDischarge30d", 1))
                
                if form1.cleaned_data["treatmentWithdrawnTimestamp"] == None:
                    izracunana_polja.append(("treatmentWithdrawnTimestamp", form1.cleaned_data["adWithdraw"]))

                
                field_list = [(field, form1.cleaned_data[field]) for field in list(filter(lambda x: (x not in ["systemID", "localID"]), second_form))] + izracunana_polja
                field_list += [(field, form1.cleaned_data[field]) for field in list(filter(lambda x: (x not in ["systemID", "localID"]), first_form))]

                # ------------------- call timestamp ---------------------------
                case = None
                if len(intID) == 12:
                    dispatch_id = generate_dispatch_id(str(intID), date)
                    case = CaseReport.objects.all().filter(dispatchID__exact=dispatch_id)[0]
                else:
                    id = generate_case_id(first_name, last_name, date, str(form1.cleaned_data["reaTimestamp"]))
                    case = CaseReport.objects.all().filter(caseID__exact=id)[0]

                # everything is dependent on the time of call recieved
                callTimestamp = form1.cleaned_data["callTimestamp"]
                caseAsDict = vars(case)
                if callTimestamp == None:
                    callTimestamp = case.callTimestamp
                timestamps = list(filter(lambda x: x not in ["treatmentWithdrawnTimestamp", "reaTimestamp", "callTimestamp"], timeline[2:])) # remove reaTimestamp and callTimestamp
                for timestampName in timestamps: 
                    timestamp = form1.cleaned_data[timestampName]
                    if timestamp == None:
                        timestamp = caseAsDict[timestampName]
                    if timestamp != None and callTimestamp != None:
                        duration = timestamp - callTimestamp
                        field_list.append((timestamp_dict[timestampName], duration.seconds))
                    

                # ----------------- doctor name + shranjevanje podatkov --------------------------------
                changes = dict()
                for (key, val) in field_list:
                    if val != None:
                        changes[key] = val

                doctor_name = form1.cleaned_data["doctorName"] + " - popravek - " + str(datetime.now())
                changes['doctorName'] = ", ".join(filter(None, (case.doctorName, doctor_name)))

                if len(intID) == 12:
                     CaseReport.objects.update_or_create(
                        dispatchID=dispatch_id, 
                        defaults=changes
                    )
                else:
                    CaseReport.objects.update_or_create(
                        caseID=id,
                        defaults=changes
                    )

        else:
            print("form invalid")
            messages.error(request, 'Nepravilno izpolnjen obrazec.')
            messages.error(request, form1.errors)
    else:#
        form1 = ErrorForm() 
        form2 = InterventionForm2()
    return render(request, "ohca/error_page.html", {"form1":form1, "form2":form2})