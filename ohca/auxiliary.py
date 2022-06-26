import json

  
def read_values():

    """Reads values from the json file and remembers titles, values, descriptions"""
    
    file = open('OHCA-registry-Slovenia/ohca/utstein.values.en.json', encoding="utf-8")
    data = json.load(file)
    values = dict()
    titles = dict()
    names = []
    desc = dict()
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
            # if ">0" not in value_dict and ">=0" not in value_dict and "0-14" not in value_dict: # te morš podat kot cifre ne kot radiobutton
            if len(set(value_dict).intersection(set(exceptions))) == 0:
                for val in value_dict:
                    # print(val)
                    if val != "null":
                        value_list.append((int(val), value_dict[val])) 
        if len(value_list) > 0:
            values[element] = value_list
    # print(names)
    # print(desc)
    return (values, titles, desc, names)
  
    # file.close()

(values, titles, desc, names) = read_values()