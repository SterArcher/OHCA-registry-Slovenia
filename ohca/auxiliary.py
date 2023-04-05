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
    
    file = open('ohca/variables.json', encoding="utf-8")
    data = json.load(file) 
    values, titles, desc = dict(), dict(), dict()
    dates = []
    first_form, second_form, both_forms = [], [], []
    utstein, eureca, utstein_and_eureca = [], [], []
    names = [] # all variable names
    sections = dict() 
    counter = 0
    exceptions = ["BLOB", ">0", ">=0", "0-14", "1-5", "0-6", "hh:mm:ss", "date"]
    except_names = []
    not_dcz = []
    estimations = []
    for element in data["cases"]:
        counter += 1

        # first collect all variable names
        if element not in except_names: #True: #element not in except_names
            if "shown" in data["cases"][element]:
                if data["cases"][element]["shown"] == True:
                    names.append(element)
            else: # če shown ni notri pol je shown
                names.append(element)

    for element in names:
        # second organize them by sections
        if "section" in data["cases"][element]:
            section = data["cases"][element]["section"]
            if section in sections:
                sections[section].append(element)
            else:
                sections[section] = [element]

        # third remember their titles which will be the questions in the form
        if "title" in data["cases"][element]:
            titles[element] = "<b>" + data["cases"][element]["title"] + "</b>"
            if 'description' in data["cases"][element]:
                desc[element] = data["cases"][element]["description"]
        
        if "dcz" in data["cases"][element]:
            not_dcz.append(element)
        
        # fourth remember possible values
        value_list = []
        if "values" in data["cases"][element] and data["cases"][element]["values"] != "BLOB":
            value_dict = data["cases"][element]["values"]

            if "date" in value_dict:
                dates.append(element)

            if len(set(value_dict).intersection(set(exceptions))) == 0: 
                for val in value_dict:
                    # print(val)
                    if val != "null" and val!= "-1":
                        # print((int(val), value_dict[val]))
                        if (val == "0" and value_dict[val] == "Ne") or (val == "1" and value_dict[val] == "Da"):
                            value_list = [(int(val), value_dict[val])] + value_list
                        else:
                            value_list.append((int(val), value_dict[val])) 
                if element not in ["estimatedAge", "estimatedAgeBystander", "emergencyTransport", "cardiacArrest"] and "estimated" not in element or element == "estimatedAgeBystander": #, "estimatedCAtimestamp"]:
                    value_list.append((-1, "Neznano/ni podatka"))
                    value_list.append((-2, "Ni zabeleženo/ni zavedeno"))

        if len(value_list) > 0:
            values[element] = value_list

        # fifth remember if it belongs to first or second form
        if "form" in data["cases"][element]:
            elt = data["cases"][element]["form"] 
            if elt == "d1" or elt == "d1&d30":
                first_form.append(element)
                both_forms.append(element)
            if elt == "d30" or elt == "d1&d30":
                second_form.append(element)
                both_forms.append(element)
            # elif elt == "d1&d30":
            #     both_forms.append(element)

            # TODO
            # if "from" in data["cases"][element]:
            #     if data["cases"][element]["from"] == "Utstein2015":
            #         utstein.append(element)
            #     elif data["cases"][element]["from"] == "EuReCa3":
            #         eureca.append(element)
            #     elif data["cases"][element]["from"] == "EuReCa3 & Utstein2015":
            #         utstein_and_eureca.append(element)

    timestamps = sections["timeline"]
    
    for timestamp in timestamps:
        if "dcz" in data["cases"][timestamp]:
            not_dcz.append(timestamp)
    return (values, titles, desc, first_form, second_form, both_forms, dates, names, timestamps, not_dcz)

(values, titles, descriptions, first_form, second_form, both_forms, dates, names, timestamps, not_dcz) = read_values()

