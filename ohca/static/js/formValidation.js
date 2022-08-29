// ======== handle fields with input and radio options ===========

function disableField(fieldID) {
    document.getElementById(fieldID).disabled = true;
}

function enableField(fieldID) {
    document.getElementById(fieldID).disabled = false;
}

function uncheckField(fieldID) {
    document.getElementById(fieldID).checked = false;
}

function handleTab(field_id, ids, event) {
    var field = document.getElementById(field_id);
    if (event.key == "Tab" && field.value == "") {
        for (let i = 0; i < ids.length; i++) {
            field.addEventListener('change', function() { enableField(ids[i]) });
        }
    }
    if (event.key == "Tab" && field.value != "") {
        for (let i = 0; i < ids.length; i++) {
            console.log("here!")
            field.addEventListener('change', function() { uncheckField(ids[i]) });
            field.addEventListener('change', function() { disableField(ids[i]) });
        }
    }
}

function handleClick(field_id, ids) {
    var field = document.getElementById(field_id);
    if (field.value == "") {
        for (let i = 0; i < ids.length; i++) {
            document.getElementById(ids[i]).disabled = false; 
        }
    }
    if (field.value != "") {
        for (let i = 0; i < ids.length; i++) {
            document.getElementById(ids[i]).checked = false;
            document.getElementById(ids[i]).disabled = true; 
        }
    }
}

const ph = document.getElementById("id_ph")
const ph_ids = ["id_adPh_0", "id_adPh_1"]

ph.addEventListener("keydown", function(event) {
    handleTab("id_ph", ph_ids, event)
    }
)
// document.getElementById("id_adPh_0").addEventListener("change", function() { disableField("id_ph") })


const lactate = document.getElementById("id_lactate")
const lactate_ids = ["id_adLactate_0", "id_adLactate_1"]

lactate.addEventListener("keydown", function(event) {
    handleTab("id_lactate", lactate_ids, event)
    }
)

const ttmTemp = document.getElementById("id_ttmTemp")
const ttmTemp_ids = ["id_adTtmTemp_0", "id_adTtmTemp_1"]

ttmTemp.addEventListener("keydown", function(event) {
    handleTab("id_ttmTemp", ttmTemp_ids, event)
    }
)

const shocks = document.getElementById("id_shocks")
const shocks_ids = ["id_adShocks_0", "id_adShocks_1"]

shocks.addEventListener("keydown", function(event) {
    handleTab("id_shocks", shocks_ids, event)
    }
)

const targetBP = document.getElementById("id_targetBP")
const targetBP_ids = ["id_adTargetBP_0", "id_adTargetBP_1", "id_adTargetBP_2"]

targetBP.addEventListener("keydown", function(event) {
    handleTab("id_targetBP", targetBP_ids, event)
    }
)

const hospitalName = document.getElementById("id_hospitalName")
const hospitalName_ids = ["id_adHospitalName_0", "id_adHospitalName_1"]

targetBP.addEventListener("keydown", function(event) {
    handleTab("id_hospitalName", hospitalName_ids, event)
    }
)

const bystanderAge = document.getElementById("id_ageBystander")
const bystanderAge_ids = ["id_adBystAge_0", "id_adBystAge_1"]

targetBP.addEventListener("keydown", function(event) {
    handleTab("id_estimatedAgeBystander", hospitalName_ids, event)
    }
)

window.onclick = function() {
    handleClick("id_ph", ph_ids);
    handleClick("id_lactate", lactate_ids);
    handleClick("id_ttmTemp", ttmTemp_ids);
    handleClick("id_shocks", shocks_ids);
    handleClick("id_targetBP", targetBP_ids);
    handleClick("id_hospitalName", hospitalName_ids);
    handleClick("id_ageBystander", bystanderAge_ids);
} 


// ========================= handle fields with text and radio buttons ================

const textFields = ["id_ph", "id_lactate", "id_shocks", "id_targetBP", "id_ttmTemp", "id_hospitalName", "id_ageBystander"]
const radioFields = [["id_adPh_0", "id_adPh_1"], ["id_adLactate_0", "id_adLactate_1"], ["id_adShocks_0", "id_adShocks_1"], ["id_adTargetBP_0", "id_adTargetBP_1"], ["id_adTtmTemp_0", "id_adTtmTemp_1"], ["id_adHospitalName_0", "id_adHospitalName_1"], ["id_adBystAge_0", "id_adBystAge_1"]]

// make fields required
window.onload = function require() {
    checkFormReload();
    for (let i = 0; i < textFields.length; i++) {
        document.getElementById(textFields[i]).setAttribute("required", "")
    }
    handleDoubleField();

    document.getElementById("id_dateOfBirth").setAttribute("required", "");
    document.getElementById("div_id_allDrugs").setAttribute("required", "");
    handleBirthdateField();

    document.getElementById("id_allDrugs_0").setAttribute("required", "");
    document.getElementById("id_airway_0").setAttribute("required", "");
    document.getElementById("id_ecgopt_0").setAttribute("required", "");
    handleMultipleselect();
}

function handleDoubleField() {
    // console.log("handledoublefield")
    var fields = textFields;
    var radioChoices = radioFields; //[["id_adPh_0", "id_adPh_1"], ["id_adLactate_0", "id_adLactate_1"]];
    for (let j = 0; j < radioChoices.length; j++) {
        var bool = true;
        for (let i = 0; i < radioChoices[j].length; i++) {
            if (document.getElementById(radioChoices[j][i]).checked) {
                bool = false;
            }
        }
        // console.log(bool);
        // console.log(fields[j].value)
        if ((fields[j].value == "" || fields.value == null) && bool) {
            document.getElementById(fields[j]).setAttribute("required", "");
        }
        else {
            document.getElementById(fields[j]).removeAttribute("required");
        }

    }
}

for (let i = 0; i < textFields.length; i++) {
    document.getElementById(textFields[i]).addEventListener("change", handleDoubleField);
}
for (let i = 0; i < radioFields.length; i++) {
    for (let j = 0; j < radioFields[i].length; j++) {
        document.getElementById(radioFields[i][j]).addEventListener("change", handleDoubleField)
    }
}

// ============================ handle date of birth and estimated age ==============================

function handleBirthdateField() {
    console.log("handledoublefield")
    var field1 = document.getElementById("id_dateOfBirth");
    var field2 = document.getElementById("id_estimatedAge");
    // var bool = true;
    console.log(field2.value)
    console.log(field1.value)

    if ((field1.value == "" || field1.value == null) && (field2.value == "" || field2.value == null)){
        field1.setAttribute("required", "");
    }
    else {
        field1.removeAttribute("required");
    }
}

document.getElementById("id_dateOfBirth").addEventListener("change", handleBirthdateField)
document.getElementById("id_estimatedAge").addEventListener("change", handleBirthdateField)

// ========================= handle multiple select fields ==================

const ecg = document.querySelectorAll('input[name="ecgopt');
const drugs = document.querySelectorAll('input[name="allDrugs');
const airway = document.querySelectorAll('input[name="airway');

// =====================ecg========================================
function check1() {
    for (let i = 0; i < ecg.length; i++) {
        if (ecg[i].checked && ecg[i].value == "-1") { 
            for (let j = 0; j < ecg.length; j++) {
                if (ecg[j].value != "-1") {
                    ecg[j].checked = false;}}}}}
function check2() {
    for (let i = 0; i < ecg.length; i++) {
        if (ecg[i].checked && ecg[i].value == "-9999") {
            for (let j = 0; j < ecg.length; j++) {
                if (ecg[j].value != "-9999") {
                    ecg[j].checked = false;}}
            ecg[i].checked = true;}}}
function check3() {
    var bool1 = false;
    for (let i = 0; i < ecg.length; i++) {
            if (ecg[i].checked && ecg[i].value != "0" && ecg[i].value != "-9999" && ecg[i].value != "-1") {
                bool1 = true;}}
    if (bool1) {
        document.getElementById("id_ecgopt_27").checked = false;
        document.getElementById("id_ecgopt_28").checked = false;}}

document.getElementById("id_ecgopt_27").addEventListener("change", check1)
document.getElementById("id_ecgopt_28").addEventListener("change", check2)
document.getElementById("id_ecgopt_27").addEventListener("change", handleMultipleselect)
document.getElementById("id_ecgopt_28").addEventListener("change", handleMultipleselect)
for (let k = 0; k < 27; k++) {
    ecg[k].addEventListener("change", check3);
    ecg[k].addEventListener("change", handleMultipleselect);
}
// =====================drugs========================================
function checkDrugs1() {
    for (let i = 0; i < drugs.length; i++) {
        if (drugs[i].checked && drugs[i].value == "-1") { 
            for (let j = 0; j < drugs.length; j++) {
                if (drugs[j].value != "-1") {
                    drugs[j].checked = false;}}}}}
function checkDrugs2() {
    for (let i = 0; i < drugs.length; i++) {
        if (drugs[i].checked && drugs[i].value == "-9999") {
            for (let j = 0; j < drugs.length; j++) {
                if (drugs[j].value != "-9999") {
                    drugs[j].checked = false;}}
            drugs[i].checked = true;}}}
function checkDrugs3() {
    for (let i = 0; i < drugs.length; i++) {
        if (drugs[i].checked && drugs[i].value == "0") {
            for (let j = 0; j < drugs.length; j++) {
                if (drugs[j].value != "0") {
                    drugs[j].checked = false;}}
            drugs[i].checked = true;}}}
function checkDrugs4() {
    var bool1 = false;
    for (let i = 0; i < drugs.length; i++) {
            if (drugs[i].checked && drugs[i].value != "0" && drugs[i].value != "-9999" && drugs[i].value != "-1") {
                bool1 = true;}}
    if (bool1) {
        document.getElementById("id_allDrugs_3").checked = false;
        document.getElementById("id_allDrugs_4").checked = false;
        document.getElementById("id_allDrugs_5").checked = false;}}

document.getElementById("id_allDrugs_3").addEventListener("change", checkDrugs3)
document.getElementById("id_allDrugs_4").addEventListener("change", checkDrugs1)
document.getElementById("id_allDrugs_5").addEventListener("change", checkDrugs2)
document.getElementById("id_allDrugs_3").addEventListener("change", handleMultipleselect)
document.getElementById("id_allDrugs_4").addEventListener("change", handleMultipleselect)
document.getElementById("id_allDrugs_5").addEventListener("change", handleMultipleselect)

for (let k = 0; k < 3; k++) {
    drugs[k].addEventListener("change", checkDrugs4);
    drugs[k].addEventListener("change", handleMultipleselect);
}
// =====================airway========================================
function checkairway1() {
    for (let i = 0; i < airway.length; i++) {
        if (airway[i].checked && airway[i].value == "-1") { 
            for (let j = 0; j < airway.length; j++) {
                if (airway[j].value != "-1") {
                    airway[j].checked = false;}}}}}
function checkairway2() {
    for (let i = 0; i < airway.length; i++) {
        if (airway[i].checked && airway[i].value == "-9999") {
            for (let j = 0; j < airway.length; j++) {
                if (airway[j].value != "-9999") {
                    airway[j].checked = false;}}
            airway[i].checked = true;}}}
function checkairway3() {
    for (let i = 0; i < airway.length; i++) {
        if (airway[i].checked && airway[i].value == "0") {
            for (let j = 0; j < airway.length; j++) {
                if (airway[j].value != "0") {
                    airway[j].checked = false;}}
            airway[i].checked = true;}}}
function checkairway4() {
    var bool1 = false;
    for (let i = 0; i < airway.length; i++) {
            if (airway[i].checked && airway[i].value != "0" && airway[i].value != "-9999" && airway[i].value != "-1") {
                bool1 = true;}}
    if (bool1) {
        document.getElementById("id_airway_4").checked = false;
        document.getElementById("id_airway_5").checked = false;
        document.getElementById("id_airway_6").checked = false;}}

document.getElementById("id_airway_4").addEventListener("change", checkairway3)
document.getElementById("id_airway_5").addEventListener("change", checkairway1)
document.getElementById("id_airway_6").addEventListener("change", checkairway2)
document.getElementById("id_airway_4").addEventListener("change", handleMultipleselect)
document.getElementById("id_airway_5").addEventListener("change", handleMultipleselect)
document.getElementById("id_airway_6").addEventListener("change", handleMultipleselect)

for (let k = 0; k < 4; k++) {
    airway[k].addEventListener("change", checkairway4);
    airway[k].addEventListener("change", handleMultipleselect);
}
//=======================================================================
function handleMultipleselect() {
    var bool1 = false;
    var bool2 = false;
    for (let i = 0; i < ecg.length; i++) {
        if (ecg[i].checked && ecg[i].value != "0" && ecg[i].value != "-9999" && ecg[i].value != "-1") {
            bool1 = true;}
        else if (ecg[i].checked || ecg[i].value == "0" || ecg[i].value == "-9999" || ecg[i].value == "-1") {
            bool2 = true;}}
    if (bool1 || bool2) {
        document.getElementById("id_ecgopt_0").removeAttribute("required");}
    var bool1 = false;
    var bool2 = false;
    for (let i = 0; i < drugs.length; i++) {
        if (drugs[i].checked && drugs[i].value != "0" && drugs[i].value != "-9999" && drugs[i].value != "-1") {
            bool1 = true;}
        else if (drugs[i].checked || drugs[i].value == "0" || drugs[i].value == "-9999" || drugs[i].value == "-1") {
            bool2 = true;}}
    if (bool1 || bool2) {
        document.getElementById("id_allDrugs_0").removeAttribute("required");}
    var bool1 = false;
    var bool2 = false;
    for (let i = 0; i < airway.length; i++) {
        if (airway[i].checked && airway[i].value != "0" && airway[i].value != "-9999" && airway[i].value != "-1") {
            bool1 = true;}
        else if (airway[i].checked || airway[i].value == "0" || airway[i].value == "-9999" || airway[i].value == "-1") {
            bool2 = true;}}
    if (bool1 || bool2) {
        document.getElementById("id_airway_0").removeAttribute("required");}}

function otherEcg() {
    if (document.getElementById("id_ecgopt_26").checked) {
        document.getElementById("id_ecgResult").setAttribute("required", "");
    }
    else {
        document.getElementById("id_ecgResult").removeAttribute("required");
    }
}
document.getElementById("id_ecgopt_26").addEventListener("change", otherEcg)


// ========================= handle bystander age - estimated or not =====================


// ============================ if sentences for timestamps! ===========================================
