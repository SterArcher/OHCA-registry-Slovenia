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

values = {'dispIdentifiedCA': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'dispProvidedCPRinst': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'gender': [(-1, 'Neznano'), (0, 'Moški'), (1, 'Ženska')], 'witnesses': [(-1, 'Neznano/ni zabeleženo - ni zavedeno'), (0, 'NE, brez prič'), (1, 'DA, v prisotnosti očividca'), (2, 'DA, v prisotnosti ekipe NMP'), (3, 'Oseba, ki je bila poslana na kraj srčnega zastoja, da nudi pomoč/oživljanje')], 'location': [(-1, 'Neznano'), (1, 'Dom/prebivališče'), (2, 'Delovno mesto'), (3, 'Športni/rekreacijski dogodek'), (4, 'Ulica/avtocesta'), (5, 'Javna zgradba'), (6, 'Varovano stanovanje/dom za ostarele'), (7, 'Učna ustanova'), (8, 'Drugo')], 'bystanderResponse': [(-1, 'Neznano'), (0, 'Očividec ni izvajal TPO'), (1, 'Izveden TPO (Samo stiski prsnega koša)'), (2, 'Izveden TPO (Stiski in umetno dihanje)')], 'bystanderAED': [(-1, 'Neznano'), (0, 'Ni bil uporabljen'), (1, 'AED uporabljen, elektrošok ni izveden'), (2, 'AED uporabljen, elektrošok izveden')], 'deadOnArrival': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'firstMonitoredRhy': [(-1, 'Neznano'), (1, 'VT'), (2, 'VT brez pulza'), (3, 'PEA'), (4, 'Asistola'), (5, 'Bradikardia'), (6, 'AED šok ni smiseln'), (7, 'AED šok smiseln')], 'pathogenesis': [(1, 'Zdravstvena težava'), (2, 'Travma'), (3, 'Predoziranje z drogami'), (4, 'Utopitev'), (5, 'Elektrošok'), (6, 'Zadušitev')], 'independentLiving': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'comorbidities': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'vad': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'cardioverterDefib': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Interni'), (2, 'Eksterni')], 'stemiPresent': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'ttm': [(-1, 'Neznano'), (1, 'Med zastojem'), (2, 'Po-ROSC predbolnišnično'), (3, 'Po-ROSC bolnišnično'), (4, 'Terapevtska hipotermija indicirana, neizvedena'), (5, 'Terapevtska hipotermija ni indicirana')], 'drugs': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Adrenaline'), (2, 'Amiodarone'), (4, 'Vasopressin')], 'airwayControl': [(-1, 'Neznano'), (0, 'Brez used'), (1, 'Orofaringealna dihalna pot'), (2, 'Supraglotična dihalna pot'), (4, 'Endotrahealni tubus'), (8, 'Kirurška dihalna pot')], 'cprQuality': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'vascularAccess': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Centralna venska'), (2, 'Periferna IV'), (3, 'IO'), (4, 'Endotrahealna')], 'mechanicalCPR': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Naprava za mehanske kompresije prnega koša (Lucas)'), (2, 'Trak za razporeditev sile'), (3, 'Druga mehanska naprava')], 'targetVent': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Samo O2'), (2, 'Samo CO2'), (3, 'O2 & CO2')], 'reperfusionAttempt': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Samo angiografija'), (2, 'PCI'), (4, 'Tromboliza')], 'reperfusionTime': [(-1, 'Neznano'), (1, 'Med zastojem'), (2, 'Znotraj 24 h od ROSC'), (3, 'Po 24 h, a pred odpustom')], 'ecls': [(-1, 'Neznano'), (0, 'Brez'), (1, 'Pred ROSC'), (2, 'Po ROSC')], 'iabp': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'glucose': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'specialistHospital': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'ecg': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'survived': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'rosc': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'SurvivalDischarge30d': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'survivalStatus': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'transportToHospital': [(-1, 'Neznano'), (0, 'Ne'), (1, 'Da')], 'organDonation': [(-1, 'Neznano'), (0, 'Ni donor'), (1, 'Donor')], 'reaConf': [(-1, 'Neznano'), (0, 'Da'), (1, 'Ne')], 'cprEms': [(-1, 'Neznano'), (0, 'Da'), (1, 'Ne')], 'noCPR': [(-1, 'Neznano'), (0, 'Umrli predhodno'), (1, 'Dokument o izraženi volji proti oživljanju'), (2, 'Želja družine'), (3, 'Želja zdravnika'), (4, 'Uspešni ICD šok'), (5, 'Znaki življenja')], 'reaCause': [(-1, 'Neznano (predviden mrtev)'), (0, 'Srčni'), (1, 'Travma'), (2, 'Potopitev'), (3, 'Respiratorni'), (4, 'Ne-srčni')], 'gbystnader': [(-1, 'Neznano'), (0, 'Moški'), (1, 
'Ženska')],'estimatedAgeBystander': [(-1, 'Neznano'), (0, 'Da'), (1, 'Ne')], 'helperCPR': [(-1, 'Neznano'), (0, 'Da'), (1, 'Ne')], 'helperWho': [(1, 'Osebo, ki jo je na kraj zastoja poslal dispečer (to je katerakoli oseba, za katero ne vemo ali ima opravljen BLS tečaj ali izpolnjuje katerega izmed spodnjih pogojev)'), (2, 'Osebo, ki ima opravljen BLS tečaj, in jo je na kraj zastoja poslal dispečer'), (3, 
'Gasilec (prvi posredovalec), ki ga je na kraj zastoja poslal dispečer'), (4, 'Zdravstveni delavec, ki trenutno ni v službi, in ga je na kraj zastoja poslal dispečer'), (5, 'Ostali, ki jih je na kraj zastoja poslal dispečer (ostale skupine, ki niso navedene zgoraj)')], 'defiOrig': [(-1, 'Neznano'), (0, 'AED'), (1, 'EMS')], 'hospArri': [(-1, 'Neznano'), (0, 'Mrtev'), (1, 'Živ'), (2, 'Brez prevoza do bolnišnice'), (3, 'Prevoz z CPR'), (4, 'Prevoz z ROSC')]}

titles = {'caseID': 'UUID primera', 'systemID': 'Regija srčnega zastoja', 'localID': 'Občina', 'dispIdentifiedCA': 'Dispečer je prepoznal prisotnost zastoja srca', 'dispProvidedCPRinst': 
'Ali je dispečer/NMP dal navodila po telefonu za oživljanje', 'age': 'Starost', 'gender': 'Spol', 'witnesses': 'Ali se je srčni zastoj zgodil vpričo očividcev', 'location': 'Lokacija zastoja', 'bystanderResponse': 'Odziv očividca', 'bystanderResponseTime': 'Začetek izvajanja TPO očividcev', 'bystanderAED': 'Uporaba AED', 'bystanderAEDTime': 'Čas prvega AED šoka očividcev', 'deadOnArrival': 'Mrtvogled', 'firstMonitoredRhy': 'Prvi zaznan ritem', 'pathogenesis': 'Patogeneza', 'independentLiving': 'Samostojno življenje', 'comorbidities': 'Pridružene bolezni', 'vad': 'VAD', 'cardioverterDefib': 'Kardioverter-defibrilator', 'stemiPresent': 'Prisoten STEMI', 'responseTime': 'Odzivni čas', 'defibTime': 'Čas do defibrilacije', 'ttm': 'Terapevtska hipotermija', 'ttmTemp': 'TTM Temperatura', 'drugs': 'Aplicirana zdravila', 'airwayControl': 'Tip nadzora dihalne poti', 'cprQuality': 'Kvaliteta TPO', 'shocks': 'Število elektrošokov', 'drugTimings': 'Čas do aplikacije zdravil', 'vascularAccess': 'Vaskularna pot', 'mechanicalCPR': 'Mehanski stiski prnega koša', 'targetVent': 'Ciljana okisgenacija/ventilacija', 'reperfusionAttempt': 'Poskus reperfuzije', 'reperfusionTime': 'Čas do poskusa reperfuzije', 'ecls': 'ECLS', 'iabp': 'IABP', 'ph': 'pH krvi', 'lactate': 'Laktat', 'glucose': 'Je bila po ROSC glukoza titrirana do določene vrednosti?', 'neuroprognosticTests': 'Število in vrsta nevroprognostičnih testov', 'specialistHospital': 'Ali je bolnišnica specialistični center', 'hospitalVolume': 'Obremenitev bolnišnice', 'ecg': 'EKG z 12 odvodi', 'ecgBLOB': 'EKG datoteka', 'targetBP': 'Ciljano upravljanje krvnega pritiska', 'survived': 'Preživetje', 'rosc': 'ROSC', 'roscTime': 'Čas do ROSC', 'SurvivalDischarge30d': '30-dnevno preživetje ali preživetje do odpusta', 'cpcDischarge': 'Nevrološki izid ob odpustu (CPC)', 'mrsDischarge': 'Nevrološki izid ob odpustu (mRS)', 'survivalStatus': 'Status preživetja', 'transportToHospital': 'Transport v bolnišnico', 'treatmentWithdrawn': 'Zdravljenje prekinjeno (vključno s časom)', 'cod': 'Vzrok smrti', 'organDonation': 'Donacija organov', 'patientReportedOutcome': 'Pacientovo poročilo o izidu', 'qualityOfLife': 'Opredelitev kvalitete življenja (standardizirani vprašalniki, npr. EQ-5D, SF-12)', 'reaLand': 'Država srčnega zastoja', 'reaRegion': 'Regija srčnega zastoja', 'reaConf': 'Srčni zastoj potrjen', 'cprEms': 'Poskus oživljanja', 'cPREMS3Time': 'Kdaj so začeli oživljati NMP', 'noCPR': 'NMP ni oživljal', 'patID': 'treba še dodati', 'reaYr': 'Leto srčnega zastoja', 'reaMo': 'Mesec srčnega zastoja', 'reaDay': 'Dan srčnega zastoja', 'reaTime': 'Čas srčnega zastoja', 'reaCause': 'Vzrok srčnega zastoja', 'timeTCPR': 'Čas začetka CPR', 'gbystnader': 'Spol očividca', 'ageBystander': 'Starost očividca', 'estimatedAgeBystander': 'Ali je starost očividca ocenjena?', 'cPRbystander3Time': 'Čas začetka CPR očividca', 'helperCPR': 'Ali je DCZ/NMP poslal osebo (ki bi lahko nudila pomoč/oživljanje) na kraj srčnega zastoja', 'helperWho': 'Katero osebo je DCZ/NMP poslal (ki bi lahko nudila pomoč/oživljanje) na kraj srčnega zastoja', 'cPRhelper3Time': 'Čas začetka PCR osebe, ki je poslana da pomaga', 'defiOrig': 'Prvi šok je dostavil AED ali NMP', 'timeROSC': 'Čas prvega ROSC', 'endCPR4Time': 'Čas konca CPR', 
'leftScene5Time': 'Čas zapusitve dogodka', 'hospitalArrival6Time': 'Čas prihoda v bolnišnico', 'hospArri': 'Status ob prihodu v bolnišnico', 'dischDay': 'Dan odpusta iz bolnice'}

descriptions = {'caseID': 'Unikaten ID primera', 'systemID': 'Navedi enoto NMP', 'localID': 'Občina, kjer je pacient doživel srčni zastoj', 'age': 'Starost pacienta ob dogodku - datum rojstva ali starost v letih', 'witnesses': 'Definicija osebe, ki je bila poslana, da bi nudila pomoč/oživljanje: oseba, ki jo je alarmiral in na kraj dogodka poslal DCZ/NMP preko SMS aplikacije, app, telefona/radijske postaje, itd... Srčni zastoj vpričo očividcev je definiran, kadar očividci vidijo srčni zastoj (npr. da se je nekdo zgrudil) ali da slišijo, da se je nekdo zgrudil (oz doživel srčni zastoj) ali zasledijo na monitorju srčni zastoj.', 'location': 'Lokacija pacienta ob incidentu', 'pathogenesis': 'Opomomba: neznani razlogi naj bodo opredeljeni kot zdravstvena težava.', 'independentLiving': 'Ali pacient živi sam', 'responseTime': 'Odzivni čas v sekundah - od časa sprejema klica do prihoda do pacienta', 'defibTime': 'Čas do defibrilacije v sekundah - čas od sprejema klica do prvega šoka', 'ttmTemp': 'Ciljna temperatura, če TTM izveden (°C)', 'drugs': 'Set vseh uporabljenih zdravil, dovoljena izbira večih (kot vsota ID-jev vrednosti)', 'airwayControl': 'Set vseh uporabljenih tipov nadzora dihalne poti, dovoljena izbira večih (kot vsota ID-jev vrednosti)', 'cprQuality':'Ali se je med oživljanjem uporabljala kakršna koli naprava za nadzor kvalitete izvedbe oživljanaj?', 'drugTimings': 'JSON, kot opisan', 'targetVent': 'Če je ta spremenljivka uporabljena, vključi podrobnosti o specifičnih ciljih v opisu sistema', 'reperfusionAttempt': 'Set vseh poskusov reperfuzije, dovoljena izbira večih (kot vsota ID-jev vrednosti)', 'lactate': 'mmol/L', 'neuroprognosticTests': 'JSON, kot opisan', 'hospitalVolume': 'Število letnih primerov', 'ecgBLOB': 'EKG datoteka kot base64 kodirani podatki', 'targetBP': 'Ciljni MAP v mmHg', 'roscTime': 'Čas do ROSC v sekundah', 'survivalStatus': 'Opisuje preživetje dogodka do sprejema v bolnišnico', 'treatmentWithdrawn': 'Ure do prekinitve zdravljenja, dnevi naj se pretvorijo v ure (zaokroženo navzgor)', 'cod': 'Vzrok smrti kot koda MKB-10-AM ver. 6', 'organDonation': 'Je pacient donor organov', 'patientReportedOutcome': 'Izidi, ki jih pacient opredeli kot pomembne', 'qualityOfLife': 'JSON, kot opisan', 'reaLand': 'Država srčnega zastoja v tekst formi', 'reaRegion': 'Regija srčnega zastoja v tekst formi', 'cPREMS3Time': 
'Kdaj so začeli oživljati NMP v hh:mm:ss formi', 'reaTime': 'Čas srčnega zastoja v hh:mm:ss formi', 'timeTCPR': 'Čas začetka CPR v hh:mm:ss formi', 'ageBystander': 'Starost očividca v XXX formi', 'cPRbystander3Time': 'Čas začetka CPR očividca v hh:mm:ss formi', 'cPRhelper3Time': 'Čas začetka PCR osebe, ki je poslana da pomaga v hh:mm:ss formi', 'helperCPR': 'Katerakoli oseba, ki so jo poslali na kraj dogodka, da bi nudila pomoč oz. izvajala oživljanje, in je bila aktivirana s strani DCZ/NMP preko SMS, app, telefon/radijske postaje.', 'timeROSC': 'Čas prvega ROSC v hh:mm:ss formi', 'endCPR4Time': 'Čas konca CPR v hh:mm:ss formi', 'leftScene5Time': 'Čas zapusitve dogodka v hh:mm:ss formi', 'hospitalArrival6Time': 'Čas prihoda v bolnišnico v hh:mm:ss form'}


# # v form se vpise samo ZD, obcina se doloci samodejno glede na ta slovar ki je bil narejen po https://github.com/SterArcher/OHCA-registry-Slovenia/blob/main/data/population/preb.csv 
# ems = {'Ajdovščina': 'ZD Ajdovščina', 'Ankaran': 'ZD Koper', 'Apače': 'ZD Gornja Radgona', 'Beltinci': 'ZD Murska Sobota', 'Benedikt': 'ZD Lenart', 'Bistrica ob Sotli': 'ZD Šmarje pri Jelšah', 'Bled': 'ZD Bled', 'Bloke': 'ZD Cerknica', 'Bohinj': 'ZD Bled', 'Borovnica': 'RP UKCL', 'Bovec': 'ZD Tolmin', 
# 'Braslovče': 'ZD Žalec', 'Brda': 'ZD Nova Gorica', 'Brežice': 'ZD Brežice', 'Brezovica': 'RP UKCL', 'Cankova': 'ZD Murska Sobota', 'Celje': 'ZD Celje', 'Cerklje na Gorenjskem': 'ZD Kranj', 'Cerknica': 'ZD Cerknica', 'Cerkno': 'ZD Idrija', 'Cerkvenjak': 'ZD Lenart', 'Cirkulane': 'ZD Ptuj', 'Črenšovci': 'ZD Lendava', 'Črna na Koroškem': 'Zdravstveno reševalni center Koroške', 'Črnomelj': 'ZD Črnomelj', 'Destrnik': 'ZD Ptuj', 'Divača': 'ZD Sežana', 'Dobje': 
# 'ZD Šentjur', 'Dobrepolje': 'RP UKCL', 'Dobrna': 'ZD Celje', 'Dobrova - Polhov Gradec': 'RP UKCL', 'Dobrovnik': 'ZD Lendava', 'Dol pri Ljubljani': 'RP UKCL', 'Dolenjske Toplice': 'ZD Novo mesto', 'Domžale': 'ZD Domžale', 'Dornava': 'ZD Ptuj', 'Dravograd': 'Zdravstveno reševalni center Koroške', 'Duplek': 'ZD Maribor', 'Gorenja vas - Poljane': 'ZD Škofja Loka', 'Gorišnica': 'ZD Ptuj', 'Gorje': 'ZD Bled', 'Gornja Radgona': 'ZD Gornja Radgona', 'Gornji Grad': 'ZSDZ NAZARJE', 'Gornji Petrovci': 'ZD Murska Sobota', 'Grad': 'ZD Murska Sobota', 'Grosuplje': 'RP UKCL', 'Hajdina': 'ZD Ptuj', 'Hoče - Slivnica': 'ZD Maribor', 'Hodoš': 'ZD Murska Sobota', 'Horjul': 'RP UKCL', 'Hrastnik': 'ZD Hrastnik', 'Hrpelje - Kozina': 'ZD Sežana', 'Idrija': 'ZD Idrija', 'Ig': 'RP UKCL', 'Ilirska Bistrica': 'ZD Ilirska Bistrica', 'Ivančna Gorica': 'RP UKCL', 'Izola': 'ZD Izola', 'Jesenice': 'ZD Jesenice', 'Jezersko': 'ZD Kranj', 'Juršinci': 'ZD Ptuj', 'Kamnik': 'ZD Kamnik', 'Kanal': 'ZD Nova Gorica', 'Kidričevo': 'ZD Ptuj', 'Kobarid': 'ZD Tolmin', 'Kobilje': 'ZD Lendava', 'Kočevje': 'ZD Kočevje', 'Komen': 'ZD Sežana', 'Komenda': 'ZD Kamnik', 'Koper': 'ZD Koper', 'Kostanjevica na Krki': 'ZD Krško', 
# 'Kostel': 'ZD Kočevje', 'Kozje': 'ZD Šmarje pri Jelšah', 'Kranj': 'ZD Kranj', 'Kranjska Gora': 'ZD Jesenice', 'Križevci': 'ZD Ljutomer', 'Krško': 'ZD Krško', 'Kungota': 'ZD Maribor', 'Kuzma': 'ZD Murska Sobota', 'Laško': 'ZD Laško', 'Lenart': 'ZD Lenart', 'Lendava': 'ZD Lendava', 'Litija': 'ZD Litija', 'Ljubljana': 'RP UKCL', 'Ljubno': 'ZSDZ NAZARJE', 'Ljutomer': 'ZD Ljutomer', 'Log - Dragomer': 'RP UKCL', 'Logatec': 'ZD Logatec', 'Loška dolina': 'ZD Cerknica', 'Loški Potok': 'ZD Ribnica', 'Lovrenc na Pohorju': 'ZD Maribor', 'Luče': 'ZSDZ NAZARJE', 'Lukovica': 'ZD Domžale', 'Majšperk': 'ZD Ptuj', 'Makole': 'ZD Slovenska Bistrica', 'Maribor': 'ZD Maribor', 'Markovci': 'ZD Ptuj', 'Medvode': 'RP UKCL', 'Mengeš': 'ZD Domžale', 'Metlika': 'ZD Metlika', 
# 'Mežica': 'Zdravstveno reševalni center Koroške', 'Miklavž na Dravskem polju': 'ZD Maribor', 'Miren - Kostanjevica': 'ZD Nova Gorica', 'Mirna': 'ZD Trebnje', 'Mirna Peč': 'ZD Novo mesto', 'Mislinja': 'Zdravstveno reševalni center Koroške', 'Mokronog - Trebelno': 'ZD Trebnje', 'Moravče': 'ZD Domžale', 'Moravske Toplice': 'ZD Murska Sobota', 'Mozirje': 'ZSDZ NAZARJE', 'Murska Sobota': 'ZD Murska Sobota', 'Muta': 'Zdravstveno reševalni center Koroške', 'Naklo': 'ZD Kranj', 'Nazarje': 'ZSDZ NAZARJE', 'Nova Gorica': 'ZD Nova Gorica', 'Novo mesto': 'ZD Novo mesto', 'Odranci': 'ZD Lendava', 'Oplotnica': 'ZD Slovenska Bistrica', 'Ormož': 'ZD Ormož', 'Osilnica': 'ZD Kočevje', 'Pesnica': 'ZD Maribor', 'Piran': 'ZD Koper', 'Pivka': 'ZD Postojna', 'Podčetrtek': 'ZD Šmarje pri Jelšah', 'Podlehnik': 'ZD Ptuj', 'Podvelka': 'Zdravstveno reševalni center Koroške', 'Poljčane': 'ZD Slovenska Bistrica', 'Polzela': 'ZD Žalec', 'Postojna': 'ZD Postojna', 'Prebold': 'ZD Žalec', 'Preddvor': 'ZD Kranj', 'Prevalje': 'Zdravstveno reševalni center Koroške', 'Ptuj': 'ZD Ptuj', 'Puconci': 'ZD Murska Sobota', 'Rače - Fram': 'ZD Maribor', 'Radeče': 'ZD Radeče', 'Radenci': 'ZD Gornja Radgona', 'Radlje ob Dravi': 'Zdravstveno reševalni center Koroške', 'Radovljica': 'ZD Bled', 'Ravne na Koroškem': 'Zdravstveno reševalni center Koroške', 'Razkrižje': 'ZD Ljutomer', 'Rečica ob Savinji': 'ZSDZ NAZARJE', 'Renče - Vogrsko': 'ZD Nova Gorica', 'Ribnica': 'ZD Ribnica', 'Ribnica na Pohorju': 'Zdravstveno reševalni center Koroške', 'Rogaška Slatina': 'ZD Šmarje pri Jelšah', 'Rogašovci': 'ZD Murska Sobota', 'Rogatec': 'ZD Šmarje pri Jelšah', 'Ruše': 'ZD Maribor', 'Šalovci': 'ZD Murska Sobota', 'Selnica ob Dravi': 'ZD Maribor', 'Semič': 'ZD Črnomelj', 'Šempeter - Vrtojba': 'ZD Nova Gorica', 'Šenčur': 'ZD Kranj', 'Šentilj': 'ZD Maribor', 'Šentjernej': 'ZD Novo mesto', 'Šentjur': 'ZD Šentjur', 'Šentrupert': 'ZD Trebnje', 'Sevnica': 'ZD Sevnica', 'Sežana': 'ZD Sežana', 'Škocjan': 'ZD Novo mesto', 'Škofja Loka': 'ZD Škofja Loka', 'Škofljica': 'RP UKCL', 'Slovenj Gradec': 'Zdravstveno reševalni center Koroške', 'Slovenska Bistrica': 'ZD Slovenska Bistrica', 'Slovenske Konjice': 'ZD Slovenske Konjice', 'Šmarje pri Jelšah': 'ZD Šmarje pri Jelšah', 'Šmarješke Toplice': 'ZD Novo mesto', 'Šmartno ob Paki': 'ZD Velenje', 'Šmartno pri Litiji': 'ZD Litija', 'Sodražica': 'ZD Ribnica', 'Solčava': 'ZSDZ NAZARJE', 'Šoštanj': 'ZD Velenje', 'Središče ob Dravi': 
# 'ZD Ormož', 'Starše': 'ZD Maribor', 'Štore': 'ZD Celje', 'Straža': 'ZD Novo mesto', 'Sveta Ana': 'ZD Lenart', 'Sveta Trojica v Slov. goricah': 'ZD Lenart', 'Sveti Andraž v Slov. goricah': '(prazno)', 'Sveti Jurij ob Ščavnici': 'ZD Gornja Radgona', 'Sveti Jurij v Slov. goricah': 'ZD Lenart', 'Sveti Tomaž': 'ZD Ormož', 'Tabor': 'ZD Žalec', 'Tišina': 'ZD Murska Sobota', 'Tolmin': 'ZD Tolmin', 'Trbovlje': 'ZD Trbovlje', 'Trebnje': 'ZD Trebnje', 'Trnovska vas': 'ZD Ptuj', 'Tržič': 'OZG Gorenjske', 'Trzin': 'ZD Domžale', 'Turnišče': 'ZD Lendava', 'Velenje': 'ZD Velenje', 'Velika Polana': 'ZD Lendava', 'Velike Lašče': 'RP UKCL', 'Veržej': 'ZD Ljutomer', 'Videm': 'ZD Ptuj', 'Vipava': 'ZD Ajdovščina', 'Vitanje': 'ZD Slovenske Konjice', 'Vodice': 'RP UKCL', 'Vojnik': 'ZD Celje', 'Vransko': 'ZD Žalec', 'Vrhnika': 'RP UKCL', 'Vuzenica': 'Zdravstveno reševalni center Koroške', 'Zagorje ob Savi': 'ZD Zagorje', 'Žalec': 'ZD Žalec', 'Zavrč': 'ZD Ptuj', 'Železniki': 'ZD Škofja Loka', 'Žetale': 'ZD Ptuj', 'Žiri': 'ZD Škofja Loka', 'Žirovnica': 'ZD Jesenice', 'Zreče': 'ZD Slovenske Konjice', 'Žužemberk': 'ZD Novo mesto'}

# first form with data immediately after CA
form1 = ['caseID', 'systemID', 'localID', 'dispIdentifiedCA', 'dispProvidedCPRinst', 'age', 'gender', 'witnesses', 'location', 
'bystanderResponse', 'bystanderResponseTime', 'bystanderAED', 'bystanderAEDTime', 'deadOnArrival', 'firstMonitoredRhy', 'pathogenesis', 
'independentLiving', 'comorbidities', 'vad', 'cardioverterDefib', 'stemiPresent', 'responseTime', 'defibTime', 'ttm', 'ttmTemp', 'drugs', 
'airwayControl', 'cprQuality', 'shocks', 'drugTimings', 'vascularAccess', 'mechanicalCPR', 'targetVent', 'reperfusionAttempt', 
'reperfusionTime', 'rosc', 'roscTime', 'transportToHospital', 
'reaLand', 'reaRegion', 'reaConf', 'cprEms', 'cPREMS3Time', 'noCPR', 'reaTime', 'reaCause', 'timeTCPR', 'gbystnader', 'ageBystander', 'estimatedAgeBystander','cPRbystander3Time', 'helperCPR', 'helperWho', 'cPRhelper3Time', 'defiOrig', 'timeROSC', 'endCPR4Time', 'leftScene5Time', 'hospitalArrival6Time', 'hospArri', ]

# secodn form with data in the hospital 
form2 = ['caseID', 'systemID', 'localID', 'ecls', 'iabp', 'ph', 'lactate', 'glucose', 'neuroprognosticTests', 'specialistHospital', 'hospitalVolume', 'ecg', 
'ecgBLOB', 'targetBP', 'survived', 'SurvivalDischarge30d', 'cpcDischarge', 'mrsDischarge', 'survivalStatus', 'treatmentWithdrawn', 
'cod', 'organDonation', 'patientReportedOutcome', 'qualityOfLife', 'dischDay']


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

def create_time_widgets(values):
	w = dict()
	for elt in values:
		w[elt] = forms.TimeField(widget=TimePickerInput)
	return w

w = create_widgets(values) #
w["ecgBLOB"] = forms.FileInput(attrs={"class" : "form-control", "type" : "file"})

# values2 = ["bystanderResponseTime", "bystanderAEDTime", "responseTime", "defibTime", "roscTime"]
# values2 = ["bystanderAEDTime"]
# ww = create_time_widgets(values2)
# for elt in ww:
# 	w[elt] = ww[elt]
# w = dict()
TIME_FORMAT = 'H:i:s'
w["bystanderAEDTime"] = TimePickerInput(format=TIME_FORMAT)
# w["roscTime"] = forms.DateField(widget=forms.DateInput(attrs={'class':'timepicker'}))
# w[""]

# w["Patient_name"] = forms.TextInput(attrs={"class" : "form-control", "style" : "max-width: 300px;"})
# w["drugTimings"] = forms.Textarea(attrs={"class" : "form-control", "style" : "max-width: 500px;"})

# dodatni helper texti
hilfe = {
            # 'bystanderResponseTime': 'Tukaj zaenkrat utipkaj -1 ali manj, da bo delalo, bomo zrihtali :)',
			# 'bystanderAEDTime' : 'tukaj tudi -1 ali manj plis',
			'firstMonitoredRhy' : 'tukej si lahko zaenkrat zbereš samo enega od prvih dveh',
			# 'specialistHospital' : 'Tukaj nas zanima ali je bolnišnica specialistični center',
		}

for elt in hilfe:
	if elt in descriptions:
		descriptions[elt] += ' // ' + hilfe[elt]
	else:
		descriptions[elt] = hilfe[elt]

MONTHS = {
    1:_('januar'), 2:_('februar'), 3:_('marec'), 4:_('april'),
    5:_('maj'), 6:_('junij'), 7:_('julij'), 8:_('avgust'),
    9:_('september'), 10:_('oktober'), 11:_('novebmer'), 12:_('december')
}

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
	Date_birth = forms.DateField(label='Datum rojstva', widget=forms.SelectDateWidget(years=[x for x in range(1910,2025)], months=MONTHS))
	# Date_birth = forms.DateField(label='Datum rojstva', widget=DatePickerInput)

	All_drugs = forms.MultipleChoiceField(label="Aplicirana zdravila",widget=forms.CheckboxSelectMultiple,choices=values['drugs'])
	#Estimated_bystander_age = forms.ChoiceField(label="Ali je starost očividca ocenjena?", widget=forms.CheckboxInput)
	class Meta: 	
		model = CaseReport
		fields = tuple(form1)		
		exclude = ("caseID", "reaLand", "age", "dischDay") 
		widgets = w
		labels = titles
		help_texts = descriptions

	
class MySecondNewFrom(forms.ModelForm):

	Patient_name = forms.CharField(label="Ime pacienta")
	Patient_surname = forms.CharField(label="Priimek pacienta")
	# Date = forms.DateField(label='Datum srčnega zastoja', widget=forms.SelectDateWidget(months=MONTHS, years=[x for x in range(2020,2025)]))
	Date = forms.DateField(label='Datum srčnega zastoja', widget=DatePickerInput())
	Date_birth = forms.DateField(label='Datum rojstva', widget=forms.SelectDateWidget(years=[x for x in range(1910,2025)], months=MONTHS))
	# Date_birth = forms.DateField(label='Datum rojstva', widget=DatePickerInput)
	Date_of_hospital_discharge = forms.DateField(label='Datum odpusta iz bolnišnice', widget=DatePickerInput, required=False)
	class Meta: 
		model = CaseReport
		fields = tuple(form2)		
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
	Date_birth = forms.DateField(label='Datum rojstva', widget=forms.SelectDateWidget(years=[x for x in range(1910,2025)], months=MONTHS))
	# Date_birth = forms.DateField(label='Datum rojstva', widget=DatePickerInput)
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
