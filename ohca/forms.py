from time import time
from django import forms
from django.core import validators
# from matplotlib import widgets
from .models import *
from django.utils.translation import gettext_lazy as _
import hashlib
from .fields import *


#========================================== USEFUL DATA =================================================================================

from .auxiliary import values, titles, descriptions, first_form, second_form, timestamps, utstein, eureca, utstein_and_eureca


first_form = [
	#'age', -> računa samodejno iz datuma rojstva
	'gender', 
	'reaConf', 
	'pathogenesis', # patogeneza = vzrok
	#'confirmedCA', -> isto kot reaConf 
	'reaCause', # -> isto kot patogeneza?
	'location', 
	'diedOnField', 
	"deadOnArrival",
	'witnesses', 
	'bystanderResponse', 
	'bystanderAED', 
	'gbystnader', 'ageBystander', 
	#'responseTime', 'defibTime', -> se zračuna iz podatka o callTimestampu, namesto tega:
	"responseTimestamp", 
	'cPRbystander3Timestamp', #'cPRbystander3Time'
	'helperCPR', 'helperWho', #'persCPRstart', -> polje za dodat v models
	'cPRhelper3Timestamp', #'cPRhelper3Time',
	'endCPR4Timestamp',
	'defiOrig', #'AEDShock', 
	'defibTimestamp', 
	'shocks',
	'cprEms', 
	'noCPR',
	'cprQuality',
	'rosc', 
	'roscTimestamp', 
	'firstMonitoredRhy', 
	'independentLiving', 
	'comorbidities', 
	'vad', 
	'cardioverterDefib', 
	'stemiPresent', 
	'ttm', 'ttmTemp', 
	"drugs", 'drugTimingsTimestamp',  
	'airwayControl', 
	'vascularAccess',
	'mechanicalCPR', 
	'targetVent', 
	'reperfusionAttempt', 
	'ecls', 'iabp', 'ph', 
	'lactate', 'glucose', 'ecg', 'targetBP', 
	'transportToHospital', 
	# 'reaYr', 'reaMo', 'reaDay', 'reaTime', -> samodejno se izracuna iz datuma dogodka
	 #'leftScene5Time', 
	'leftScene5Timestamp', 
	'hospitalArrival6Timestamp', # 'hospitalArrival6Time',
 	'hospArri'
 ] 



# # spodnja polja morajo biti samodejno poračunana
exclude_first = (
	"age", 
	'responseTime', # rabimo call timestamt
	# 'drugs', # TODO widget multiple select
	'defibTime', 
	'reaTime', 
	'timeTCPR', 
	'cPRhelper3Time', 
	#'endCPR4Timestamp', 
	'leftScene5Time', 
	#'leftScene5Timestamp', 
	'hospitalArrival6Time',
	"reaYr",
	"reaMo",
	"reaDay",
	"reaTime")

# first_form = list(filter(lambda x: x not in exclude_first, first_form))



first_form = ["localID", "systemID"] + first_form
# # first_form += ["responseTimestamp", "defibTimestamp", "roscTimestamp", "reaTimestamp", "cPRbystander3Time", "endCPR4Timestamp", "leftScene5Timestamp", "hospitalArrival6Timestamp"]
# #

# second_form = ['neuroprognosticTests', 'survived', 'survival30d', 
# 'survivalDischarge', 'SurvivalDischarge30d', 'cpcDischarge', 'treatmentWithdrawn', 
# 'treatmentWithdrawnTimestamp', 'cod', 'organDonation', 
# 'patientReportedOutcome', 'qualityOfLife', 'dischDay', 
# 'dischMonth', 'dischYear']

second_form = [
	'survival30d', 
	"survivalDischarge", 
	#'SurvivalDischarge30d', -> zračunamo iz zgornjih dveh
	'survived12m',
	'neuroprognosticTests', 
	 
	'cpcDischarge', 
	'hospDisc', 
	'treatmentWithdrawn', 
	'treatmentWithdrawnhours', 
	'treatmentWithdrawnTimestamp', 
	'cod', 
	'organDonation', 
	'patientReportedOutcome', 
	'qualityOfLife', 
	'dischDay', 'dischMonth', 'dischYear']

# TODO v models
# second_form.remove("survived12m")
second_form.remove("hospDisc")
# second_form.remove("treatmentWithdrawnhours")

exclude_second = [
	"SurvivalDischarge30d",
	"dischDay",
	"dischMonth",
	"dischYear",
	"treatmentWithdrawn"
]

second_form = list(filter(lambda x: x not in exclude_second, second_form))
second_form = ["localID", "systemID"] + second_form

# treba ločit med DateTime timestampi in integer Time (sekunde)
timestamp_dict = {
	"bystanderResponseTimestamp" : "bystanderResponseTime",
	"bystanderAEDTimestamp" : "bystanderAEDTime", #cPRbystander3Time",
	"responseTimestamp" : "responseTime",
	"defibTimestamp" : "defibTime",
	"drugTimingsTimestamp" : "drugTimings",
	"reperfusionTimestamp" : "reperfusionTime",
	"roscTimestamp" : "roscTime",
	"treatmentWithdrawnTimestamp" : "treatmentWithdrawn",
	"reaTimestamp" : "reaTime",
	"timestampTCPR" : "timeTCPR",
	"cPRbystander3Timestamp" : "cPRbystander3Time",
	"cPRhelper3Timestamp" : "cPRhelper3Time",
	"timestampROSC" : "timeROSC",
	"endCPR4Timestamp" : "endCPR4Time",
	"leftScene5Timestamp" : "leftScene5Time",
	"hospitalArrival6Timestamp" : "hospitalArrival6Time",
	"cPREMS3Timestamp" : 'cPREMS3Time'
}

timestamps = [
	'callTimestamp', 
	'CAtimestamp', 
	'cPRhelper3Timestamp',
	'endCPR4Timestamp', 
	# 'bystanderResponseTimestamp', 
	'bystanderAEDTimestamp', 
	'responseTimestamp', 
	'defibTimestamp', 
	'drugTimingsTimestamp', 
	'reperfusionTimestamp', 
	'roscTimestamp',
	 'treatmentWithdrawnTimestamp', 
	#'cPREMS3Timestamp', 
	#'reaTimestamp', 
	# 'timestampTCPR', 
	# 'cPRbystander3Timestamp', 
	 
	#'timestampROSC', 
	
	'leftScene5Timestamp', 
	'hospitalArrival6Timestamp']

all_form = first_form + second_form + ["interventionID", "mainInterventionID"]

#======================================== USEFUL FUNCTIONS ==================================================================================


def generate_case_id(first_name: str, last_name: str, cardiac_arrest_date: str, birth_date: str):
	"""Takes the name, surname and dates in format recieved from input from form: 2020-02-03 (year, month, day) and generates ID"""

	# poskrbi za primer več imen in poenoti velike začetnice
	name = ""
	for i in range(len(first_name)):
		name += first_name[i][0].upper() + first_name[i][1:].lower()

	surname = ""
	for i in range(len(last_name)):
		surname += last_name[i][0].upper() + last_name[i][1:].lower()

	# split 
	cardiac_arrest_date = cardiac_arrest_date.split("-")
	birth_date = birth_date.split("-")

	ca_date = cardiac_arrest_date[2] + cardiac_arrest_date[1] + cardiac_arrest_date[0]
	birth_date = birth_date[2] + birth_date[1] + birth_date[0]
	
	code = name + ca_date + surname + birth_date
	print(code)
	hashed = hashlib.sha256(code.encode("utf-8")).hexdigest() #hexdigest
	return hashed

def generate_dispatch_id(intervention_num: str, cardiac_arrest_date: str):
	cardiac_arrest_date = cardiac_arrest_date.split("-")
	ca_date = cardiac_arrest_date[2] + cardiac_arrest_date[1] + cardiac_arrest_date[0]
	
	code = intervention_num + ca_date
	return hashlib.sha256(code.encode("utf-8")).hexdigest()


def create_widgets(values, timestamps): 
	w, w_times = dict(), dict()
	for element in values:
		w[element] = forms.RadioSelect(choices=values[element])#, attrs={"class" : "with-gap", "type" : "radio"}) #attrs={'class': "form-check-input", "type" : "radio"})
		# w[element] = "radio"
	# for element in timestamps:
	# 	w_times[element] = DateTimeSelector
	# return (w, w_times) 
	for element in timestamps:
		w[element] = DateTimeSelector()
	return w


w = create_widgets(values, timestamps) #
w["ecgBLOB"] = forms.FileInput(attrs={"class" : "form-control", "type" : "file"})
w["estimatedAgeBystander"] = forms.CheckboxInput
w["estimatedCAtimestamp"] = forms.CheckboxInput
# w["drugs"] = forms.MultipleChoiceField(label="Aplicirana zdravila",widget=forms.CheckboxSelectMultiple,choices=values['drugs'], required=False)

# ========================================== FORMS ================================================================================

from django import forms

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column
# from ohca import fields


class InterventionForm(forms.Form):
	"""Form for 12 separate fields for the intervention number"""

	i1 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}))
	i2 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}))
	i3 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}))
	i4 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}))
	i5 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}))
	i6 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}))
	i7 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}))
	i8 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}))
	i9 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}))
	i10 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}))
	i11 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}))
	i12 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}))

	# TODO
	#interventionID = fields.InterventionField()

	# https://simpleisbetterthancomplex.com/tutorial/2018/11/28/advanced-form-rendering-with-django-crispy-forms.html

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		fields = ["i1",'i2','i3','i4','i5','i6','i7','i8','i9','i10','i11','i12',]
		#fields = ["interventionID"]

		for f in fields:
			self.fields[f].label = False

class TimestampForm(forms.ModelForm):

	class Meta:
		model = CaseReport
		fields = tuple(timestamps)
		exclude = ("cPREMS3Timestamp", ) 
		widgets= w
		labels = titles
		help_texts = descriptions
	

	

class MyNewFrom(forms.ModelForm):
	
	Patient_name = forms.CharField(label="Ime pacienta")
	Patient_surname = forms.CharField(label="Priimek pacienta")
	Date = forms.DateField(label='Datum srčnega zastoja', widget=DatePickerInput())
	Time = forms.TimeField(label="Čas srčnega zastoja", widget=TimePickerInputSeconds(format='%H:%M:%S', attrs={'type': 'time', 'step' : 1}), required=False)
	estim_time = forms.BooleanField(label="Označite, če je čas srčnega zastoja le ocenjen.", widget=forms.CheckboxInput(), required=False)
	Date_birth = forms.DateField(label='Datum rojstva', widget=DatePickerInput())
	estim_age = forms.BooleanField(label="Označite, če je starost očividca le ocenjena.", widget=forms.CheckboxInput(), required=False)

	All_drugs = forms.MultipleChoiceField(label="Aplicirana zdravila", widget=forms.CheckboxSelectMultiple,choices=values['drugs'], required=False)
	# Estimated_bystander_age = forms.ChoiceField(label="Ali je starost očividca ocenjena?", widget=forms.CheckboxInput)

	class Meta: 	
		model = CaseReport
		fields = tuple(first_form)		
		# exclude = ("age", 'responseTime', 'responseTime', 'defibTime','reaTime', 'timeTCPR', 'cPRhelper3Time', 'endCPR4Timestamp', 'leftScene5Time', 'leftScene5Timestamp', 'hospitalArrival6Time',)
		# ("caseID", "reaLand", "drugs", "age", "dischDay") 
		exclude = ("bystanderAEDTime",)
		widgets = w
		labels = titles
		help_texts = descriptions

	# def __init__(self, *args, **kwargs):
	# 	super(MyNewFrom, self).__init__(*args, **kwargs)
	# 	for elt in timestamps:
	# 		if elt in first_form:
	# 			self.fields[elt].required = False

	
class MySecondNewFrom(forms.ModelForm):

	Patient_name = forms.CharField(label="Ime pacienta")
	Patient_surname = forms.CharField(label="Priimek pacienta")
	# Date = forms.DateField(label='Datum srčnega zastoja', widget=forms.SelectDateWidget(months=MONTHS, years=[x for x in range(2020,2025)]))
	Date = forms.DateField(label='Datum srčnega zastoja', widget=DatePickerInput())
	# Date_birth = forms.DateField(label='Datum rojstva', widget=forms.SelectDateWidget(years=[x for x in range(1910,2025)], months=MONTHS))
	Date_birth = forms.DateField(label='Datum rojstva', widget=DatePickerInput)

	Date_of_hospital_discharge = forms.DateField(label='Datum odpusta iz bolnišnice', widget=DatePickerInput, required=False)

	class Meta: #
		model = CaseReport
		fields = tuple(second_form)		
		# exclude = ("caseID", "reaLand", "age", "dischDay")
		# exclude = ("dispatchID", "interventionID", "mainInterventionID", ) 
		widgets = w
		labels = titles
		help_texts = descriptions
		
# nekej na to temo : https://docs.djangoproject.com/en/dev/ref/forms/validation/


class MyThirdNewFrom(forms.ModelForm):

	Patient_name = forms.CharField(label="Ime pacienta")
	Patient_surname = forms.CharField(label="Priimek pacienta")
	# Date = forms.DateField(label='Datum srčnega zastoja', widget=forms.SelectDateWidget(months=MONTHS, years=[x for x in range(2020,2025)]))
	Date = forms.DateField(label='Datum srčnega zastoja', widget=DatePickerInput())
	# Time = forms.TimeField(label="Čas srčnega zastoja", widget=TimeWidgetSeconds)
	Time = forms.TimeField(label="Čas srčnega zastoja", widget=TimePickerInputSeconds(format='%H:%M:%S', attrs={'type': 'time', 'step' : 1}))
	# Date_birth = forms.DateField(label='Datum rojstva', widget=forms.SelectDateWidget(years=[x for x in range(1910,2025)], months=MONTHS))
	Date_birth = forms.DateField(label='Datum rojstva', widget=DatePickerInput)
	estim_time = forms.BooleanField(label="Označite, če je čas srčnega zastoja le ocenjen.", widget=forms.CheckboxInput(), required=False)
	Date_of_hospital_discharge = forms.DateField(label='Datum odpusta iz bolnišnice', widget=DatePickerInput, required=False)

	# poskus = forms.DateTimeField(label="poskus", widget=DateTimeSelector)

	All_drugs = forms.MultipleChoiceField(label="Aplicirana zdravila",widget=forms.CheckboxSelectMultiple,choices=values['drugs'], required=False)
	#Estimated_bystander_age = forms.ChoiceField(label="Ali je starost očividca ocenjena?", widget=forms.CheckboxInput)
	class Meta: 
		model = CaseReport
		fields = tuple(all_form)		
		# exclude = ("caseID", "reaLand", "age", "dischDay", "dispatchID") 
		widgets = w
		labels = titles
		help_texts = descriptions


