from random import choices
from time import time
from django import forms
from django.core import validators
# from matplotlib import widgets
from .models import *
from django.utils.translation import gettext_lazy as _
import hashlib
from .fields import *


#========================================== USEFUL DATA =================================================================================

from .auxiliary import values, titles, descriptions, first_form, second_form, dates, timestamps, not_dcz



# # treba ločit med DateTime timestampi in integer Time (sekunde)
timestamp_dict = {
	"timestampTCPR" : "timeTCPR",
	"cPRbystander3Timestamp" : "cPRbystander3Time",
	"defibTimestamp" : "defibTime",
	"cPRhelper3Timestamp" : "cPRhelper3Time",
	"responseTimestamp" : "responseTime",
	"cPREMS3Timestamp" : 'cPREMS3Time',
	"drugTimingsTimestamp" : "drugTimings",
	"roscTimestamp" : "roscTime",
	"endCPR4Timestamp" : "endCPR4Time",
	"leftScene5Timestamp" : "leftScene5Time",
	"hospitalArrival6Timestamp" : "hospitalArrival6Time",
	# "bystanderResponseTimestamp" : "bystanderResponseTime",
	"bystanderAEDTimestamp" : "bystanderResponseTime", #cPRbystander3Time",
	# "reperfusionTimestamp" : "reperfusionTime",
	# "treatmentWithdrawnTimestamp" : "treatmentWithdrawn",
	# "reaTimestamp" : "reaTime",
	# "cPRbystander3Timestamp" : "cPRbystander3Time",
	# "timestampROSC" : "timeROSC",
}


#======================================== USEFUL FUNCTIONS ==================================================================================


def generate_case_id(first_name: str, last_name: str, cardiac_arrest_date: str, ca_timestamp: str): #birth_date: str):
	"""Takes the name, surname and dates in format recieved from input from form: 2020-02-03 (year, month, day) and generates ID"""

	# poskrbi za primer več imen in poenoti velike začetnice
	name = ""
	for i in range(len(first_name)):
		name += first_name[i][0].upper() + first_name[i][1:].lower()

	surname = ""
	for i in range(len(last_name)):
		surname += last_name[i][0].upper() + last_name[i][1:].lower()

	print((cardiac_arrest_date, ca_timestamp))
	# split 
	cardiac_arrest_date = cardiac_arrest_date.split("-")

	
	ca_timestamp = (ca_timestamp.split(" "))[1]
	if "+" in ca_timestamp:
		ca_timestamp = ca_timestamp[:ca_timestamp.find("+")]

	cardiac_arrest_time = ca_timestamp.split(":")

	# birth_date = birth_date.split("-")

	print(cardiac_arrest_time)

	ca_date = cardiac_arrest_date[2] + cardiac_arrest_date[1] + cardiac_arrest_date[0]
	# birth_date = birth_date[2] + birth_date[1] + birth_date[0]
	cardiac_arrest_time = cardiac_arrest_time[0] + cardiac_arrest_time[1] + cardiac_arrest_time[2]
	
	code = name + ca_date + surname + cardiac_arrest_time #birth_date
	print(code)
	hashed = hashlib.sha256(code.encode("utf-8")).hexdigest() #hexdigest
	return hashed

def generate_dispatch_id(intervention_num: str, cardiac_arrest_date: str):
	cardiac_arrest_date = cardiac_arrest_date.split("-")
	ca_date = cardiac_arrest_date[2] + cardiac_arrest_date[1] + cardiac_arrest_date[0]
	
	code = intervention_num + ca_date
	return hashlib.sha256(code.encode("utf-8")).hexdigest()


def create_widgets(values, dates, timestamps): 
	w, w_times = dict(), dict()
	for element in values:
		w[element] = forms.RadioSelect(choices=values[element], attrs={"class" : "with-gap", "type" : "radio"}) #attrs={'class': "form-check-input", "type" : "radio"})
	for element in dates:
		w[element] = DatePickerInput()
	for element in timestamps:
		w[element] = DateTimeSelector()
	return w

# cause of death widget
cods = list(ICD.objects.all())
icd_choices = [(0, "Izberite")]
for elt in cods:
	icd_choices.append((elt.code, str(elt.code) + " - " + str(elt.slovenian)))

w = create_widgets(values, dates, timestamps) 

w["ecgBLOB"] = forms.FileInput(attrs={"class" : "form-control", "type" : "file"})
w["cod"] = forms.Select(choices=icd_choices)


# ========================================== FORMS ================================================================================

from django import forms


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


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		fields = ["i1",'i2','i3','i4','i5','i6','i7','i8','i9','i10','i11','i12',]
		#fields = ["interventionID"]

		for f in fields:
			self.fields[f].label = False

# class TimestampForm(forms.ModelForm):

# 	class Meta:
# 		model = CaseReport
# 		fields = tuple(timestamps)
# 		exclude = ("cPREMS3Timestamp", ) 
# 		widgets= w
# 		labels = titles
# 		help_texts = descriptions
	

	

class DSZ_1_DAN(forms.ModelForm):

	allDrugs = forms.MultipleChoiceField(label=titles["drugs"], widget=forms.CheckboxSelectMultiple,choices=values['drugs'], required=False)
	airway = forms.MultipleChoiceField(label=titles["airwayControl"], widget=forms.CheckboxSelectMultiple,choices=values['airwayControl'], required=False)

	class Meta: 	
		model = CaseReport
		fields = tuple(first_form)	
		exclude = tuple(not_dcz)	
		widgets = w
		labels = titles
		help_texts = descriptions

	# def __init__(self, *args, **kwargs):
	# 	super(DSZ_1_DAN, self).__init__(*args, **kwargs)
		
	# 	for key in self.fields:
	# 		self.fields[key].required = True

class NDSZ_1_DAN(forms.ModelForm):

	allDrugs = forms.MultipleChoiceField(label=titles["drugs"], widget=forms.CheckboxSelectMultiple,choices=values['drugs'], required=False)
	airway = forms.MultipleChoiceField(label=titles["airwayControl"], widget=forms.CheckboxSelectMultiple,choices=values['airwayControl'], required=False)

	class Meta: 	
		model = CaseReport
		fields = tuple(first_form)	
		# exclude = tuple(not_dcz)	
		widgets = w
		labels = titles
		help_texts = descriptions

	# def __init__(self, *args, **kwargs):
	# 	super(NDSZ_1_DAN, self).__init__(*args, **kwargs)
		
	# 	for key in self.fields:
	# 		self.fields[key].required = True

	
class MySecondNewFrom(forms.ModelForm):


	class Meta: 
		model = CaseReport
		fields = tuple(second_form)		
		# exclude = timestamps
		widgets = w
		labels = titles
		help_texts = descriptions

	# def __init__(self, *args, **kwargs):
	# 	super(MySecondNewFrom, self).__init__(*args, **kwargs)
		
	# 	for key in self.fields:
	# 		self.fields[key].required = True
		


