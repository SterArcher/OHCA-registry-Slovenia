# from covering.csv prepare the necessary csv files for the population.py script

# we only run this at the beginnig

# we need two files:
# 1) columns: obcina, ZD, povrsina, st_preb (municipality, hospital, area, population)
# 2) columns: ZD, st, povrsina (hospital, population, area)
#       - sum of population over all covered municipalities

# useful : https://pxweb.stat.si/SiStatData/pxweb/en/Data/-/05C4003S.px/table/tableViewLayout2/ 

import csv 

municipalities = dict() # key: municipatily, value: (population, area, hospital)
hosp_pop, hosp_area = dict(), dict()
nmp_pop, nmp_area = dict(), dict()

def up(dict, key, val):
    "Updates dict with key and value"
    if key in dict:
        dict[key] += val
    else:
        dict[key] = val
    return dict
    
# create necessary dictionaries
with open("OHCA-registry-Slovenia\data\Serving_population\covering.csv", encoding="utf-8") as file:
    lines = csv.reader(file)
    counter = 0
    for line in lines:
        # print(line)
        if counter != 0: # skip the header
            
            municipality = line[1]

            if "*" in municipality:
                municipality = municipality.replace("*", "") # special case

            num_people = int(line[2])
            area = round(float(line[6]), 2)
            hosp = line[4]
            nmp = line[5]
            
            # for every municipality we save: number of people, area, which hospital covers it
            municipalities[municipality] = (num_people, area, hosp)

            hosp_pop = up(hosp_pop, hosp, num_people)
            hosp_area = up(hosp_area, hosp, area)

            nmp_pop = up(nmp_pop, nmp, num_people)
            nmp_area = up(nmp_area, nmp, area)

        counter += 1

def generate_files():

    with open("OHCA-registry-Slovenia\data\population\population.csv", "w", newline="", encoding="utf-8") as new_file:
        header = ["obcina", "enota_nmp", "povrsina", "st_preb"]
        csvwriter = csv.writer(new_file,)
        csvwriter.writerow(header)
        for key in municipalities:
            if "*" in key:
                key = key.replace("*", "")
            csvwriter.writerow([key, 
                                municipalities[key][2], # hospital
                                municipalities[key][1], # area
                                municipalities[key][0]])# population

    with open("OHCA-registry-Slovenia\data\population\hospitals.csv", "w", newline="", encoding="utf-8") as new_file:
        header = ["zd", "st", "povrsina"]
        csvwriter = csv.writer(new_file,)
        csvwriter.writerow(header)
        for key in hosp_pop:
            csvwriter.writerow([key,             
                                hosp_pop[key],      # population covered by that hospital
                                round(hosp_area[key], 2)])    # area covered by that hospital


# with open("OHCA-registry-Slovenia\data\Serving_population\enote_nmp.csv", "w", encoding="utf-8") as new_file:
#     top = ["zd", "st", "povrsina"]
#     csvwriter = csv.writer(new_file,)
#     csvwriter.writerow(top)
#     for key in nmp_pop:
#         csvwriter.writerow([key, nmp_pop[key], nmp_area[key]])

generate_files()



