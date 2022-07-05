from django import forms
from django.core import validators
# from matplotlib import widgets
from .models import *
from django.utils.translation import gettext_lazy as _
import hashlib
# from django.forms import HiddenInput, IntegerField, MultiWidget, NumberInput, TextInput
from .widget import *


#========================================== USEFUL DATA =================================================================================

# TODO import functions instead of whole dictionaries

# tole je trenutno narejeno zelo nepraktično, moram spravit vse pomožne datoteke v en file :)

values = {'dispIdentifiedCA': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'dispProvidedCPRinst': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'gender': [(-1, 'Neznano'), (0, 'Moški'), (1, 'Ženska')], 'witnesses': [(-1, 'Neznano/ni zabeleženo - ni zavedeno'), (0, 'NE, brez prič'), (1, 'DA, v prisotnosti očividca'), (2, 'DA, v prisotnosti ekipe NMP'), (3, 'Oseba, ki je bila poslana na kraj srčnega zastoja, da nudi pomoč/oživljanje')], 'location': [(-1, 'Neznano'), (1, 'Dom/prebivališče (stalno ali začasno)'), (2, 'Industrija/delovno mesto/pisarna'), (3, 'Športni/rekreacijski dogodek oz. infrasturktura (dvorana, telovadnica, stadion,..)'), (4, 'Ulica/avtocesta'), (5, 'Javna ustanova/zgradba'), (6, 'Varovano stanovanje/dom za ostarele (ustanove za dolgotrajno oskrbo)'), (7, 'Učna ustanova'), (8, 'Drugo')], 'bystanderResponse': [(-1, 'Neznano'), (0, 'Očividec ni izvajal TPO'), (1, 'Očividec izvajal TPO (podrobneje: samo stisi prsnega koša, stisi prsnega koša in umetno predihavanje)'), (2, 'Očividec izvajal TPO (podrobneje: samo stisi prsnega koša, stisi prsnega koša in umetno predihavanje)')], 'bystanderAED': [(-1, 'Neznano'), (0, 'AED ni uporabljen'), (1, 'AED uporabljen, defibrilacija ni izvedena'), (2, 'AED uporabljen, defibrilacija izvedena')], 'deadOnArrival': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'firstMonitoredRhy': [(-1, 'Neznano'), (1, 'VF'), (2, 'VT brez utripa'), (3, 'PEA'), (4, 'Asistolija'), (5, 'Bradikardija'), (6, 'AED - defibrilacija ni potrebna'), (7, 'AED - defibrilacija je potrebna')], 'pathogenesis': [(1, 'Zdravstvena težava'), (2, 'Travma'), (3, 'Predoziranje z drogami'), (4, 'Utopitev'), (5, 'Elektrošok'), (6, 'Zadušitev')], 'independentLiving': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'comorbidities': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'vad': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'cardioverterDefib': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Interni'), (2, 'Eksterni')], 'stemiPresent': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'ttm': [(-1, 'Neznano'), (1, 'Med zastojem'), (2, 'Po-ROSC predbolnišnično'), (3, 'Po-ROSC bolnišnično'), (4, 'Terapevtska hipotermija indicirana, neizvedena'), (5, 'Terapevtska hipotermija ni indicirana')], 'drugs': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Adrenaline'), (2, 'Amiodarone'), (4, 'Vasopressin')], 'airwayControl': [(-1, 'Neznano'), (0, 'Brez used'), (1, 'Orofaringealna dihalna pot'), (2, 'Supraglotična dihalna pot'), (4, 'Endotrahealni tubus'), (8, 'Kirurška dihalna pot')], 'cprQuality': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'vascularAccess': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Centralna venska'), (2, 'Periferna IV'), (3, 'IO'), (4, 'Endotrahealna')], 'mechanicalCPR': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Naprava za mehanske kompresije prnega koša (Lucas)'), (2, 'Trak za razporeditev sile'), (3, 'Druga mehanska naprava')], 'targetVent': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Samo O2'), (2, 'Samo CO2'), (3, 'O2 & CO2')], 'reperfusionAttempt': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Samo angiografija'), (2, 'PCI'), (4, 'Tromboliza')], 'reperfusionTime': [(-1, 'Neznano'), (1, 'Med zastojem'), (2, 'Znotraj 24 h od ROSC'), (3, 'Po 24 h, a pred odpustom')], 'ecls': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Pred ROSC'), (2, 'Po ROSC')], 'iabp': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'glucose': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'specialistHospital': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'ecg': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'survived': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'rosc': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'SurvivalDischarge30d': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'survivalStatus': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'transportToHospital': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'organDonation': [(-1, 'Neznano'), (0, 'Ni donor'), (1, 'Donor')], 'reaConf': [(-1, 'Neznano'), (0, 'Da'), (1, 'Ne')], 'cprEms': [(-1, 'Neznano'), (0, 'Da'), (1, 'Ne')], 'noCPR': [(-1, 'Neznano'), (0, 'Umrl prej/pred prihodom NMP'), (1, 'DNAR/želja bolnika, da ge ne oživljajo'), (2, 'Želja družinskih članov, da bolnika ne oživljajo'), (3, 'Želja/odločitev zdravnika'), (4, 'Uspešna defibrilacija ICD (implantiran kardioverter/defibrlator)'), (5, 'Znaki življenja ob prihodu NMP')], 'reaCause': [(-1, 'Neznano (najverjetneje srčni)'), (0, 'Srčni'), (1, 'Poškodba'), (2, 'Utopitev'), (3, 'Respiratorni'), (4, 'Ostali - ne-srčni')], 'gbystnader': [(-1, 'Neznano'), (0, 'Moški'), (1, 
'Ženska')],'estimatedAgeBystander': [(-1, 'Neznano'), (0, 'Da'), (1, 'Ne')], 'helperCPR': [(-1, 'Neznano'), (0, 'Da'), (1, 'Ne')], 'helperWho': [(1, 'Osebo, ki jo je na kraj zastoja poslal dispečer (to je katerakoli oseba, za katero ne vemo ali ima opravljen BLS tečaj ali izpolnjuje katerega izmed spodnjih pogojev)'), (2, 'Osebo, ki ima opravljen BLS tečaj, in jo je na kraj zastoja poslal dispečer'), (3, 
'Gasilec (prvi posredovalec), ki ga je na kraj zastoja poslal dispečer'), (4, 'Zdravstveni delavec, ki trenutno ni v službi, in ga je na kraj zastoja poslal dispečer'), (5, 'Ostali, ki jih je na kraj zastoja poslal dispečer (ostale skupine, ki niso navedene zgoraj)')], 'defiOrig': [(-1, 'Neznano'), (0, 'AED'), (1, 'NMP (tudi, če je NMP uporabil AED - npr. MoENRV ali motorist)')], 'hospArri': [(-1, 'Neznano'), (0, 'Mrtev'), (1, 'Živ'), (2, 'Brez prevoza do bolnišnice'), (3, 'Prevoz z CPR'), (4, 'Prevoz z ROSC')]}

titles = {'caseID': 'UUID primera', 'systemID': 'Regija srčnega zastoja', 'localID': 'Občina', 'dispIdentifiedCA': 'Dispečer je prepoznal prisotnost zastoja srca', 'dispProvidedCPRinst': 
'Ali je dispečer/NMP dal navodila po telefonu za oživljanje', 'age': 'Starost', 'gender': 'Spol', 'witnesses': 'Ali se je srčni zastoj zgodil vpričo očividcev', 'location': 'Lokacija zastoja - Utstein 2015', 'bystanderResponse': 'Odziv očividca', 'bystanderResponseTime': 'Začetek izvajanja TPO očividcev', 'bystanderAED': 'Uporaba AED s strani očividca', 'bystanderAEDTime': 'Čas prvega AED šoka očividcev', 'deadOnArrival': 'Mrtvogled', 'firstMonitoredRhy': 'Začetni (prvi) ritem - Utstein 2015', 'pathogenesis': 'Patogeneza', 'independentLiving': 'Samostojno življenje', 'comorbidities': 'Pridružene bolezni', 'vad': 'VAD', 'cardioverterDefib': 'Kardioverter-defibrilator', 'stemiPresent': 'Prisoten STEMI', 'responseTime': 'Odzivni čas', 'defibTime': 'Čas do defibrilacije', 'ttm': 'Terapevtska hipotermija', 'ttmTemp': 'TTM Temperatura', 'drugs': 'Aplicirana zdravila', 'airwayControl': 'Tip nadzora dihalne poti', 'cprQuality': 'Kvaliteta TPO', 'shocks': 'Število elektrošokov', 'drugTimings': 'Čas do aplikacije zdravil', 'vascularAccess': 'Vaskularna pot', 'mechanicalCPR': 'Mehanski stiski prnega koša', 'targetVent': 'Ciljana okisgenacija/ventilacija', 'reperfusionAttempt': 'Poskus reperfuzije', 'reperfusionTime': 'Čas do poskusa reperfuzije', 'ecls': 'ECLS', 'iabp': 'IABP', 'ph': 'pH krvi', 'lactate': 'Laktat', 'glucose': 'Je bila po ROSC glukoza titrirana do določene vrednosti?', 'neuroprognosticTests': 'Število in vrsta nevroprognostičnih testov', 'specialistHospital': 'Ali je bolnišnica specialistični center', 'hospitalVolume': 'Obremenitev bolnišnice', 'ecg': 'EKG z 12 odvodi', 'ecgBLOB': 'EKG datoteka', 'targetBP': 'Ciljano upravljanje krvnega pritiska', 'survived': 'Preživetje', 'rosc': 'ROSC', 'roscTime': 'Čas do ROSC', 'SurvivalDischarge30d': '30-dnevno preživetje ali preživetje do odpusta', 'cpcDischarge': 'Nevrološki izid ob odpustu (CPC)', 'mrsDischarge': 'Nevrološki izid ob odpustu (mRS)', 'survivalStatus': 'Status preživetja', 'transportToHospital': 'Transport v bolnišnico', 'treatmentWithdrawn': 'Zdravljenje prekinjeno (vključno s časom)', 'cod': 'Vzrok smrti', 'organDonation': 'Donacija organov', 'patientReportedOutcome': 'Pacientovo poročilo o izidu', 'qualityOfLife': 'Opredelitev kvalitete življenja (standardizirani vprašalniki, npr. EQ-5D, SF-12)', 'reaLand': 'Država srčnega zastoja', 'reaRegion': 'Regija srčnega zastoja', 'reaConf': 'Srčni zastoj potrjen', 'cprEms': 'Poskus oživljanja', 'cPREMS3Time': 'Kdaj so začeli oživljati NMP', 'noCPR': 'Vzrok, zakaj NMP ne izvaja oživljanja - EuReCa 3', 'patID': 'treba še dodati', 'reaYr': 'Leto srčnega zastoja', 'reaMo': 'Mesec srčnega zastoja', 'reaDay': 'Dan srčnega zastoja', 'reaTime': 'Čas srčnega zastoja', 'reaCause': 'Vzrok srčnega zastoja - EuReCa 3', 'timeTCPR': 'Čas začetka CPR', 'gbystnader': 'Spol očividca', 'ageBystander': 'Starost očividca', 'estimatedAgeBystander': 'Ali je starost očividca ocenjena?', 'cPRbystander3Time': 'Čas začetka CPR očividca', 'helperCPR': 'Ali je DCZ/NMP poslal osebo (ki bi lahko nudila pomoč/oživljanje) na kraj srčnega zastoja', 'helperWho': 'Katero osebo je DCZ/NMP poslal (ki bi lahko nudila pomoč/oživljanje) na kraj srčnega zastoja - EuReCa 3', 'cPRhelper3Time': 'Čas, ko je pričela oseba, ki jo je DCZ/NMP poslal na kraj zastoja (ki bi lahko nudila pomoč/oživljanje), z oživljanjem (TPO) - EuReCa 3', 'defiOrig': 'Kdo je izvedel prvo defibrilacijo? - EuReCa 3', 'timeROSC': 'Čas prvega ROSC', 'endCPR4Time': 'Čas konca CPR', 
'leftScene5Time': 'Čas zapusitve dogodka', 'hospitalArrival6Time': 'Čas prihoda v bolnišnico', 'hospArri': 'Status ob prihodu v bolnišnico', 'dischDay': 'Dan odpusta iz bolnice'}

descriptions = {'caseID': 'Unikaten ID primera', 'systemID': 'Navedi enoto NMP', 'localID': 'Občina, kjer je pacient doživel srčni zastoj', 'age': 'Starost pacienta ob dogodku - datum rojstva ali starost v letih', 'witnesses': 'Definicija osebe, ki je bila poslana, da bi nudila pomoč/oživljanje: oseba, ki jo je alarmiral in na kraj dogodka poslal DCZ/NMP preko SMS aplikacije, app, telefona/radijske postaje, itd... Srčni zastoj vpričo očividcev je definiran, kadar očividci vidijo srčni zastoj (npr. da se je nekdo zgrudil) ali da slišijo, da se je nekdo zgrudil (oz doživel srčni zastoj) ali zasledijo na monitorju srčni zastoj.', 'location': 'Lokacija pacienta ob incidentu', 'pathogenesis': 'Opomomba: neznani razlogi naj bodo opredeljeni kot zdravstvena težava.', 'independentLiving': 'Ali pacient živi sam', 'responseTime': 'Odzivni čas v sekundah - od časa sprejema klica do prihoda do pacienta', 'defibTime': 'Čas do defibrilacije v sekundah - čas od sprejema klica do prvega šoka', 'ttmTemp': 'Ciljna temperatura, če TTM izveden (°C)', 'drugs': 'Set vseh uporabljenih zdravil, dovoljena izbira večih (kot vsota ID-jev vrednosti)', 'airwayControl': 'Set vseh uporabljenih tipov nadzora dihalne poti, dovoljena izbira večih (kot vsota ID-jev vrednosti)', 'cprQuality':'Ali se je med oživljanjem uporabljala kakršna koli naprava za nadzor kvalitete izvedbe oživljanaj?', 'drugTimings': 'JSON, kot opisan', 'targetVent': 'Če je ta spremenljivka uporabljena, vključi podrobnosti o specifičnih ciljih v opisu sistema', 'reperfusionAttempt': 'Set vseh poskusov reperfuzije, dovoljena izbira večih (kot vsota ID-jev vrednosti)', 'lactate': 'mmol/L', 'neuroprognosticTests': 'JSON, kot opisan', 'hospitalVolume': 'Število letnih primerov', 'ecgBLOB': 'EKG datoteka kot base64 kodirani podatki', 'targetBP': 'Ciljni MAP v mmHg', 'roscTime': 'Čas do ROSC v sekundah', 'survivalStatus': 'Opisuje preživetje dogodka do sprejema v bolnišnico', 'treatmentWithdrawn': 'Ure do prekinitve zdravljenja, dnevi naj se pretvorijo v ure (zaokroženo navzgor)', 'cod': 'Vzrok smrti kot koda MKB-10-AM ver. 6', 'organDonation': 'Je pacient donor organov', 'patientReportedOutcome': 'Izidi, ki jih pacient opredeli kot pomembne', 'qualityOfLife': 'JSON, kot opisan', 'reaLand': 'Država srčnega zastoja v tekst formi', 'reaRegion': 'Regija srčnega zastoja v tekst formi', 'cPREMS3Time': 
'Kdaj so začeli oživljati NMP v hh:mm:ss formi', 'noCPR':'Vzrok zakaj NMP ne izvaja oživljanja. V primeru, da je pri spremenljivki Ali je NMP izvajal oživljanje označeno z DA, potem tukaj pustimo prazno.', 'reaTime': 'Čas srčnega zastoja v hh:mm:ss formi', 'reaCause': 'Vzrok za srčni zastoj se predvideva, da je srčni; razen če je znano oz. zelo verjetno, da je povzročen zaradi poškodbe, utopitve, prekomernega odmerka drog, zadušitve, izkravitve, ali katerega koli drugega ne-srčnega vzroka potrjenega s strani NMP.', 'timeTCPR': 'Čas začetka CPR v hh:mm:ss formi', 'ageBystander': 'Starost očividca v XXX formi', 'cPRbystander3Time': 'Čas začetka CPR očividca v hh:mm:ss formi', 'cPRhelper3Time': 'Čas začetka PCR osebe, ki je poslana da pomaga v hh:mm:ss formi', 'defiOrig': 'Pustite prazno, če ni šoka. AED - v ta odgovor so vključeni vsi, ki so uporabili AED, razen osebja NMP, ki je takrat v službi - npr. za očividce ali prve posredovalce, ki uporabljajo AED se označi odgovor; če je član prvih posredovalcev tudi član NMP in ob aktivaciji takrat ni v službi NMP oz. ni del redne aktivirane ekipe NMP ter uporabi AED ob oživljanju, se označi ta odgovor).', 'helperCPR': 'Katerakoli oseba, ki so jo poslali na kraj dogodka, da bi nudila pomoč oz. izvajala oživljanje, in je bila aktivirana s strani DCZ/NMP preko SMS, app, telefon/radijske postaje.', 'timeROSC': 'Čas prvega ROSC v hh:mm:ss formi', 'endCPR4Time': 'Čas konca CPR v hh:mm:ss formi', 'leftScene5Time': 'Čas zapusitve dogodka v hh:mm:ss formi', 'hospitalArrival6Time': 'Čas prihoda v bolnišnico v hh:mm:ss form'}

# first form with data immediately after CA
first_form = ['caseID', 'systemID', 'localID', 'dispIdentifiedCA', 'dispProvidedCPRinst', 'age', 'gender', 'witnesses', 'location', 
'bystanderResponse', 'bystanderResponseTime', 'bystanderAED', 'bystanderAEDTime', 'deadOnArrival', 'firstMonitoredRhy', 'pathogenesis', 
'independentLiving', 'comorbidities', 'vad', 'cardioverterDefib', 'stemiPresent', 'responseTime', 'defibTime', 'ttm', 'ttmTemp', 'drugs', 
'airwayControl', 'cprQuality', 'shocks', 'drugTimings', 'vascularAccess', 'mechanicalCPR', 'targetVent', 'reperfusionAttempt', 
'reperfusionTime', 'rosc', 'roscTime', 'transportToHospital', 
'reaLand', 'reaRegion', 'reaConf', 'cprEms', 'cPREMS3Time', 'noCPR', 'reaTime', 'reaCause', 'timeTCPR', 'gbystnader', 'ageBystander', 'estimatedAgeBystander','cPRbystander3Time', 'helperCPR', 'helperWho', 'cPRhelper3Time', 'defiOrig', 'timeROSC', 'endCPR4Time', 'leftScene5Time', 'hospitalArrival6Time', 'hospArri', ]

# secodn form with data in the hospital 
second_form = ['caseID', 'systemID', 'localID', 'ecls', 'iabp', 'ph', 'lactate', 'glucose', 'neuroprognosticTests', 'specialistHospital', 'hospitalVolume', 'ecg', 
'ecgBLOB', 'targetBP', 'survived', 'SurvivalDischarge30d', 'cpcDischarge', 'mrsDischarge', 'survivalStatus', 'treatmentWithdrawn', 
'cod', 'organDonation', 'patientReportedOutcome', 'qualityOfLife'] #, 'dischDay']



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

# def create_time_widgets(values):
# 	w = dict()
# 	for elt in values:
# 		w[elt] = forms.TimeField(widget=TimePickerInput)
# 	return w

w = create_widgets(values) #
w["ecgBLOB"] = forms.FileInput(attrs={"class" : "form-control", "type" : "file"})


TIME_FORMAT = 'H:i:s'
w["bystanderAEDTime"] = TimePickerInput(format=TIME_FORMAT)

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
	# Date_birth = forms.DateField(label='Datum rojstva', widget=forms.SelectDateWidget(years=[x for x in range(1910,2025)], months=MONTHS))
	Date_birth = forms.DateField(label='Datum rojstva', widget=DatePickerInput())

	All_drugs = forms.MultipleChoiceField(label="Aplicirana zdravila", widget=forms.CheckboxSelectMultiple,choices=values['drugs'])
	# Estimated_bystander_age = forms.ChoiceField(label="Ali je starost očividca ocenjena?", widget=forms.CheckboxInput)

	class Meta: 	
		model = CaseReport
		fields = tuple(first_form)		
		exclude = ("caseID", "reaLand", 
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
	# Date_birth = forms.DateField(label='Datum rojstva', widget=forms.SelectDateWidget(years=[x for x in range(1910,2025)], months=MONTHS))
	Date_birth = forms.DateField(label='Datum rojstva', widget=DatePickerInput)
	Date_of_hospital_discharge = forms.DateField(label='Datum odpusta iz bolnišnice', widget=DatePickerInput, required=False)

	All_drugs = forms.MultipleChoiceField(label="Aplicirana zdravila",widget=forms.CheckboxSelectMultiple,choices=values['drugs'])
	#Estimated_bystander_age = forms.ChoiceField(label="Ali je starost očividca ocenjena?", widget=forms.CheckboxInput)
	class Meta: 
		model = CaseReport
		fields = "__all__"		
		exclude = ("caseID", "reaLand", "age", "dischDay") 
		widgets = w
		labels = titles
		help_texts = descriptions
