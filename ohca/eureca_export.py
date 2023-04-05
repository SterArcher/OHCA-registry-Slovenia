import json
from ohca.models import CaseReport, Locale, System

import datetime
from datetime import datetime

# DONE should export excel not csv
# TODO double check the fields and values in eureca_variables.json
# DONE our timestamps include the date and time zone - but it has to be just hh:mm:ss
# DONE municipality names dont contain čžš 
# DONE reaPop has to be added manually for all municipalities from Locale db
# TODO update population values in the db!
# DONE check if the right times are exported or if time has to be 'changed' (based on timezone)
# DONE variables in our db are -2, -1, 0, 1, 2.. in eureca they are 00, 01, 02, 99, 11...

# first define the columns from our db swe will need for eureca based on the eureca-template
eureca_columns = {
    "systemID" : "Zdravstveni dom",
    "numID" : "NumID",
    "reaLand" : "ReaLand *",
    "reaRegion" : "ReaRegion *",
    "reaPop" : "ReaPop *", 
    "reaConf" : "ReaConf - A1 *",
    "CPRdone" : "CPRdone - A2 *",
    "persCPRstart" : "PersCPRstart  - A3",
    "cprEms" : "CprEms - A4 *",
    "cPREMS3Timestamp" : "CPREMS3Time - A5",
    "noCPR" : "NoCPR - A6 *",
    "numID" : "PatID *", # patID  
    "age" : "PatAge - B1 *", # anonimnost?
    "gender" : "PaGender - B2 *",
    "reaYr" : "ReaYr - B3 *",
    "reaMo" : "ReaMo - B3 *",
    "reaDay" : "ReaDay - B3",
    "reaTimestamp" : "ReaTime - B4 *", # #reaTime
    "callTimestamp" : "time112 - B5 *", # time112
    "responseTimestamp" : "timeScene - B6 *", # timeScene
    "reaCause" : "ReaCause - C1 *",
    "pathogenesis" : "ReaC2014 - C2", 
    "reaLocation" : "ReaLocat - C3 *",
    "cprEms" : "TeleCPR - D1 *", 
    "cPREMS3Timestamp" : "timeTCPR - D2", 
    "reaWitnesses" : "ReaWitnes - D3 *",
    "bystanderCPR" : "BystanCPR - D4 *", 
    "gbystnader" : "Gbystander - D6",
    "ageBystander" : "AgeBystander - D5",
    "cPRbystander3Timestamp" : "CPRbystander3Time - D7",
    "helperCPR" : "HelperCPR - E1",
    "helperWho" : "HelperWho - E2",
    "cPRhelper3Timestamp" : "CPRhelper3Time - E3",
    "iniRythm" : "IniRythm - F1 *", 
    "AEDconn" : "AEDConn - F2 *",
    "AEDshock" : "AEDShock - F3 *",
    "defibTimestamp" : "Def1Time - F4 *",
    "defiOrig" : "DefiOrig - F5 *",
    "rosc" : "ROSC - G1 *", 
    "roscTimestamp" : "timeROSC - G2 *",
    "endCPR4Timestamp" : "EndCPR4Time - G4",
    "diedOnField" : "DeadSc - G3 *",
    "leftScene5Timestamp" : "LeftScene5Time - G5",
    "hospitalArrival6Timestamp" : "HospitalArrival6Time - G6",
    "hospArri" : "HospArri - G7 *",
    "dischMonth" : "DischMonth - H1 *",
    "dischDay" : "DischDay - H1 *",
    "survivalDischarge" : "HospDisc - H2",
    "survival30d" : "surv30d - H3",
}

eureca_db_columns = list(eureca_columns.keys())
eureca_template_columns = list(eureca_columns.values())

# create a list of all cases, each list element (case) is a dict with col names as keys and respective values as dict values 
all_cases = CaseReport.objects.all().values(
    *eureca_columns
    )

# for reaPop variable we need to know the population of every location
locales = Locale.objects.all().values("friendlyName", "population")
population = dict() # contains population # for each locale
for loc in locales:
    population[loc["friendlyName"]] = loc["population"]

def convert_time(timestamp):
    """Takes timestamp in the form 2022-month-day hh:mm:ss+00:00:00 (UTC timezone) and returns hh:mm:ss in the Europe/Ljubljana timezone.
    .astimezone() already considers the daylight savings time"""
    slo_time = format(timestamp.astimezone())
    slo_time = (slo_time.split(" "))[1]
    if "+" in slo_time:
        slo_time = slo_time[:slo_time.find("+")]
    return slo_time

# open the file eureca_variables which will tell us how to convert the values of the variables
file = open('ohca/eureca_variables.json')
eureca_variables = json.load(file)

# create header for the exported file
header = eureca_template_columns


# loop through the cases and "fix" the elements
for case in all_cases:
    for variable in case:
        if type(case[variable]) == datetime:
            case[variable] = convert_time(case[variable])
        elif variable in eureca_variables and case[variable] != None: # if it's in the json file it has to be converted
            # convert the variables based on the eureca_variables.json
            case[variable] = eureca_variables[variable]["encoding"][str(case[variable])]
        if case["reaRegion"] != None:
            case["reaPop"] = population[case["reaRegion"]]

