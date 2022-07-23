from time import time
from django import forms
from django.core import validators
# from matplotlib import widgets
from .models import *
from django.utils.translation import gettext_lazy as _
import hashlib
# from django.forms import HiddenInput, IntegerField, MultiWidget, NumberInput, TextInput
from .widget import *


#========================================== USEFUL DATA =================================================================================

from .auxiliary import values, titles, descriptions, first_form, second_form, timestamps, utstein, eureca, utstein_and_eureca


# bom zakomentirala to spodaj ko bom testirala

# first form with data immediately after CA
first_form = ['caseID', 'systemID', 'localID', 'callTimestamp', 'dispIdentifiedCA', 'dispProvidedCPRinst', 'gender', 'witnesses', 'location', 
'bystanderResponse', 'bystanderResponseTimestamp', 'bystanderAED', 'bystanderAEDTimestamp', 'deadOnArrival', 'firstMonitoredRhy', 'pathogenesis', 
'independentLiving', 'comorbidities', 'vad', 'cardioverterDefib', 'stemiPresent', 'responseTime', 'defibTime', 'ttm', 'ttmTemp',  
'airwayControl', 'cprQuality', 'shocks', 'drugTimings', 'vascularAccess', 'mechanicalCPR', 'targetVent', 'reperfusionAttempt', 
'reperfusionTime', 'rosc', 'roscTime', 'transportToHospital', 
'reaRegion', 'reaConf', 'cprEms', 'cPREMS3Time', 'noCPR', 'reaTime', 'reaCause', 'timeTCPR', 'gbystnader', 'ageBystander', 
'estimatedAgeBystander','cPRbystander3Time', 'helperCPR', 'helperWho', 'cPRhelper3Time', 'defiOrig', 'timeROSC', 'endCPR4Time', 
'leftScene5Time', 'hospitalArrival6Time', 'hospArri', "mainInterventionID", "interventionID", ]

# secodn form with data in the hospital 
second_form = ['systemID', 'localID', 'ecls', 'iabp', 'ph', 'lactate', 'glucose', 'neuroprognosticTests', 'specialistHospital', 'hospitalVolume', 'ecg', 
'ecgBLOB', 'targetBP', 'survived', 'SurvivalDischarge30d', 'cpcDischarge', 'mrsDischarge', 'survivalStatus', 'treatmentWithdrawn', 
'cod', 'organDonation', 'patientReportedOutcome', 'qualityOfLife'] + ["interventionID", "mainInterventionID"] #, 'dischDay']

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


def create_widgets(values): 
	w = dict()
	for element in values:
		w[element] = forms.RadioSelect(choices=values[element])#, attrs={"class" : "with-gap", "type" : "radio"}) #attrs={'class': "form-check-input", "type" : "radio"})
		# w[element] = "radio"
	return w 

values["estimatedAgeBystander"] = [("", 'Neznano'), (True, 'Da'), (False, 'Ne')]

# def create_time_widgets(values):
# 	w = dict()
# 	for elt in values:
# 		w[elt] = forms.TimeField(widget=TimePickerInput)
# 	return w

w = create_widgets(values) #
w["ecgBLOB"] = forms.FileInput(attrs={"class" : "form-control", "type" : "file"})



# ========================================== FORMS ================================================================================

from django import forms

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Submit, Row, Column
from ohca import fields


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


	# 	self.helper = FormHelper(self)
	# 	self.helper.layout = Layout(
	# 		Row(
	# 			Column('i1', css_class='form-group col-md-1 mb-0'),
	# 			Column('i2', css_class='form-group col-md-1 mb-0'),
	# 			Column('i3', css_class='form-group col-md-1 mb-0'),
	# 			Column('i4', css_class='form-group col-md-1 mb-0'),
	# 			Column('i5', css_class='form-group col-md-1 mb-0'),
	# 			Column('i6', css_class='form-group col-md-1 mb-0'),
	# 			Column('i7', css_class='form-group col-md-1 mb-0'),
	# 			Column('i8', css_class='form-group col-md-1 mb-0'),
	# 			Column('i9', css_class='form-group col-md-1 mb-0'),
	# 			Column('i10', css_class='form-group col-md-1 mb-0'),
	# 			Column('i11', css_class='form-group col-md-1 mb-0'),
	# 			Column('i12', css_class='form-group col-md-1 mb-0'),
	# 			css_class='form-row'
	# 		),
	# 		Submit("submit", "submit!")
	# 	)
	

class MyNewFrom(forms.ModelForm):
	
	Patient_name = forms.CharField(label="Ime pacienta")
	Patient_surname = forms.CharField(label="Priimek pacienta")
	# Date = forms.DateField(label='Datum srčnega zastoja', widget=forms.SelectDateWidget(months=MONTHS, years=[x for x in range(2020,2025)]))
	Date = forms.DateField(label='Datum srčnega zastoja', widget=DatePickerInput())
	Time = forms.TimeField(label="Čas srčnega zastoja", widget=TimeWidgetSeconds)
	# Date_birth = forms.DateField(label='Datum rojstva', widget=forms.SelectDateWidget(years=[x for x in range(1910,2025)], months=MONTHS))
	Date_birth = forms.DateField(label='Datum rojstva', widget=DatePickerInput())

	All_drugs = forms.MultipleChoiceField(label="Aplicirana zdravila", widget=forms.CheckboxSelectMultiple,choices=values['drugs'])
	# Estimated_bystander_age = forms.ChoiceField(label="Ali je starost očividca ocenjena?", widget=forms.CheckboxInput)

	class Meta: 	
		model = CaseReport
		fields = tuple(first_form)		
		exclude = ("caseID", "reaLand", "drugs"
		"age", 
		"dischDay") 
		widgets = w
		labels = titles
		help_texts = descriptions

	
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
		exclude = ("caseID", "reaLand", "age", "dischDay") 
		widgets = w
		labels = titles
		help_texts = descriptions
		
# nekej na to temo : https://docs.djangoproject.com/en/dev/ref/forms/validation/


class MyThirdNewFrom(forms.ModelForm):

	Patient_name = forms.CharField(label="Ime pacienta")
	Patient_surname = forms.CharField(label="Priimek pacienta")
	# Date = forms.DateField(label='Datum srčnega zastoja', widget=forms.SelectDateWidget(months=MONTHS, years=[x for x in range(2020,2025)]))
	Date = forms.DateField(label='Datum srčnega zastoja', widget=DatePickerInput())
	Time = forms.TimeField(label="Čas srčnega zastoja", widget=TimeWidgetSeconds)
	# Date_birth = forms.DateField(label='Datum rojstva', widget=forms.SelectDateWidget(years=[x for x in range(1910,2025)], months=MONTHS))
	Date_birth = forms.DateField(label='Datum rojstva', widget=DatePickerInput)
	
	Date_of_hospital_discharge = forms.DateField(label='Datum odpusta iz bolnišnice', widget=DatePickerInput, required=False)

	All_drugs = forms.MultipleChoiceField(label="Aplicirana zdravila",widget=forms.CheckboxSelectMultiple,choices=values['drugs'], required=False)
	#Estimated_bystander_age = forms.ChoiceField(label="Ali je starost očividca ocenjena?", widget=forms.CheckboxInput)
	class Meta: 
		model = CaseReport
		fields = "__all__"		
		exclude = ("caseID", "reaLand", "age", "dischDay", "drugs", "dispatchID") 
		widgets = w
		labels = titles
		help_texts = descriptions
