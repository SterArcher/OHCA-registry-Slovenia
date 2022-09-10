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


// ===========================================


function handleTreatmentWithdrawn() {
    var val = document.getElementById("id_treatmentWithdrawn_0").checked;
    // var death2 = document.getElementById("id_survival30d_1");
    console.log(val)
    if (val) {

        document.getElementById("id_treatmentWithdrawnTimestamp_0").setAttribute("required", "");
        document.getElementById("id_treatmentWithdrawnTimestamp_1").setAttribute("required", "");
    }
    else {
        document.getElementById("id_treatmentWithdrawnTimestamp_0").removeAttribute("required");
        document.getElementById("id_treatmentWithdrawnTimestamp_1").removeAttribute("required");
    }}
document.getElementById("id_treatmentWithdrawn_0").addEventListener("change", handleTreatmentWithdrawn)
document.getElementById("id_treatmentWithdrawn_1").addEventListener("change", handleTreatmentWithdrawn)
document.getElementById("id_treatmentWithdrawn_2").addEventListener("change", handleTreatmentWithdrawn)
document.getElementById("id_treatmentWithdrawn_3").addEventListener("change", handleTreatmentWithdrawn)

function handleTreatmentWithdrawn1() {
    if (document.getElementById("id_treatmentWithdrawnTimestamp_1").value != null && document.getElementById("id_treatmentWithdrawnTimestamp_1").value != "") {
        document.getElementById("id_adWithdraw_0").checked = false;
        document.getElementById("id_adWithdraw_1").checked = false;
        document.getElementById("id_adWithdraw_0").removeAttribute("required")
        document.getElementById("id_adWithdraw_1").removeAttribute("required")
    }
}
function handleTreatmentWithdrawn2() {
    if (document.getElementById("id_adWithdraw_0").checked || document.getElementById("id_adWithdraw_0").checked) {
        document.getElementById("id_treatmentWithdrawnTimestamp_1").value = null;
        document.getElementById("id_treatmentWithdrawnTimestamp_0").value = null;
        document.getElementById("id_treatmentWithdrawnTimestamp_1").removeAttribute("required")
        document.getElementById("id_treatmentWithdrawnTimestamp_0").removeAttribute("required")
    }
}
document.getElementById("id_treatmentWithdrawnTimestamp_1").addEventListener("change", handleTreatmentWithdrawn1)
document.getElementById("id_treatmentWithdrawnTimestamp_0").addEventListener("change", handleTreatmentWithdrawn1)
document.getElementById("id_adWithdraw_0").addEventListener("change", handleTreatmentWithdrawn2)
document.getElementById("id_adWithdraw_1").addEventListener("change", handleTreatmentWithdrawn2)

function handleDiscDate() {
    var val = document.getElementById("id_survivalDischarge_0").checked;
    console.log(val)
    if (val) {
        document.getElementById("id_discDate").setAttribute("required", "");
    }
    else {
        document.getElementById("id_discDate").removeAttribute("required");
    }}
document.getElementById("id_survivalDischarge_0").addEventListener("change", handleDiscDate)
document.getElementById("id_survivalDischarge_1").addEventListener("change", handleDiscDate)
document.getElementById("id_survivalDischarge_2").addEventListener("change", handleDiscDate)
document.getElementById("id_survivalDischarge_3").addEventListener("change", handleDiscDate)

// other neuroprognostic tests
function tests() {
    if (document.getElementById("id_otherNeuroprognosticTests_0").checked) {
        document.getElementById("id_neuroprognosticTests").setAttribute("required", "");
    }
    else {
        document.getElementById("id_neuroprognosticTests").removeAttribute("required");
    }}
document.getElementById("id_otherNeuroprognosticTests_0").addEventListener("change", tests)
document.getElementById("id_otherNeuroprognosticTests_1").addEventListener("change", tests)
document.getElementById("id_otherNeuroprognosticTests_2").addEventListener("change", tests)
document.getElementById("id_otherNeuroprognosticTests_3").addEventListener("change", tests)
    

window.onload = function require() {
    checkFormReload();

    checkFormReload();
        for (let i = 0; i < textFields.length; i++) {
            document.getElementById(textFields[i]).setAttribute("required", "")
        }
    handleDoubleField();
    handleTreatmentWithdrawn1();
    handleTreatmentWithdrawn2();
    handleTreatmentWithdrawn();
    handleDiscDate();
    tests();

    document.getElementById("id_allDrugs_0").setAttribute("required", "");
    document.getElementById("id_airway_0").setAttribute("required", "");

    handleMultipleselect();
    drugTimings();

    document.getElementById("id_dateOfBirth").setAttribute("required", "");
    // document.getElementById("div_id_allDrugs").setAttribute("required", "");
    handleBirthdateField();
}


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



const targetBP = document.getElementById("id_targetBP")
const targetBP_ids = ["id_adTargetBP_0", "id_adTargetBP_1", "id_adTargetBP_2"]

targetBP.addEventListener("keydown", function(event) {
    handleTab("id_targetBP", targetBP_ids, event)
    }
)



window.onclick = function() {
    handleClick("id_ph", ph_ids);
    handleClick("id_lactate", lactate_ids);
    handleClick("id_ttmTemp", ttmTemp_ids);
    handleClick("id_targetBP", targetBP_ids);

} 

// ========================= handle fields with text and radio buttons ================

const textFields = ["id_ph", "id_lactate", "id_targetBP", "id_ttmTemp"] //, "id_hospitalName", "id_ageBystander"]
const radioFields = [["id_adPh_0", "id_adPh_1"], ["id_adLactate_0", "id_adLactate_1"], ["id_adTargetBP_0", "id_adTargetBP_1", "id_adTargetBP_2"], ["id_adTtmTemp_0", "id_adTtmTemp_1"]]//, ["id_adHospitalName_0", "id_adHospitalName_1"], ["id_adBystAge_0", "id_adBystAge_1"]]



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



const drugs = document.querySelectorAll('input[name="allDrugs');
const airway = document.querySelectorAll('input[name="airway');

// =====================drugs========================================
function checkDrugs1() {
    for (let i = 0; i < drugs.length; i++) {
        if (drugs[i].checked && drugs[i].value == "-1") { 
            for (let j = 0; j < drugs.length; j++) {
                if (drugs[j].value != "-1") {
                    drugs[j].checked = false;}}}}}
function checkDrugs2() {
    for (let i = 0; i < drugs.length; i++) {
        if (drugs[i].checked && drugs[i].value == "-2") {
            for (let j = 0; j < drugs.length; j++) {
                if (drugs[j].value != "-2") {
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
            if (drugs[i].checked && drugs[i].value != "0" && drugs[i].value != "-2" && drugs[i].value != "-1") {
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
        if (airway[i].checked && airway[i].value == "-2") {
            for (let j = 0; j < airway.length; j++) {
                if (airway[j].value != "-2") {
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
            if (airway[i].checked && airway[i].value != "0" && airway[i].value != "-2" && airway[i].value != "-1") {
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


function handleMultipleselect() {
    console.log("multiple select")
    // var bool1 = false;
    // var bool2 = false;
    // for (let i = 0; i < ecg.length; i++) {
    //     if (ecg[i].checked && ecg[i].value != "0" && ecg[i].value != "-2" && ecg[i].value != "-1") {
    //         bool1 = true;}
    //     else if (ecg[i].checked && (ecg[i].value == "0" || ecg[i].value == "-2" || ecg[i].value == "-1")) {
    //         bool2 = true;}}
    // console.log(bool1)
    // console.log(bool2)
    // if (bool1 || bool2) {
    //     document.getElementById("id_ecgopt_0").removeAttribute("required");}
    // else {
    //     document.getElementById("id_ecgopt_0").setAttribute("required", "");
    // }
    var bool1 = false;
    var bool2 = false;
    for (let i = 0; i < drugs.length; i++) {
        if (drugs[i].checked && drugs[i].value != "0" && drugs[i].value != "-2" && drugs[i].value != "-1") {
            bool1 = true;}
        else if (drugs[i].checked && (drugs[i].value == "0" || drugs[i].value == "-2" || drugs[i].value == "-1")) {
            bool2 = true;}}
    if (bool1 || bool2) {
        document.getElementById("id_allDrugs_0").removeAttribute("required");}
    var bool1 = false;
    var bool2 = false;
    for (let i = 0; i < airway.length; i++) {
        if (airway[i].checked && airway[i].value != "0" && airway[i].value != "-2" && airway[i].value != "-1") {
            bool1 = true;}
        else if (airway[i].checked && (airway[i].value == "0" || airway[i].value == "-2" || airway[i].value == "-1")) {
            bool2 = true;}}
    if (bool1 || bool2) {
        document.getElementById("id_airway_0").removeAttribute("required");}
    }

    function drugTimings() {
        if (document.getElementById("id_drugTimingsTimestamp_0")) {
            console.log(document.getElementById("id_allDrugs_0").checked || document.getElementById("id_allDrugs_1").checked || document.getElementById("id_allDrugs_2").checked)
            if (document.getElementById("id_allDrugs_0").checked || document.getElementById("id_allDrugs_1").checked || document.getElementById("id_allDrugs_2").checked) {
                document.getElementById("id_drugTimingsTimestamp_0").setAttribute("required", "");
                document.getElementById("id_drugTimingsTimestamp_1").setAttribute("required", "");
                document.getElementById("id_estimatedDrugTimings_0").setAttribute("required", "");
                document.getElementById("id_estimatedDrugTimings_1").setAttribute("required", "");
            }
            else {
                document.getElementById("id_drugTimingsTimestamp_0").removeAttribute("required");
                document.getElementById("id_drugTimingsTimestamp_1").removeAttribute("required");
                document.getElementById("id_estimatedDrugTimings_0").removeAttribute("required");
                document.getElementById("id_estimatedDrugTimings_1").removeAttribute("required");
            }}}
    const drugTimings1 = document.querySelectorAll('input[name="allDrugs"]')
    for (let i = 0; i < drugTimings1.length; i++) {drugTimings1[i].addEventListener("change", drugTimings)}
    
    // window.onload = function require() {
    //     checkFormReload();
    //     for (let i = 0; i < textFields.length; i++) {
    //         document.getElementById(textFields[i]).setAttribute("required", "")
    //     }
    //     handleDoubleField();
    
    //     document.getElementById("id_dateOfBirth").setAttribute("required", "");
    //     document.getElementById("div_id_allDrugs").setAttribute("required", "");
    //     handleBirthdateField();
    
    //     document.getElementById("id_allDrugs_0").setAttribute("required", "");
    //     document.getElementById("id_airway_0").setAttribute("required", "");
    //     // document.getElementById("id_ecgopt_0").setAttribute("required", "");
    //     handleMultipleselect();
    //     // handleNoCPR();
    
    //     // timestampTCPR();
    //     // bystanderCPR();
    //     // helperCPR();
    //     // CPREMS();
    //     // defibTime();
    //     drugTimings();
    //     // rosc();
    //     // cprEnd();
    // }