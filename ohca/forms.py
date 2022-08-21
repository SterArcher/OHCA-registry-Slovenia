from django import forms
from django.core.exceptions import ValidationError
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
	name = "",
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

timestamps += ["treatmentWithdrawnTimestamp"]
w = create_widgets(values, dates, timestamps) 

w["ecgBLOB"] = forms.FileInput(attrs={"class" : "form-control", "type" : "file"})
w["cod"] = forms.Select(choices=icd_choices)

# w["ttmTemp"] = valueInput
w["drugs"] = forms.CheckboxSelectMultiple(choices=values['drugs'])
w["airwayControl"] = forms.CheckboxSelectMultiple(choices=values['airwayControl'])

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
	"""Form for 12 separate fields for the intervention number"""

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

	allDrugs = forms.MultipleChoiceField(label=titles["drugs"], widget=forms.CheckboxSelectMultiple,choices=values['drugs'], required=False)
	airway = forms.MultipleChoiceField(label=titles["airwayControl"], widget=forms.CheckboxSelectMultiple,choices=values['airwayControl'], required=False)

	adTtmTemp = forms.IntegerField(widget=forms.RadioSelect(choices=((-1, "Neznano/ni podatka"), (-9999, "Ni zabeleženo/ni zavedeno"))), required=False)
	adTargetBP = forms.IntegerField(widget=forms.RadioSelect(choices=((0, "Ni opredeljenega cilja"), (-1, "Neznano/ni podatka"), (-9999, "Ni zabeleženo/ni zavedeno"))), required=False)
	adPh = forms.IntegerField(widget=forms.RadioSelect(choices=((-1, "Neznano/ni podatka"), (-9999, "Ni zabeleženo/ni zavedeno"))), required=False)
	adLactate = forms.IntegerField(widget=forms.RadioSelect(choices=((-1, "Neznano/ni podatka"), (-9999, "Ni zabeleženo/ni zavedeno"))), required=False)
	adShocks = forms.IntegerField(widget=forms.RadioSelect(choices=((-1, "Neznano/ni podatka"), (-9999, "Ni zabeleženo/ni zavedeno"))), required=False)

	class Meta: 	
		model = CaseReport
		fields = tuple(first_form)	
		exclude = tuple(not_dcz) + ("estimatedCAtimestamp",)
		widgets = w
		labels = titles
		help_texts = descriptions

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		fields = ["adTtmTemp", "adPh", "adTargetBP", "adLactate", "adShocks"]

		for f in fields:
			self.fields[f].label = False

		extras = ["ph", "adPh", "lactate", "adLactate", "targetBP", "adTargetBP", "shocks", "adShocks", "ttmTemp", "adTtmTemp"]


		for key in self.fields:
			if key not in (timestamps + extras + ["dateOfBirth", "estimatedAge"]):
				self.fields[key].required = True


	def clean(self):# -> Optional[Dict[str, Any]]:
		cleaned_data = super().clean()
		print(cleaned_data)

		errors = dict()

		ph = cleaned_data["ph"]
		adPh = cleaned_data["adPh"]
		if ph == None and adPh == None:
			errors["ph"] = "Izpolnite podatke o ph tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"
			errors["adPh"] = "Izpolnite podatke o ph tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"

		lactate = cleaned_data["lactate"]
		adlactate = cleaned_data["adLactate"]
		if lactate == None and adlactate == None:
			errors["lactate"] = "Izpolnite podatke o laktatu tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"
			errors["adLactate"] = "Izpolnite podatke o laktatu tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"

		Shocks = cleaned_data["shocks"]
		adShocks = cleaned_data["adShocks"]
		if Shocks == None and adShocks == None:
			errors["shocks"] = "Izpolnite podatke o številu defibrilacij tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"
			errors["adShocks"] = "Izpolnite podatke o številu defibrilacij tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"

		TargetBP = cleaned_data["targetBP"]
		adTargetBP = cleaned_data["adTargetBP"]
		if TargetBP == None and adTargetBP == None:
			errors["targetBP"] = "Izpolnite podatke o ciljanem upravljanju krvnega pritiska tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"
			errors["adTargetBP"] = "Izpolnite podatke o ciljanem upravljanju krvnega pritiska tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"

		TtmTemp = cleaned_data["ttmTemp"]
		adTtmTemp = cleaned_data["adTtmTemp"]
		if TtmTemp == None and adTtmTemp == None:
			errors["ttmTemp"] = "Izpolnite podatke o ciljanem upravljanju krvnega pritiska tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"
			errors["adTtmTemp"] = "Izpolnite podatke o ciljanem upravljanju krvnega pritiska tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"


		for key in cleaned_data:
			if cleaned_data[key] == -9999:
				cleaned_data[key] = None

		

		drugs = cleaned_data["allDrugs"]
		const = "1" in drugs or "2" in drugs or "4" in drugs
		if "0" in drugs and const:
			errors["allDrugs"] = "Pri vprašanju o aplikaciji zdravil ste označili možnost 'brez', 'neznano' ali 'ni zabeleženo' in hkrati enega od zdravil!"
		elif "-1" in drugs and const:
			errors["allDrugs"] = "Pri vprašanju o aplikaciji zdravil ste označili možnost 'brez', 'neznano' ali 'ni zabeleženo' in hkrati enega od zdravil!"
		elif "-9999" in drugs and const:
			errors["allDrugs"] = "Pri vprašanju o aplikaciji zdravil ste označili možnost 'brez', 'neznano' ali 'ni zabeleženo' in hkrati enega od zdravil!"
		else:
			drugs = list(map(lambda x: int(x), drugs))
			cleaned_data["drugs"] = sum(drugs)

		airway = cleaned_data["airway"]
		const = "1" in airway or "2" in airway or "4" in airway or "8" in airway
		if "0" in airway and const:
			errors["airway"] = "Pri vprašanju o aplikaciji zdravil ste označili možnost 'brez', 'neznano' ali 'ni zabeleženo' in hkrati enega od zdravil!"
		elif "-1" in airway and const:
			errors["airway"] = "Pri vprašanju o aplikaciji zdravil ste označili možnost 'brez', 'neznano' ali 'ni zabeleženo' in hkrati enega od zdravil!"
		elif "-9999" in airway and const:
			errors["airway"] = "Pri vprašanju o aplikaciji zdravil ste označili možnost 'brez', 'neznano' ali 'ni zabeleženo' in hkrati enega od zdravil!"
		else:
			airway = list(map(lambda x: int(x), airway))
			cleaned_data["airwayControl"] = sum(airway)
		# ne smejo bit prazna oboje ph in neznano

		if cleaned_data["dateOfBirth"] == None and cleaned_data["estimatedAge"] == None:
			errors["dateOfBirth"] = "Vpišite ali datum rojstva ali ocenjeno starost!"
			errors["estimatedAge"] = "Vpišite ali datum rojstva ali ocenjeno starost!"

		
		if len(list(errors.keys())) >= 1:
			raise ValidationError(errors)

		return cleaned_data



class NDSZ_1_DAN(forms.ModelForm):

	allDrugs = forms.MultipleChoiceField(label=titles["drugs"], widget=forms.CheckboxSelectMultiple,choices=values['drugs'], required=False)
	airway = forms.MultipleChoiceField(label=titles["airwayControl"], widget=forms.CheckboxSelectMultiple,choices=values['airwayControl'], required=False)

	adTtmTemp = forms.IntegerField(widget=forms.RadioSelect(choices=((-1, "Neznano/Ni podatka"), (-9999, "Ni zabeleženo/ni zavedeno"))), required=False)
	adTargetBP = forms.IntegerField(widget=forms.RadioSelect(choices=((0, "Ni opredeljenega cilja"), (-1, "Neznano/Ni podatka"), (-9999, "Ni zabeleženo/ni zavedeno"))), required=False)
	adPh = forms.IntegerField(widget=forms.RadioSelect(choices=((-1, "Neznano/Ni podatka"), (-9999, "Ni zabeleženo/ni zavedeno"))), required=False)
	adLactate = forms.IntegerField(widget=forms.RadioSelect(choices=((-1, "Neznano/Ni podatka"), (-9999, "Ni zabeleženo/ni zavedeno"))), required=False)
	adShocks = forms.IntegerField(widget=forms.RadioSelect(choices=((-1, "Neznano/Ni podatka"), (-9999, "Ni zabeleženo/ni zavedeno"))), required=False)

	class Meta: 	
		model = CaseReport
		fields = tuple(first_form)	
		# exclude = tuple(not_dcz)	
		widgets = w
		labels = titles
		help_texts = descriptions

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		fields = ["adTtmTemp", "adPh", "adTargetBP", "adLactate", "adShocks"]

		for f in fields:
			self.fields[f].label = False

		extras = ["ph", "adPh", "lactate", "adLactate", "targetBP", "adTargetBP", "shocks", "adShocks", "ttmTemp", "adTtmTemp"]

		for key in self.fields:
			if key not in ((list(filter(lambda x: x != "reaTimestamp", timestamps))) + ["dateOfBirth", "estimatedAge"] + extras):
				self.fields[key].required = True


	def clean(self):# -> Optional[Dict[str, Any]]:
		cleaned_data = super().clean()
		print(cleaned_data)

		errors = dict()

		ph = cleaned_data["ph"]
		adPh = cleaned_data["adPh"]
		if ph == None and adPh == None:
			errors["ph"] = "Izpolnite podatke o ph tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"
			errors["adPh"] = "Izpolnite podatke o ph tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"

		lactate = cleaned_data["lactate"]
		adlactate = cleaned_data["adLactate"]
		if lactate == None and adlactate == None:
			errors["lactate"] = "Izpolnite podatke o laktatu tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"
			errors["adLactate"] = "Izpolnite podatke o laktatu tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"

		Shocks = cleaned_data["shocks"]
		adShocks = cleaned_data["adShocks"]
		if Shocks == None and adShocks == None:
			errors["shocks"] = "Izpolnite podatke o številu defibrilacij tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"
			errors["adShocks"] = "Izpolnite podatke o številu defibrilacij tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"

		TargetBP = cleaned_data["targetBP"]
		adTargetBP = cleaned_data["adTargetBP"]
		if TargetBP == None and adTargetBP == None:
			errors["targetBP"] = "Izpolnite podatke o ciljanem upravljanju krvnega pritiska tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"
			errors["adTargetBP"] = "Izpolnite podatke o ciljanem upravljanju krvnega pritiska tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"

		TtmTemp = cleaned_data["ttmTemp"]
		adTtmTemp = cleaned_data["adTtmTemp"]
		if TtmTemp == None and adTtmTemp == None:
			errors["ttmTemp"] = "Izpolnite podatke o ciljanem upravljanju krvnega pritiska tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"
			errors["adTtmTemp"] = "Izpolnite podatke o ciljanem upravljanju krvnega pritiska tako da vpišete vrednost ali označite 'neznano' ali 'ni zabeleženo'!"


		for key in cleaned_data:
			if cleaned_data[key] == -9999:
				cleaned_data[key] = None

		

		drugs = cleaned_data["allDrugs"]
		const = "1" in drugs or "2" in drugs or "4" in drugs
		if "0" in drugs and const:
			errors["allDrugs"] = "Pri vprašanju o aplikaciji zdravil ste označili možnost 'brez', 'neznano' ali 'ni zabeleženo' in hkrati enega od zdravil!"
		elif "-1" in drugs and const:
			errors["allDrugs"] = "Pri vprašanju o aplikaciji zdravil ste označili možnost 'brez', 'neznano' ali 'ni zabeleženo' in hkrati enega od zdravil!"
		elif "-9999" in drugs and const:
			errors["allDrugs"] = "Pri vprašanju o aplikaciji zdravil ste označili možnost 'brez', 'neznano' ali 'ni zabeleženo' in hkrati enega od zdravil!"
		else:
			drugs = list(map(lambda x: int(x), drugs))
			cleaned_data["drugs"] = sum(drugs)

		airway = cleaned_data["airway"]
		const = "1" in airway or "2" in airway or "4" in airway or "8" in airway
		if "0" in airway and const:
			errors["airway"] = "Pri vprašanju o aplikaciji zdravil ste označili možnost 'brez', 'neznano' ali 'ni zabeleženo' in hkrati enega od zdravil!"
		elif "-1" in airway and const:
			errors["airway"] = "Pri vprašanju o aplikaciji zdravil ste označili možnost 'brez', 'neznano' ali 'ni zabeleženo' in hkrati enega od zdravil!"
		elif "-9999" in airway and const:
			errors["airway"] = "Pri vprašanju o aplikaciji zdravil ste označili možnost 'brez', 'neznano' ali 'ni zabeleženo' in hkrati enega od zdravil!"
		else:
			airway = list(map(lambda x: int(x), airway))
			cleaned_data["airwayControl"] = sum(airway)
		# ne smejo bit prazna oboje ph in neznano

		if cleaned_data["dateOfBirth"] == None and cleaned_data["estimatedAge"] == None:
			errors["dateOfBirth"] = "Vpišite ali datum rojstva ali ocenjeno starost!"
			errors["estimatedAge"] = "Vpišite ali datum rojstva ali ocenjeno starost!"

		
		if len(list(errors.keys())) >= 1:
			raise ValidationError(errors)

		return cleaned_data


	
class MySecondNewFrom(forms.ModelForm):


	class Meta: 
		model = CaseReport
		fields = tuple(second_form)		
		exclude = ("doctorName",)
		widgets = w
		labels = titles
		help_texts = descriptions

	def __init__(self, *args, **kwargs):
		super(MySecondNewFrom, self).__init__(*args, **kwargs)
		
		

		all_fields = list(self.fields)
		for key in list(filter(lambda x: x != "reaTimestamp", all_fields)):
			self.fields[key].required = True

		for key in ["reaTimestamp", "estimatedCAtimestamp", "dateOfBirth", "estimatedAge"]:
			self.fields[key].required = False
		
	def clean(self):# -> Optional[Dict[str, Any]]:
		cleaned_data = super().clean()
		# print(cleaned_data)
		errors = dict()

		for key in cleaned_data:
			if cleaned_data[key] == -9999:
				cleaned_data[key] = None

		# if cleaned_data["interventionID"] == None and cleaned_data["reaTimestamp"] == None:
		# 	errors["reaTimestamp"] = "Vpišite ali intervencijko številko ali pa podatke o datumu, imenu, priimku in času srčnega zastoja, da lahko sistem identificira pacienta!"
		# # if cleaned_data["interventionID"] == None and cleaned_data["name"] == None:
		# 	errors["reaTimestamp"] = "Vpišite ali intervencijko številko ali pa podatke o datumu, imenu, priimku in času srčnega zastoja, da lahko sistem identificira pacienta!"
		# if cleaned_data["interventionID"] == None and cleaned_data["surname"] == None:
		# 	errors["reaTimestamp"] = "Vpišite ali intervencijko številko ali pa podatke o datumu, imenu, priimku in času srčnega zastoja, da lahko sistem identificira pacienta!"
		# if cleaned_data["interventionID"] == None and cleaned_data["reaTimestamp"] == None:
		# 	errors["reaTimestamp"] = "Vpišite ali intervencijko številko ali pa podatke o datumu, imenu, priimku in času srčnega zastoja, da lahko sistem identificira pacienta!"

		if cleaned_data["dateOfBirth"] == None and cleaned_data["estimatedAge"] == None:
			errors["dateOfBirth"] = "Vpišite ali datum rojstva ali ocenjeno starost!"
			errors["estimatedAge"] = "Vpišite ali datum rojstva ali ocenjeno starost!"

		if len(list(errors.keys())) >= 1:
			raise ValidationError(errors)

		# if cleaned_data["name"] == None and cleaned_data["surname"] == None:
		# 	raise ValidationError({"name" : "poskus", "surname" : "tudi poskus"})

		return cleaned_data

