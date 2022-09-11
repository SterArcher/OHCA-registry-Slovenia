from django import forms
from django.core.exceptions import ValidationError
from .models import *
from django.utils.translation import gettext_lazy as _
import hashlib
from .fields import *


#========================================== USEFUL DATA =================================================================================

from .auxiliary import values, titles, descriptions, first_form, second_form, dates, timestamps, not_dcz

# this defines the connections between timestamps and times
# which we need when we are calculating time intervals!
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
	"bystanderAEDTimestamp" : "bystanderResponseTime", #cPRbystander3Time",
}

#======================================== USEFUL FUNCTIONS ==================================================================================


def generate_case_id(first_name, last_name, cardiac_arrest_date: str, ca_timestamp: str): #birth_date: str):
	"""Takes the name, surname and dates in format recieved from input from form: 2020-02-03 (year, month, day) and generates ID"""
	# poskrbi za primer več imen in poenoti velike začetnice
	name = ""
	for i in range(len(first_name)):
		name = name + first_name[i][0].upper() + first_name[i][1:].lower()
	surname = ""
	for i in range(len(last_name)):
		surname += last_name[i][0].upper() + last_name[i][1:].lower()
	cardiac_arrest_date = cardiac_arrest_date.split("-")

	ca_timestamp = (ca_timestamp.split(" "))[1]
	if "+" in ca_timestamp:
		ca_timestamp = ca_timestamp[:ca_timestamp.find("+")]

	cardiac_arrest_time = ca_timestamp.split(":")

	ca_date = cardiac_arrest_date[2] + cardiac_arrest_date[1] + cardiac_arrest_date[0]

	cardiac_arrest_time = cardiac_arrest_time[0] + cardiac_arrest_time[1] + cardiac_arrest_time[2]
	
	code = name + ca_date + surname + cardiac_arrest_time #birth_date
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

timestamps += ["treatmentWithdrawnTimestamp"]
w = create_widgets(values, dates, timestamps) 

w["ecgBLOB"] = forms.FileInput(attrs={"class" : "form-control", "type" : "file"})
w["cod"] = forms.Select(choices=icd_choices)

# w["ttmTemp"] = valueInput
w["drugs"] = forms.CheckboxSelectMultiple(choices=values['drugs'])
w["airwayControl"] = forms.CheckboxSelectMultiple(choices=values['airwayControl'])
w["ecgOptions"] = forms.CheckboxSelectMultiple(choices=values['ecgOptions'])

w["neuroprognosticTests"] = forms.Textarea(attrs={'rows':1})

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

class InterventionForm2(forms.Form):
	"""Form for 12 separate fields for the intervention number 
	- this one is used on the 30 days after form where the fields are not required."""

	i1 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}), required=False)
	i2 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}), required=False)
	i3 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}), required=False)
	i4 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}), required=False)
	i5 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}), required=False)
	i6 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}), required=False)
	i7 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}), required=False)
	i8 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}), required=False)
	i9 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}), required=False)
	i10 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}), required=False)
	i11 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}), required=False)
	i12 = forms.IntegerField(min_value=0, max_value=9, widget=forms.NumberInput(attrs={'style': 'width: 50px'}), required=False)


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		fields = ["i1",'i2','i3','i4','i5','i6','i7','i8','i9','i10','i11','i12',]
		#fields = ["interventionID"]

		for f in fields:
			self.fields[f].label = False
	

class DSZ_1_DAN(forms.ModelForm):

	ecgopt = forms.MultipleChoiceField(label=titles["ecgOptions"], widget=forms.CheckboxSelectMultiple,choices=values['ecgOptions'], required=False)

	# create separate fields for radion options below string fields ("ni podatka", "ni zabeleženo")
	adShocks = forms.IntegerField(widget=forms.RadioSelect(choices=((-1, "Neznano/ni podatka"), (-2, "Ni zabeleženo/ni zavedeno"))), required=False)
	adHospitalName = forms.IntegerField(widget=forms.RadioSelect(choices=((-1, "Neznano/ni podatka"), (-2, "Ni zabeleženo/ni zavedeno"))), required=False)
	adBystAge = forms.IntegerField(widget=forms.RadioSelect(choices=((-1, "Neznano/ni podatka"), (-2, "Ni zabeleženo/ni zavedeno"))), required=False)

	class Meta: 	
		model = CaseReport
		fields = tuple(first_form)	
		exclude = tuple(not_dcz) 
		widgets = w
		labels = titles
		help_texts = descriptions

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# delete labels for auxiliary fields
		fields = ["adShocks", "adHospitalName", "adBystAge"]
		for f in fields:
			self.fields[f].label = False

		# define fields that are NOT required
		extras = [
			# "drugs", "airwayControl", 
			"ecgOptions", # mutliple select fields
			# "targetBP", "drugs", "ttmTemp", "ph", "lactate", # string fields with radio 
			# "adPh", "adLactate", "adTtmTemp", "adShocks", "adTargetBP",
			"dateOfBirth", "estimatedAge", "ageBystander", "adBystAge", 
			"shocks", "ecgResult", "hospitalName", "adHospitalName", "noCPR"
			]

		estimatedTimestamps = ["estimatedCallTimestamp", "estimatedResponseTime", "estimatedDefibTimestamp", "estimatedDrugTimings", "estimatedRoscTimestamp", "estimatedCPREMStimestamp", "estimatedTimestampTCPR", "estimatedCPRbystander", "estimatedCPRhelperTimestamp", "estimatedEndCPRtimestamp", "estimatedLeftSceneTimestamp", "estimatedHospitalArrival"]

		for key in self.fields:
			if key not in (timestamps + extras + estimatedTimestamps):
				self.fields[key].required = True

		# time of the event is the only always required timestamp on this form
		self.fields["reaTimestamp"].required = True


	def clean(self):# -> Optional[Dict[str, Any]]:
		cleaned_data = super().clean()
		print(cleaned_data)

		errors = dict()

		for key in cleaned_data:
			# when they choose "ni zabeleženo" it is saved as -9999 and needs to be converted into something that can be saved to db
			if cleaned_data[key] == -9999:
				cleaned_data[key] = None

		# handling multipleselect fields
		# values are saved as a list of string values that we want to sum
		# we are not worried about them choosing "ni podatka" and other drugs at the same time bc we handled this in formValidation.js
		# drugs = cleaned_data["allDrugs"]
		# drugs = list(map(lambda x: int(x), drugs))
		# cleaned_data["drugs"] = sum(drugs) if -9999 not in drugs else None

		# airway = cleaned_data["airway"]
		# airway = list(map(lambda x: int(x), airway))
		# cleaned_data["airwayControl"] = sum(airway) if -9999 not in airway else None

		# this one has many values so we save them as a list of numbers
		ecg = cleaned_data["ecgopt"]
		ecg_val = ""
		for elt in ecg:
			ecg_val = (ecg_val + ", " + str(elt)) if ecg_val != "" else str(elt)
		cleaned_data["ecgOptions"] = ecg_val

		return cleaned_data



class NDSZ_1_DAN(forms.ModelForm):

	# allDrugs = forms.MultipleChoiceField(label=titles["drugs"], widget=forms.CheckboxSelectMultiple,choices=values['drugs'], required=False)
	# airway = forms.MultipleChoiceField(label=titles["airwayControl"], widget=forms.CheckboxSelectMultiple,choices=values['airwayControl'], required=False)
	ecgopt = forms.MultipleChoiceField(label=titles["ecgOptions"], widget=forms.CheckboxSelectMultiple,choices=values['ecgOptions'], required=False)

	adShocks = forms.IntegerField(widget=forms.RadioSelect(choices=((-1, "Neznano/Ni podatka"), (-2, "Ni zabeleženo/ni zavedeno"))), required=False)
	adHospitalName = forms.IntegerField(widget=forms.RadioSelect(choices=((-1, "Neznano/ni podatka"), (-2, "Ni zabeleženo/ni zavedeno"))), required=False)
	adBystAge = forms.IntegerField(widget=forms.RadioSelect(choices=((-1, "Neznano/ni podatka"), (-2, "Ni zabeleženo/ni zavedeno"))), required=False)


	class Meta: 	
		model = CaseReport
		fields = tuple(first_form)		
		widgets = w
		labels = titles
		help_texts = descriptions

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

		# delete labels for auxiliary fields
		fields = ["adShocks", "adHospitalName", "adBystAge"]
		for f in fields:
			self.fields[f].label = False

		# define fields that are NOT required
		extras = [
			# "drugs", "airwayControl", 
			"ecgOptions", # mutliple select fields
			# "targetBP", "drugs", "ttmTemp", "ph", "lactate", # string fields with radio 
			# "adPh", "adLactate", "adTtmTemp", "adShocks", "adTargetBP",
			"dateOfBirth", "estimatedAge", "ageBystander", "adBystAge", 
			"shocks", "ecgResult", "hospitalName", "adHospitalName", "noCPR"
			]

		estimatedTimestamps = ["estimatedDefibTimestamp", "estimatedDrugTimings", "estimatedRoscTimestamp", "estimatedCPREMStimestamp", "estimatedTimestampTCPR", "estimatedCPRbystander", "estimatedCPRhelperTimestamp", "estimatedEndCPRtimestamp", "estimatedHospitalArrival"]

		for key in self.fields:
			if key not in (timestamps + extras + estimatedTimestamps):
				self.fields[key].required = True
		
		# more timestamps are required on this form
		self.fields["reaTimestamp"].required = True
		self.fields["callTimestamp"].required = True
		self.fields["responseTimestamp"].required = True
		self.fields["leftScene5Timestamp"].required = True

		

	def clean(self):# -> Optional[Dict[str, Any]]:
		cleaned_data = super().clean()
		print(cleaned_data)

		errors = dict()

		for key in cleaned_data:
			if cleaned_data[key] == -9999:
				cleaned_data[key] = None


		ecg = cleaned_data["ecgopt"]
		ecg_val = ""
		for elt in ecg:
			ecg_val += elt
		cleaned_data["ecgOptions"] = ecg_val

		# this isnt supposed to happen bc of formValidation.js
		if cleaned_data["dateOfBirth"] == None and cleaned_data["estimatedAge"] == None:
			errors["dateOfBirth"] = "Vpišite ali datum rojstva ali ocenjeno starost!"
			errors["estimatedAge"] = "Vpišite ali datum rojstva ali ocenjeno starost!"

		
		if len(list(errors.keys())) >= 1:
			raise ValidationError(errors)

		return cleaned_data


	
class MySecondNewFrom(forms.ModelForm):

	# create new fields for multiple select questions
	allDrugs = forms.MultipleChoiceField(label=titles["drugs"], widget=forms.CheckboxSelectMultiple,choices=values['drugs'], required=False)
	airway = forms.MultipleChoiceField(label=titles["airwayControl"], widget=forms.CheckboxSelectMultiple,choices=values['airwayControl'], required=False)
	

	adWithdraw = forms.IntegerField(widget=forms.RadioSelect(choices=((-9999, "Neznano/Ni podatka"), (-9999, "Ni zabeleženo/ni zavedeno"))), required=False)

	adTtmTemp = forms.IntegerField(widget=forms.RadioSelect(choices=((-1, "Neznano/Ni podatka"), (-2, "Ni zabeleženo/ni zavedeno"))), required=False)
	adTargetBP = forms.IntegerField(widget=forms.RadioSelect(choices=((0, "Ni opredeljenega cilja"), (-1, "Neznano/Ni podatka"), (-2, "Ni zabeleženo/ni zavedeno"))), required=False)
	adPh = forms.IntegerField(widget=forms.RadioSelect(choices=((-1, "Neznano/Ni podatka"), (-2, "Ni zabeleženo/ni zavedeno"))), required=False)
	adLactate = forms.IntegerField(widget=forms.RadioSelect(choices=((-1, "Neznano/Ni podatka"), (-2, "Ni zabeleženo/ni zavedeno"))), required=False)
	

	class Meta: 
		model = CaseReport
		fields = tuple(second_form)		
		widgets = w
		labels = titles
		help_texts = descriptions

	def __init__(self, *args, **kwargs):
		super(MySecondNewFrom, self).__init__(*args, **kwargs)

		all_fields = list(self.fields)
		# time of CA is not required bc if they're part of DCZ they don't have it
		# they have to either fill the intevrention number or this timestamp which is handled with formValidation.js
		required = list(filter(lambda x: x != "reaTimestamp", all_fields))
		not_required = ["neuroprognosticTests", "discDate", "cod", "treatmentWithdrawnTimestamp", "adWithdraw"]
		for key in required:
			if key not in not_required:
				self.fields[key].required = True

		self.fields["neuroprognosticTests"].label = False
		self.fields["adWithdraw"].label = False

		# delete labels for auxiliary fields
		fields = ["adTtmTemp", "adPh", "adTargetBP", "adLactate"]
		for f in fields:
			self.fields[f].label = False

		# define fields that are NOT required
		extras = [
			"drugs", "airwayControl", #"ecgOptions", # mutliple select fields
			"targetBP", "drugs", "ttmTemp", "ph", "lactate", # string fields with radio 
			"adPh", "adLactate", "adTtmTemp", "adTargetBP",
			"dateOfBirth", #"estimatedAge", "ageBystander", "adBystAge", 
			# "shocks", "ecgResult", "hospitalName", "adHospitalName", "noCPR"
			]

		estimatedTimestamps = ["estimatedDefibTimestamp", "estimatedDrugTimings", "estimatedRoscTimestamp", "estimatedCPREMStimestamp", "estimatedTimestampTCPR", "estimatedCPRbystander", "estimatedCPRhelperTimestamp", "estimatedEndCPRtimestamp", "estimatedHospitalArrival"]

		for key in self.fields:
			if key not in (timestamps + extras + estimatedTimestamps):
				self.fields[key].required = True

		for key in ["reaTimestamp", "estimatedCAtimestamp", "dateOfBirth", "estimatedAge", "drugTimingsTimestamp", "estimatedDrugTimings"]:
			self.fields[key].required = False

		for key in extras:
			self.fields[key].required = False

		self.fields["neuroprognosticTests"].required = False

		
	def clean(self):# -> Optional[Dict[str, Any]]:
		cleaned_data = super().clean()
		print(cleaned_data)
		errors = dict()

		for key in cleaned_data:
			if cleaned_data[key] == -9999:
				cleaned_data[key] = None

		drugs = cleaned_data["allDrugs"]
		drugs = list(map(lambda x: int(x), drugs))
		cleaned_data["drugs"] = sum(drugs)

		airway = cleaned_data["airway"]
		airway = list(map(lambda x: int(x), airway))
		cleaned_data["airwayControl"] = sum(airway)

		if cleaned_data["dateOfBirth"] == None and cleaned_data["estimatedAge"] == None:
			errors["dateOfBirth"] = "Vpišite ali datum rojstva ali ocenjeno starost!"
			errors["estimatedAge"] = "Vpišite ali datum rojstva ali ocenjeno starost!"

		if len(list(errors.keys())) >= 1:
			raise ValidationError(errors)

		return cleaned_data

