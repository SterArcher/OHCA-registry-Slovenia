from ohca.models import System, CaseReport, Locale
import csv
from django.http import HttpResponse
from django.db.models import Q 

def queries(system_list):
    "Takes the system and summarizes its data according to Utstein specifications."
    all_elements = CaseReport.objects.all().values() # returns queryset of dictionaries   
    
    case = CaseReport.objects.none() # empty queryset
    for system in system_list:
        sysID = system.systemID
        case = case | CaseReport.objects.all().filter(systemID__exact=sysID)

    # EMS
    # EMS description - if there's only one system then it returns its description?

    # RESPONSE TIMES (assuming normal distribution of times?)
    cases_with_time = case.exclude(responseTime__isnull=True).exclude(responseTime__exact=-1) 
    num_cases = cases_with_time.count()
    time = 0
    for i in range(len(cases_with_time)):
        time += cases_with_time[i].responseTime
    if num_cases > 0:
        mean_resptime = time / num_cases
    else:
        mean_resptime = 0
    # standard deviation
    sd = 0
    for i in range(len(cases_with_time)):
        sd += (cases_with_time[i].responseTime - mean_resptime)**2
    if num_cases > 0:
        standard_deviation = (sd / num_cases)**0.5
    else:
        standard_deviation = 0
    fractile = 1.28 * standard_deviation + mean_resptime


    # DISPATCH
    disp_idca = case.filter(dispIdentifiedCA__exact=1).count()
    disp_not_idca = case.filter(dispIdentifiedCA__exact=0).count()
    disp_idca_unknown = case.filter(dispIdentifiedCA__exact=-1).count()
    disp_cpr = case.filter(dispProvidedCPRinst__exact=1).count()
    disp_not_cpr = case.filter(dispProvidedCPRinst__exact=0).count()
    disp_cpr_unknown = case.filter(dispProvidedCPRinst__exact=-1).count()
    dispatch_dict = {"Response time (90-th percentile)" : fractile,
    "Dispatcher ID CA - Yes" : disp_idca,
    "Dispatcher ID CA - No" : disp_not_idca,
    "Dispatcher ID CA - unknown" : disp_idca_unknown,
    "Dispatcher CPR - Yes" : disp_cpr,
    "Dispatcher CPR - No" : disp_not_cpr,
    "Dispatcher CPR - unknown" : disp_cpr_unknown}

    # GENERAL 
    systems = System.objects.all().exclude(population__isnull=True) # exclude systems with no data on population
    population_served, num_cases, resusc_attempted, resusc_not_attempted = 0, 0, 0, 0
    dnar, obv_dead, life_signs = 0, 0, 0
    for system in systems:
        population_served += system.population
        num_cases += system.attendedCAs
        resusc_attempted += system.attemptedResusc
        dnar += system.casesDNR
        life_signs += system.casesFutile + system.casesCirculation # where does futile belong?
    obv_dead = case.filter(deadOnArrival__exact=1).count()
    resusc_not_attempted = num_cases - resusc_attempted  

    resuscitation = case.filter(Q(bystanderResponse__exact=1) | Q(bystanderResponse__exact=2) | Q(bystanderAED__exact=2)) # shock not delivered counts as resuscitation or not?
    # only cases where resuscitation was attemted
    vf = resuscitation.filter(firstMonitoredRhy__exact=2).count() # pulseless VT?
    vt = resuscitation.filter(firstMonitoredRhy__exact=1).count()
    pea = resuscitation.filter(firstMonitoredRhy__exact=3).count()
    asys = resuscitation.filter(firstMonitoredRhy__exact=4).count()
    brady = resuscitation.filter(firstMonitoredRhy__exact=5).count()
    aed_shockable = resuscitation.filter(firstMonitoredRhy__exact=7).count()
    aed_non_shockable = resuscitation.filter(firstMonitoredRhy__exact=6).count()
    rhy_nr = resuscitation.filter(firstMonitoredRhy__isnull=True).count()
    rhy_unknown = resuscitation.filter(firstMonitoredRhy__exact=-1).count()
    general_dict = {"Total population served" : population_served, 
    "Total number of cases" : num_cases,
    "Resuscitation not attempted" : resusc_not_attempted,
    "DNAR" : dnar,
    "Obviously dead" : obv_dead,
    "Signs of life" : life_signs,
    "Resuscitation attempted" : resusc_attempted, 
    "VF":vf,
    "VT":vt,
    "PEA":pea,
    "Asystole":asys,
    "Bradycardia":brady,
    "AED non-shockable":aed_non_shockable,
    "AED shockable": aed_shockable,
    "First monitored rhytm not recorded" : rhy_nr,
    "First monitored rhytm unknown" : rhy_unknown
    }

    # Location
    home = case.filter(location__exact=1).count()
    work = case.filter(location__exact=2).count()
    rec = case.filter(location__exact=3).count()
    public = case.filter(location__exact=5).count()
    educ = case.filter(location__exact=7).count()
    nursing = case.filter(location__exact=6).count()
    street = case.filter(location__exact=4).count()
    loc_other = case.filter(location__exact=8).count()
    loc_unknown = case.filter(location__exact=-1).count()
    location = [home, work, rec, public, educ, nursing, street, loc_other, loc_unknown]
    location_dict = {"Location - home" : home, 
    "Location - work" : work,
    "Location - rec" : rec,
    "Location - public" : public,
    "Location - educ" : educ,
    "Location - nursing" : nursing,
    "Location - street" : street,
    "Location - other location" : loc_other,
    "Location - unknown" : loc_unknown}

    # Patient
    # average age
    cases_with_age = case.exclude(age__isnull=True) # gledam samo tiste ki imajo neko vrednost
    num_cases = cases_with_age.count()
    age = 0
    for i in range(len(cases_with_age)):
        age += cases_with_age[i].age
    if num_cases > 0:
        mean_age = age / num_cases
    else:
        mean_age = 0

    # standard deviation
    sd = 0
    for i in range(len(cases_with_age)):
        sd += (cases_with_age[i].age - mean_age)**2
    if num_cases > 0:
        standard_deviation = (sd / num_cases)**0.5
    else:
        standard_deviation = 0

    age_unknown = case.exclude(age__isnull=True).count()
    males = case.filter(gender__exact=0).count()
    females = case.filter(gender__exact=1).count()
    gender_unknown = case.filter(gender__exact=-1).count()
    patient_dict = {"Average age" : mean_age, 
    "Standrad deviation" : standard_deviation, 
    "Age unknown" : age_unknown,
    "Males" : males, 
    "Females" : females, 
    "Genader unknwon" : gender_unknown}

    # Witnessed
    bystander = case.filter(Q(witnesses__exact=1) | Q(witnesses__exact=3)).count() # just bystander or both
    ems = case.filter(Q(witnesses__exact=2) | Q(witnesses__exact=3)).count() # just ems or both
    unwitnessed = case.filter(witnesses__exact=0).count()
    bystander_ems = case.filter(witnesses__exact=3).count()
    witnessed_unknown = case.filter(witnesses__exact=-1).count()
    witnessed_dict = {"Bystander" : bystander + bystander_ems, 
    "EMS" : ems + bystander_ems, 
    "Unwitnessed" : unwitnessed, 
    "Witnessed unknown" : witnessed_unknown}

    # bystander response
    no_bcpr = case.filter(bystanderResponse__exact=0).count()
    cc_only = case.filter(bystanderResponse__exact=1).count()
    cc_vent = case.filter(bystanderResponse__exact=2).count()
    bcpr = case.filter(Q(bystanderResponse__exact=1) | Q(bystanderResponse__exact=2)).count()
    bres_unknown = case.filter(bystanderResponse__exact=-1).count()
    banalyse = 0
    bshock = case.filter(bystanderAED__exact=2).count() # shock delivered, kaj pa shock not delivered?
    baed_unknown = case.filter(bystanderAED__exact=-1).count()
    bystander_response_dict = {"No bCPR" : no_bcpr, 
    "bCPR" : bcpr, 
    "CC Only" : cc_only, 
    "CC/vent" : cc_vent, 
    "Bystander CPR unknown" : bres_unknown,
    "Bystander AED analyse" : banalyse, 
    "Bystander AED Shock" : bshock, 
    "Bystander AED unknown" : baed_unknown}

    # etiology
    medical = case.filter(pathogenesis__exact=1).count()
    trauma = case.filter(pathogenesis__exact=2).count()
    overdose = case.filter(pathogenesis__exact=3).count()
    drowning = case.filter(pathogenesis__exact=4).count()
    electrocution = case.filter(pathogenesis__exact=5).count()
    asphyxial = case.filter(pathogenesis__exact=6).count()
    etiology_not_recorded = case.filter(pathogenesis__isnull=True).count()
    etiology_dict = {"Medical" : medical, "Trauma" : trauma, "Overdose" : overdose, "Drowning" : drowning, 
    "Electrocution" : electrocution, "Asphyxial" : asphyxial, "Etiology not recorded" : etiology_not_recorded}

    # ems process
    # first_defib_time = case.exclude(defibTime__isnull=True).exclude(defibTime__exact=-1).count()
    cases_with_defibtime = case.exclude(defibTime__isnull=True).exclude(defibTime__exact=-1) # gledam samo tiste ki imajo neko vrednost
    num_cases = cases_with_defibtime.count()
    defibtime = 0
    for i in range(len(cases_with_defibtime)):
        defibtime += cases_with_defibtime[i].defibTime
    if num_cases > 0:
        mean_defibtime = defibtime / num_cases
    else:
        mean_defibtime = 0

    ems_ttc_indicated_done = case.filter(Q(ttm__exact=1) | Q(ttm__exact=2)).count()
    ems_ttc_indicated_not_done = case.filter(ttm__exact=4).count() # doesn't differentiate between hospital and ems process
    ems_ttc_not_indicated = case.filter(ttm__exact=5).count() # doesn't differentiate between hospital and ems process
    ems_ttc_unknown = case.filter(ttm__exact=-1).count() # doesn't differentiate between hospital and ems process
    drugs_given = case.exclude(drugs__isnull=True).exclude(drugs__exact=-1).count()
    # adrenaline = case.filter(Q(drugs__exact=1) | Q(drugs__exact=3) | Q(drugs__exact=5))
    # amiodarone = case.filter(Q(drugs__exact=2) | Q(drugs__exact=3) | Q(drugs__exact=6))
    # vasopressin = case.filter(Q(drugs__exact=4) | Q(drugs__exact=5) | Q(drugs__exact=6))
    EMS_process_dict = {"First defib time" : mean_defibtime, 
    "EMS Targeted Temp Control - indicated, done" : ems_ttc_indicated_done,
    "EMS Targeted Temp Control - indicated, not done" : ems_ttc_indicated_not_done,
    "EMS Targeted Temp Control - not indicated, done" : ems_ttc_not_indicated,
    "EMS Targeted Temp Control - unknown" : ems_ttc_unknown,
    "Drugs given" : drugs_given}

    # hospital process
    reperfusion = case.exclude(reperfusionAttempt__isnull=True).exclude(reperfusionAttempt__exact=-1).count()
    hosp_ttc_indicated_done = case.filter(ttm__exact=3).count()
    hosp_ttc_indicated_not_done = case.filter(ttm__exact=4).count() # doesn't differentiate between hospital and ems process
    hosp_ttc_not_indicated = case.filter(ttm__exact=5).count() # doesn't differentiate between hospital and ems process
    hosp_ttc_unknown = case.filter(ttm__exact=-1).count() # doesn't differentiate between hospital and ems process
    organ_donation = case.filter(organDonation__exact=1).count()
    hosp_process_dict = {
        "Reperfusion attempted" : reperfusion, 
        "Hospital Targeted Temp Control - indicated, done" : hosp_ttc_indicated_done,
        "Hospital Targeted Temp Control - indicated, not done" : hosp_ttc_indicated_not_done,
        "Hospital Targeted Temp Control - not indicated, done" : hosp_ttc_not_indicated,
        "Hospital Targeted Temp Control - unknown" : hosp_ttc_unknown,
        "Organ donation" : organ_donation
        }


    # PATIENT OUTCOMES REPORTING POPULATION
    # resuscitation = case.filter(Q(bystanderResponse__exact=1) | Q(bystanderResponse__exact=2) | Q(bystanderAED__exact=2)) # shock not delivered counts as resuscitation or not?
    ems_witness_included = resuscitation.filter(Q(witnesses__exact=2) | Q(witnesses__exact=3))
    ems_witness_included_rosc = ems_witness_included.filter(rosc__exact=1).count()
    ems_witness_included_rosc_unknown = ems_witness_included.filter(rosc__exact=-1).count()
    ems_witness_included_surv = ems_witness_included.filter(survivalStatus__exact=1).count()
    ems_witness_included_surv_unknown = ems_witness_included.filter(survivalStatus__exact=-1).count()
    ems_witness_included_surv30d = ems_witness_included.filter(SurvivalDischarge30d__exact=1).count()
    ems_witness_included_surv30d_unknown = ems_witness_included.filter(SurvivalDischarge30d__exact=-1).count()
    ems_witness_included_cpcmrs = ems_witness_included.filter(Q(mrsDischarge__lte=3) | Q(cpcDischarge__lte=2)).count() 
    ems_witness_included_cpcmrs_unk = ems_witness_included.filter(mrsDischarge__lte=-1).filter(cpcDischarge__lte=-1).count()
    ems_witness_included_dict = {
        "EMS witness included - rosc" : ems_witness_included_rosc,
        "EMS witness included - rosc unknown" : ems_witness_included_rosc_unknown,
        "EMS witness included - survived event" : ems_witness_included_surv,
        "EMS witness included - survived event unknown" : ems_witness_included_surv_unknown,
        "EMS witness included - survival 30 days" : ems_witness_included_surv30d,
        "EMS witness included - survival 30 days unknown" : ems_witness_included_surv30d_unknown,
        "EMS witness included - CPC <= 2 or MRS <= 3 at discharge" : ems_witness_included_cpcmrs,
        "EMS witness included - CPC and MRS at discharge unknown" : ems_witness_included_cpcmrs_unk
    }

    ems_witness_excluded = resuscitation.exclude(witnesses__exact=2).exclude(witnesses__isnull=True)
    ems_shockbyst = ems_witness_excluded.filter(bystanderResponse__exact=0).filter(Q(firstMonitoredRhy__exact=1) | Q(firstMonitoredRhy__exact=2) | Q(firstMonitoredRhy__exact=7))
    ems_shockbystCPR = ems_witness_excluded.filter(Q(bystanderResponse__exact=1) | Q(bystanderResponse__exact=2)).filter(Q(firstMonitoredRhy__exact=1) | Q(firstMonitoredRhy__exact=2) | Q(firstMonitoredRhy__exact=7))
    ems_nonshock = ems_witness_excluded.filter(bystanderResponse__exact=0).filter(Q(firstMonitoredRhy__exact=3) | Q(firstMonitoredRhy__exact=4) | Q(firstMonitoredRhy__exact=6))

    rosc_shockbyst = ems_shockbyst.filter(rosc__exact=1).count() 
    roscunk_shockbyst= ems_shockbyst.filter(rosc__exact=-1).count() 
    surv_shockbyst = ems_shockbyst.filter(survivalStatus__exact=1).count() 
    survunk_shockbyst  = ems_shockbyst.filter(survivalStatus__exact=-1).count() 
    surv30d_shockbyst  = ems_shockbyst.filter(SurvivalDischarge30d__exact=1).count() 
    surv30dunk_shockbyst  = ems_shockbyst.filter(SurvivalDischarge30d__exact=-1).count() 
    neur_shockbyst  = ems_shockbyst.filter(Q(mrsDischarge__lte=3) | Q(cpcDischarge__lte=2)).count() 
    neurunk_shockbyst  = ems_shockbyst.filter(mrsDischarge__lte=-1).filter(cpcDischarge__lte=-1).count()


    rosc_shockbystCPR = ems_shockbystCPR.filter(rosc__exact=1).count() 
    roscunk_shockbystCPR= ems_shockbystCPR.filter(rosc__exact=-1).count() 
    surv_shockbystCPR = ems_shockbystCPR.filter(survivalStatus__exact=1).count() 
    survunk_shockbystCPR  = ems_shockbystCPR.filter(survivalStatus__exact=-1).count() 
    surv30d_shockbystCPR  = ems_shockbystCPR.filter(SurvivalDischarge30d__exact=1).count() 
    surv30dunk_shockbystCPR  = ems_shockbystCPR.filter(SurvivalDischarge30d__exact=-1).count() 
    neur_shockbystCPR  = ems_shockbystCPR.filter(Q(mrsDischarge__lte=3) | Q(cpcDischarge__lte=2)).count()
    neurunk_shockbystCPR = ems_shockbystCPR.filter(mrsDischarge__lte=-1).filter(cpcDischarge__lte=-1).count() 

    rosc_nonshock = ems_nonshock.filter(rosc__exact=1).count()
    roscunk_nonshock = ems_nonshock.filter(rosc__exact=-1).count() 
    surv_nonshock= ems_nonshock.filter(survivalStatus__exact=1).count() 
    survunk_nonshock  = ems_nonshock.filter(survivalStatus__exact=-1).count() 
    surv30d_nonshock  = ems_nonshock.filter(SurvivalDischarge30d__exact=1).count() 
    surv30dunk_nonshock  = ems_nonshock.filter(SurvivalDischarge30d__exact=-1).count() 
    neur_nonshock  = ems_nonshock.filter(Q(mrsDischarge__lte=3) | Q(cpcDischarge__lte=2)).count() 
    neurunk_nonshock = ems_nonshock.filter(mrsDischarge__lte=-1).filter(cpcDischarge__lte=-1).count() 

    ems_witness_excluded_dict = {
        "EMS witness excluded (shockable bystander witnessed) - rosc" : rosc_shockbyst,
        "EMS witness excluded (shockable bystander witnessed) - rosc unknown" : roscunk_shockbyst,
        "EMS witness excluded (shockable bystander witnessed) - survived event" : surv_shockbyst,
        "EMS witness excluded (shockable bystander witnessed) - survived event unknown" : survunk_shockbyst,
        "EMS witness excluded (shockable bystander witnessed) - survival 30 days" : surv30d_shockbyst,
        "EMS witness excluded (shockable bystander witnessed) - survival 30 days unknown" : surv30dunk_shockbyst,
        "EMS witness included (shockable bystander witnessed) - CPC <= 2 or MRS <= 3 at discharge" : neur_shockbyst,
        "EMS witness included (shockable bystander witnessed) - CPC and MRS at discharge unknown" : neurunk_shockbyst,

        "EMS witness excluded (shockable bystander CPR) - rosc" : rosc_shockbystCPR,
        "EMS witness excluded (shockable bystander CPR) - rosc unknown" : roscunk_shockbystCPR,
        "EMS witness excluded (shockable bystander CPR) - survived event" : surv_shockbystCPR,
        "EMS witness excluded (shockable bystander CPR) - survived event unknown" : survunk_shockbystCPR,
        "EMS witness excluded (shockable bystander CPR) - survival 30 days" : surv30d_shockbystCPR,
        "EMS witness excluded (shockable bystander CPR) - survival 30 days unknown" : surv30dunk_shockbystCPR,
        "EMS witness included (shockable bystander CPR) - CPC <= 2 or MRS <= 3 at discharge" : neur_shockbystCPR,
        "EMS witness included (shockable bystander CPR) - CPC and MRS at discharge unknown" : neurunk_shockbystCPR,

        "EMS witness excluded (non - shockable witnessed) - rosc" : rosc_nonshock,
        "EMS witness excluded (non - shockable witnessed) - rosc unknown" : roscunk_nonshock,
        "EMS witness excluded (non - shockable witnessed) - survived event" : surv_nonshock,
        "EMS witness excluded (non - shockable witnessed) - survived event unknown" : survunk_nonshock,
        "EMS witness excluded (non - shockable witnessed) - survival 30 days" : surv30d_nonshock,
        "EMS witness excluded (non - shockable witnessed) - survival 30 days unknown" : surv30dunk_nonshock,
        "EMS witness included (non - shockable witnessed) - CPC <= 2 or MRS <= 3 at discharge" : neur_nonshock,
        "EMS witness included (non - shockable witnessed) - CPC and MRS at discharge unknown" : neurunk_nonshock,      
    }

    dict_list = [dispatch_dict, general_dict, location_dict, patient_dict, witnessed_dict, bystander_response_dict, etiology_dict, 
    EMS_process_dict, hosp_process_dict, ems_witness_included_dict, ems_witness_excluded_dict]

    return dict_list

dict_list = queries(System.objects.all())

def data_summary(dict_list):
    "Returns a joined dictionary of the dict_list which is easy to turn into csv."
    summary_table = dict()
    for d in dict_list:
        for key in d:
            summary_table[key] = d[key]

    return summary_table

summary_table = data_summary(dict_list)


