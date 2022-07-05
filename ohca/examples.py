import random, string
from .models import System, Locale, CaseReport
import hashlib

# IN SHELL (for each model):
# for entry in new_system_entries:
#   entry.save()

# generated with the help of extract() function in population.py

municipalities = {'Ajdovščina': '19727', 'Ankaran/Ancarano': '3282', 'Bled': '8250', 'Bloke': '1610', 'Bohinj': '5676', 'Borovnica': '4629', 'Bovec': '3178', 'Brda': '5632', 'Brezovica': '12823', 'Cerklje na Gorenjskem': '7901', 'Cerknica': '11718', 'Cerkno': '4546', 'Črnomelj': '14279', 'Divača': '4371', 'Dobrepolje': '3871', 'Dobrova - Polhov Gradec': '7844', 'Dol pri Ljubljani': '6348', 'Dolenjske Toplice': '3589', 'Domžale': '36905', 'Gorenja vas - Poljane': '7672', 'Gorje': 
'2779', 'Grosuplje': '21333', 'Horjul': '3006', 'Hrpelje - Kozina': '4970', 'Idrija': '11729', 'Ig': '7695', 'Ilirska Bistrica': '13399', 'Ivančna Gorica': 
'17599', 'Izola/Isola': '16647', 'Jesenice': '21758', 'Jezersko': '667', 'Kamnik': '29793', 'Kanal': '5245', 'Kobarid': '4044', 'Kočevje': '15623', 'Komen': '3634', 'Komenda': '6482', 'Koper/Capodistria': '53462', 'Kostel': '678', 'Kranj': '56639', 'Kranjska Gora': '7689', 'Litija': '15720', 'Ljubljana': '293218', 'Log - Dragomer': '3681', 'Logatec': '14699', 'Loška dolina': '3624', 'Loški Potok': '1807', 'Lukovica': '5978', 'Medvode': '16792', 'Mengeš': '8487', 'Metlika': '8452', 'Miren - Kostanjevica': '5072', 'Mirna': '2694', 'Mirna Peč': '3077', 'Mokronog - Trebelno': '3164', 'Moravče': '5522', 'Naklo': '5380', 'Nova Gorica': '31824', 'Novo mesto': '37615', 'Osilnica': '321', 'Piran/Pirano': '18432', 'Pivka': '6230', 'Postojna': '16753', 'Preddvor': '3811', 'Radovljica': '19325', 'Renče - Vogrsko': '4377', 'Ribnica': '9684', 'Semič': '3864', 'Sežana': '13842', 'Sodražica': '2269', 'Straža': '3881', 'Šempeter - Vrtojba': '6164', 'Šenčur': '8893', 'Šentjernej': '7247', 'Šentrupert': '2935', 'Škocjan': '3419', 'Škofja Loka': '23622', 'Škofljica': '11666', 'Šmarješke Toplice': '3522', 'Šmartno pri Litiji': '5700', 'Tolmin': '10953', 'Trebnje': '13413', 'Trzin': '3900', 'Tržič': '15011', 'Velike Lašče': '4584', 'Vipava': '5822', 
'Vodice': '4974', 'Vrhnika': '17684', 'Železniki': '6685', 'Žiri': '4990', 'Žirovnica': '4479', 'Žužemberk': '4719', 'Apače': '3556', 'Beltinci': '8104', 'Benedikt': '2684', 'Bistrica ob Sotli': '1361', 'Braslovče': '5681', 'Brežice': '24370', 'Cankova': '1740', 'Celje': '48679', 'Cerkvenjak': '2179', 'Cirkulane': '2363', 'Črenšovci': '3982', 'Črna na Koroškem': '3201', 'Destrnik': '2632', 'Dobje': '942', 'Dobrna': '2277', 'Dobrovnik/Dobronak': '1263', 'Dornava': 
'2880', 'Dravograd': '8882', 'Duplek': '7015', 'Gorišnica': '4180', 'Gornja Radgona': '8476', 'Gornji Grad': '2552', 'Gornji Petrovci': '2010', 'Grad': '2063', 'Hajdina': '3873', 'Hoče - Slivnica': '11723', 'Hodoš/Hodos': '362', 'Hrastnik': '8963', 'Juršinci': '2501', 'Kidričevo': '6547', 'Kobilje': '532', 'Kostanjevica na Krki': '2453', 'Kozje': '3029', 'Križevci': '3536', 'Krško': '25833', 'Kungota': '4916', 'Kuzma': '1654', 'Laško': '12976', 'Lenart': '8561', 'Lendava/Lendva': '10312', 'Ljubno': '2542', 'Ljutomer': '11140', 'Lovrenc na Pohorju': '2958', 'Luče': '1455', 'Majšperk': '4026', 'Makole': '2048', 'Maribor': '113004', 'Markovci': '4022', 'Mežica': '3567', 'Miklavž na Dravskem polju': '7045', 'Mislinja': '4532', 'Moravske Toplice': '5990', 'Mozirje': '4401', 
'Murska Sobota': '18543', 'Muta': '3402', 'Nazarje': '2682', 'Odranci': '1595', 'Oplotnica': '4131', 'Ormož': '11890', 'Pesnica': '7576', 'Podčetrtek': '3657', 'Podlehnik': '1844', 'Podvelka': '2337', 'Poljčane': '4493', 'Polzela': '6386', 'Prebold': '5302', 'Prevalje': '6732', 'Ptuj': '23509', 'Puconci': '5871', 'Rače - Fram': '7749', 'Radeče': '4146', 'Radenci': '5056', 'Radlje ob Dravi': '6181', 'Ravne na Koroškem': '11228', 'Razkrižje': '1237', 'Rečica ob Savinji': '2324', 'Ribnica na Pohorju': '1141', 'Rogaška Slatina': '11438', 'Rogašovci': '3125', 'Rogatec': '3055', 'Ruše': '7091', 'Selnica ob Dravi': '4513', 
'Sevnica': '17661', 'Slovenj Gradec': '16716', 'Slovenska Bistrica': '26042', 'Slovenske Konjice': '15221', 'Solčava': '524', 'Središče ob Dravi': '1904', 'Starše': '4077', 'Sveta Ana': '2326', 'Sveta Trojica v Slov. goricah': '2194', 'Sveti Andraž v Slov. goricah': '1201', 'Sveti Jurij ob Ščavnici': '2855', 'Sveti Jurij v Slov. goricah': '2118', 'Sveti Tomaž': '2015', 'Šalovci': '1372', 'Šentilj': '8367', 'Šentjur': '19378', 'Šmarje pri Jelšah': '10361', 'Šmartno ob Paki': '3324', 'Šoštanj': '8822', 'Štore': '4396', 'Tabor': '1693', 'Tišina': '3941', 'Trbovlje': '15893', 'Trnovska vas': '1385', 'Turnišče': '3153', 'Velenje': '33548', 'Velika Polana': '1387', 'Veržej': '1371', 'Videm': '5601', 'Vitanje': '2266', 'Vojnik': '9063', 'Vransko': '2672', 'Vuzenica': '2652', 'Zagorje ob Savi': '16307', 'Zavrč': '1506', 'Zreče': '6576', 'Žalec': '21477', 'Žetale': '1309'}

ems_units = {'ZD Ajdovščina': '25549', 'ZD Koper': '56744', 'ZD Bled': '11029', 'ZD Cerknica': '16952', 'ZD Bohinj': '5676', 'ZD Vrhnika': '25994', 'ZD Tolmin': '18175', 'ZD Nova Gorica': '58314', 'ZD Ljubljana': '347574', 'ZD Kranj': '83291', 'ZD Idrija': '16275', 'ZD Črnomelj': '18143', 'ZD Sežana': '26817', 'ZD Grosuplje': '25204', 'ZD Novo mesto': '63188', 'ZD Domžale': '60792', 'ZD Škofja Loka': '42969', 'ZD Ilirska Bistrica': '13399', 'ZD Ivančna Gorica': '17599', 'ZD Izola': '16647', 'ZD Jesenice': '26237', 'ZD Kamnik': '36275', 'ZD Kočevje': '16622', 'ZD Kranjska Gora': '7689', 'ZD Litija': '21420', 'ZD Logatec': '14699', 'ZD Ribnica': '18344', 'ZD Medvode': '16792', 'ZD Metlika': '8452', 'ZD Trebnje': '22206', 'ZD Piran': '18432', 'ZD Postojna': '22983', 'ZD Radovljica': '19325', 'ZD Novo mesto ': '3881', 'ZD Tržič': '15011', 'ZD Gornja Radgona': '19943', 'ZD Murska Sobota': '54775', 'ZD Lenart': '20062', 'ZD Šmarje pri Jelšah': '32901', 'ZD Žalec': '43211', 'ZD Brežice': '24370', 'ZD Celje': '64415', 'ZD Ptuj': '69379', 'ZD Lendava': '22224', 'ZD Ravne na Koroškem': '24728', 'ZD Šentjur': '20320', 'ZD Dravograd': '8882', 'ZD Maribor': '186034', 'ZSDZ NAZARJE': '16480', 'ZD Hrastnik': '8963', 'ZD Krško': '28286', 'ZD Ljutomer': '17284', 'ZD Laško': '12976', 'ZD Slovenska Bistrica': '36714', 'ZD Slovenj Gradec': '21248', 'ZD Radlje ob Dravi': '15713', 'ZD Ormož': '15809', 'ZD Radeče': '4146', 'ZD Sevnica': '17661', 'ZD Slovenske Konjice': '24063', 'ZD Velenje': '45694', 'ZD Trbovlje': '15893', 'ZD Zagorje': '16307'}


# ======================================= SYSTEM ===================================================================

possible_systems = []
for key in ems_units:
    possible_systems.append((key, ems_units[key]))

def generate_new_system_entry(existing_ids, possible_systems):
    taken_ids =  existing_ids
    entries = []
    # for i in range(n):
    while len(possible_systems) > 0:
        id = random.choice([i for i in range(1, 1000) if i not in taken_ids])
        name = random.choice(possible_systems)
        num = int(name[1])//3
        num = int(num)

        new_entry_system = System(systemID=id,
        friendlyName=name[0], #"".join(random.choice(string.ascii_letters) for _ in range(5)), # friendly indeed
        population=int(name[1]), #random.randint(1000, 10000),
        attendedCAs=random.randint(10, int(num)),
        attemptedResusc=random.randint(1, 3*num//4),
        casesDNR=random.randint(1, 1*num//4),
        casesFutile=random.randint(1, 1*num//4),
        casesCirculation=random.randint(1, 1*num//4),
        casesUnknown=random.randint(1, 1*num//8),
        description="description of the system",
        descriptionSupplemental="supplemental description") 

        taken_ids.append(int(id))   
        entries.append(new_entry_system)
        possible_systems.remove(name)

    return (entries, taken_ids)

systems = System.objects.all()

existing_ids = []
for system in systems:
    existing_ids.append(int(system.systemID))

(system_entries, system_ids) = generate_new_system_entry(existing_ids, possible_systems)  


# ======================================= LOCALE ===================================================================

possible_locales = []
for key in municipalities:
    possible_locales.append((key, municipalities[key]))

def generate_new_locale_entry(existing_ids, possible_locales):
    taken_ids = existing_ids
    entries = []
    # for i in vrange(n):
    while len(possible_locales) > 0:
        id = random.choice([i for i in range(1, 1000) if i not in taken_ids])
        name = random.choice(possible_locales)
        num = int(name[1])//3
        num = int(num)
        
        new_entry_locale = Locale(localID=id, 
        friendlyName=name[0],#"".join(random.choice(string.ascii_letters) for _ in range(7)),
        population=int(name[1]), #random.randint(1000, 50000),
        attendedCAs=random.randint(10, num),
        attemptedResusc=random.randint(1, 3*num//4),
        casesDNR=random.randint(1, 1*num//4),
        casesFutile=random.randint(1, 1*num//4),
        casesCirculation=random.randint(1, 1*num//4),
        casesUnknown=random.randint(1, 1*num//8),
        description="description",
        descriptionSupplemental="descriptionSupplemental") 

        taken_ids.append(int(id))  
        entries.append(new_entry_locale)
        possible_locales.remove(name)

    return (entries, taken_ids)

locales = Locale.objects.all()

existing_ids = []
for locale in locales:
    existing_ids.append(int(locale.localID))

(locale_entries, locale_ids) = generate_new_locale_entry(existing_ids, possible_locales)  



# ======================================= CASEREPORT ===================================================================

def generate_new_case_entry(n, existing_ids, system_entries, locale_entries):
    taken_ids = existing_ids
    entries = []
    for i in range(n):
        code = random.choice([i for i in range(100, 10000) if i not in taken_ids])
        hashed = hashlib.sha256(code.encode("utf-8")).hexdigest()
        id = hashed

        new_case_entry = CaseReport(caseID=id,
        # dispatchID=????,
        systemID=random.choice(system_entries),
        localID=random.choice(locale_entries),
        dispIdentifiedCA=random.choice([-1, 0, 1]),
        dispProvidedCPRinst=random.choice([-1, 0, 1]),
        age=random.randint(25, 100),
        gender=random.choice([-1, 0, 1]),
        witnesses=random.randint(-1, 3),
        location =random.randint(-1, 8),
        bystanderResponse=random.randint(-1, 2),
        bystanderResponseTime=random.randint(50, 10000),
        bystanderAED=random.randint(-1, 2),
        bystanderAEDTime=random.randint(50, 10000),
        deadOnArrival=random.randint(-1, 1),
        firstMonitoredRhy=random.randint(-1, 7),
        pathogenesis=random.randint(1, 6),
        independentLiving=random.randint(-1, 1),
        comorbidities=random.randint(-1, 1),
        vad=random.randint(-1, 1),
        cardioverterDefib=random.randint(-1, 2),
        stemiPresent=random.randint(-1, 1),
        responseTime=random.randint(150, 10000),
        defibTime=random.randint(150, 10000),
        ttm=random.randint(-1, 5),
        ttmTemp=random.randint(300, 310),
        drugs=random.choice([-1, 0, 1, 2, 4]),
        airwayControl=random.randint(-1, 8),
        cprQuality=random.randint(-1, 1),
        shocks=random.randint(-1, 5),
        drugTimings={
        "adrenaline": random.randint(10, 180),
        "amiodarone": random.randint(10, 180),
        "vasopressin": random.randint(10, 180),
        },
        vascularAccess=random.randint(-1,4),
        mechanicalCPR=random.randint(-1,3),
        targetVent=random.randint(-1, 4),
        reperfusionAttempt=random.randint(-1, 4),
        reperfusionTime=random.randint(-1, 3),
        ecls=random.randint(-1, 2),
        iabp=random.randint(-1, 1),
        ph=random.randint(-1, 14),
        lactate=random.randint(-1, 10),
        glucose=random.randint(-1, 1),
        neuroprognosticTests="description of neuroprognostic tests",
        specialistHospital=random.randint(-1, 1),
        hospitalVolume=random.randint(10, 500),
        ecg=random.randint(-1, 4),
        ecgBLOB="ECG file as base64 encoded data",  
        targetBP=random.randint(50, 70),
        survived=random.randint(-1, 1),
        rosc=random.randint(-1, 1),
        roscTime=random.randint(1, 200),
        SurvivalDischarge30d=random.randint(-1, 1),
        cpcDischarge=random.choice([-1, 1, 2, 3, 4, 5]),
        mrsDischarge=random.randint(-1, 6),
        survivalStatus=random.randint(-1, 1),
        transportToHospital=random.randint(-1, 1),
        treatmentWithdrawn=random.randint(-1, 50),
        cod="cod", # has to be fixed
        organDonation=random.randint(-1, 1),
        patientReportedOutcome=random.randint(-1, 1),
        qualityOfLife="quality of life")  

        taken_ids.append(int(id))  
        entries.append(new_case_entry)

    return (entries, taken_ids)

cases = CaseReport.objects.all()

existing_ids = []
for case in cases:
    existing_ids.append(int(case.caseID))

systems = System.objects.all()
locales = Locale.objects.all()

# (case_entries, case_ids) = generate_new_case_entry(150, existing_ids, systems, locales)  


