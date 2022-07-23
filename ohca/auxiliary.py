import json

  
def read_values():
    """Reads the json file and returns:
    - titles 
    - values (only for questions with radio buttons)
    - descriptions (as help text) 
    - first_form (names of fields belonging to first form)
    - second_form (names of fields belonging to second form)
    - utstein (names of fields belonging to utstein)
    - eureca (names of fields belonging to eureca)
    - timestamps (all fields that are filled as timestamps)"""
    
    file = open('ohca/utstein.values.en.json', encoding="utf-8")
    data = json.load(file)
    values, titles, desc = dict(), dict(), dict()
    timestamps = []
    first_form, second_form = [], []
    utstein, eureca, utstein_and_eureca = [], [], []
    names = [] # all variable names
    exceptions = ["BLOB", ">0", ">=0", "0-14", "1-5", "0-6"]
    for element in data["cases"]:
        names.append(element)
        if "title" in data["cases"][element]:
            titles[element] = data["cases"][element]["title"]
            if 'description' in data["cases"][element]:
                desc[element] = data["cases"][element]["description"]
        value_list = []
        if "values" in data["cases"][element] and data["cases"][element]["values"] != "BLOB":
            value_dict = data["cases"][element]["values"]
            # print(value_dict)
            if "hh:mm:ss" in value_dict:
                timestamps.append(element)

            if len(set(value_dict).intersection(set(exceptions))) == 0: 
                for val in value_dict:
                    # print(val)
                    if val != "null" and val!= "hh:mm:ss":
                        value_list.append((int(val), value_dict[val])) 
        if len(value_list) > 0:
            values[element] = value_list

        if "form" in data["cases"][element]:
            if data["cases"][element]["form"] == "day1":
                first_form.append(element)
            elif data["cases"][element]["form"] == "day30":
                second_form.append(element)

        if "from" in data["cases"][element]:
            if data["cases"][element]["from"] == "Utstein2015":
                utstein.append(element)
            elif data["cases"][element]["from"] == "EuReCa3":
                eureca.append(element)
            elif data["cases"][element]["from"] == "EuReCa3 & Utstein2015":
                utstein_and_eureca.append(element)

    return (values, titles, desc, first_form, second_form, timestamps, utstein, eureca, utstein_and_eureca)
  
    # file.close()

(values, titles, descriptions, first_form, second_form, timestamps, utstein, eureca, utstein_and_eureca) = read_values()