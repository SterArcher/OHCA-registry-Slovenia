import random, string
from .models import System, Locale, CaseReport

# IN SHELL (for each model):
# for entry in new_system_entries:
#   entry.save()

# ======================================= SYSTEM ===================================================================

def generate_new_system_entry(n, existing_ids):
    taken_ids =  existing_ids
    entries = []
    for i in range(n):
        id = random.choice([i for i in range(1, 1000) if i not in taken_ids])

        new_entry_system = System(systemID=id,
        friendlyName="".join(random.choice(string.ascii_letters) for _ in range(5)), # friendly indeed
        population=random.randint(1000, 10000),
        attendedCAs=random.randint(500, 700),
        attemptedResusc=random.randint(1, 400),
        casesDNR=random.randint(1, 400),
        casesFutile=random.randint(1, 400),
        casesCirculation=random.randint(1, 400),
        casesUnknown=random.randint(1, 100),
        description="description of the system",
        descriptionSupplemental="supplemental description") 

        taken_ids.append(int(id))   
        entries.append(new_entry_system)

    return (entries, taken_ids)

systems = System.objects.all()

existing_ids = []
for system in systems:
    existing_ids.append(int(system.systemID))

(system_entries, system_ids) = generate_new_system_entry(5, existing_ids)  


# ======================================= LOCALE ===================================================================

def generate_new_locale_entry(n, existing_ids):
    taken_ids = existing_ids
    entries = []
    for i in range(n):
        id = random.choice([i for i in range(1, 1000) if i not in taken_ids])
        
        new_entry_locale = Locale(localID=id, 
        friendlyName="".join(random.choice(string.ascii_letters) for _ in range(7)),
        population=random.randint(1000, 50000),
        attendedCAs=random.randint(500, 1000),
        attemptedResusc=random.randint(10, 500),
        casesDNR=random.randint(10, 300),
        casesFutile=random.randint(10, 300),
        casesCirculation=random.randint(10, 300),
        casesUnknown=random.randint(10, 100),
        description="description",
        descriptionSupplemental="descriptionSupplemental") 

        taken_ids.append(int(id))  
        entries.append(new_entry_locale)

    return (entries, taken_ids)

locales = Locale.objects.all()

existing_ids = []
for locale in locales:
    existing_ids.append(int(locale.localID))

(locale_entries, locale_ids) = generate_new_locale_entry(5, existing_ids)  


# ======================================= CASEREPORT ===================================================================

def generate_new_case_entry(n, existing_ids, system_entries, locale_entries):
    taken_ids = existing_ids
    entries = []
    for i in range(n):
        id = random.choice([i for i in range(100, 10000) if i not in taken_ids])

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

(case_entries, case_ids) = generate_new_case_entry(5, existing_ids, systems, locales)  

