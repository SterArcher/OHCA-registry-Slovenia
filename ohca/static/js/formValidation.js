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

// const ph = document.getElementById("id_ph")
// const ph_ids = ["id_adPh_0", "id_adPh_1"]

// ph.addEventListener("keydown", function(event) {
//     handleTab("id_ph", ph_ids, event)
//     }
// )
// // document.getElementById("id_adPh_0").addEventListener("change", function() { disableField("id_ph") })


// const lactate = document.getElementById("id_lactate")
// const lactate_ids = ["id_adLactate_0", "id_adLactate_1"]

// lactate.addEventListener("keydown", function(event) {
//     handleTab("id_lactate", lactate_ids, event)
//     }
// )

// const ttmTemp = document.getElementById("id_ttmTemp")
// const ttmTemp_ids = ["id_adTtmTemp_0", "id_adTtmTemp_1"]

// ttmTemp.addEventListener("keydown", function(event) {
//     handleTab("id_ttmTemp", ttmTemp_ids, event)
//     }
// )

const shocks = document.getElementById("id_shocks")
const shocks_ids = ["id_adShocks_0", "id_adShocks_1"]

shocks.addEventListener("keydown", function(event) {
    handleTab("id_shocks", shocks_ids, event)
    }
)

// const targetBP = document.getElementById("id_targetBP")
// const targetBP_ids = ["id_adTargetBP_0", "id_adTargetBP_1", "id_adTargetBP_2"]

// targetBP.addEventListener("keydown", function(event) {
//     handleTab("id_targetBP", targetBP_ids, event)
//     }
// )

const hospitalName = document.getElementById("id_hospitalName")
const hospitalName_ids = ["id_adHospitalName_0", "id_adHospitalName_1"]

hospitalName.addEventListener("keydown", function(event) {
    handleTab("id_hospitalName", hospitalName_ids, event)
    }
)

const bystanderAge = document.getElementById("id_ageBystander")
const bystanderAge_ids = ["id_adBystAge_0", "id_adBystAge_1"]

bystanderAge.addEventListener("keydown", function(event) {
    handleTab("id_estimatedAgeBystander", bystanderAge_ids, event)
    }
)

window.onclick = function() {
    // handleClick("id_ph", ph_ids);
    // handleClick("id_lactate", lactate_ids);
    // handleClick("id_ttmTemp", ttmTemp_ids);
    handleClick("id_shocks", shocks_ids);
    // handleClick("id_targetBP", targetBP_ids);
    handleClick("id_hospitalName", hospitalName_ids);
    handleClick("id_ageBystander", bystanderAge_ids);
} 


// ========================= handle fields with text and radio buttons ================

const textFields = ["id_shocks"] //, "id_hospitalName", "id_ageBystander"]
const radioFields = [["id_adShocks_0", "id_adShocks_1"],]//, ["id_adHospitalName_0", "id_adHospitalName_1"], ["id_adBystAge_0", "id_adBystAge_1"]]



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
// const drugs = document.querySelectorAll('input[name="allDrugs');
// const airway = document.querySelectorAll('input[name="airway');

// =====================ecg========================================
function check1() {
    for (let i = 0; i < ecg.length; i++) {
        if (ecg[i].checked && ecg[i].value == "-1") { 
            for (let j = 0; j < ecg.length; j++) {
                if (ecg[j].value != "-1") {
                    ecg[j].checked = false;}}}}}
function check2() {
    for (let i = 0; i < ecg.length; i++) {
        if (ecg[i].checked && ecg[i].value == "-2") {
            for (let j = 0; j < ecg.length; j++) {
                if (ecg[j].value != "-2") {
                    ecg[j].checked = false;}}
            ecg[i].checked = true;}}}
function check3() {
    var bool1 = false;
    for (let i = 0; i < ecg.length; i++) {
            if (ecg[i].checked && ecg[i].value != "0" && ecg[i].value != "-2" && ecg[i].value != "-1") {
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
// // =====================drugs========================================
// function checkDrugs1() {
//     for (let i = 0; i < drugs.length; i++) {
//         if (drugs[i].checked && drugs[i].value == "-1") { 
//             for (let j = 0; j < drugs.length; j++) {
//                 if (drugs[j].value != "-1") {
//                     drugs[j].checked = false;}}}}}
// function checkDrugs2() {
//     for (let i = 0; i < drugs.length; i++) {
//         if (drugs[i].checked && drugs[i].value == "-2") {
//             for (let j = 0; j < drugs.length; j++) {
//                 if (drugs[j].value != "-2") {
//                     drugs[j].checked = false;}}
//             drugs[i].checked = true;}}}
// function checkDrugs3() {
//     for (let i = 0; i < drugs.length; i++) {
//         if (drugs[i].checked && drugs[i].value == "0") {
//             for (let j = 0; j < drugs.length; j++) {
//                 if (drugs[j].value != "0") {
//                     drugs[j].checked = false;}}
//             drugs[i].checked = true;}}}
// function checkDrugs4() {
//     var bool1 = false;
//     for (let i = 0; i < drugs.length; i++) {
//             if (drugs[i].checked && drugs[i].value != "0" && drugs[i].value != "-2" && drugs[i].value != "-1") {
//                 bool1 = true;}}
//     if (bool1) {
//         document.getElementById("id_allDrugs_3").checked = false;
//         document.getElementById("id_allDrugs_4").checked = false;
//         document.getElementById("id_allDrugs_5").checked = false;}}

// document.getElementById("id_allDrugs_3").addEventListener("change", checkDrugs3)
// document.getElementById("id_allDrugs_4").addEventListener("change", checkDrugs1)
// document.getElementById("id_allDrugs_5").addEventListener("change", checkDrugs2)
// document.getElementById("id_allDrugs_3").addEventListener("change", handleMultipleselect)
// document.getElementById("id_allDrugs_4").addEventListener("change", handleMultipleselect)
// document.getElementById("id_allDrugs_5").addEventListener("change", handleMultipleselect)

// for (let k = 0; k < 3; k++) {
//     drugs[k].addEventListener("change", checkDrugs4);
//     drugs[k].addEventListener("change", handleMultipleselect);
// }
// // =====================airway========================================
// function checkairway1() {
//     for (let i = 0; i < airway.length; i++) {
//         if (airway[i].checked && airway[i].value == "-1") { 
//             for (let j = 0; j < airway.length; j++) {
//                 if (airway[j].value != "-1") {
//                     airway[j].checked = false;}}}}}
// function checkairway2() {
//     for (let i = 0; i < airway.length; i++) {
//         if (airway[i].checked && airway[i].value == "-2") {
//             for (let j = 0; j < airway.length; j++) {
//                 if (airway[j].value != "-2") {
//                     airway[j].checked = false;}}
//             airway[i].checked = true;}}}
// function checkairway3() {
//     for (let i = 0; i < airway.length; i++) {
//         if (airway[i].checked && airway[i].value == "0") {
//             for (let j = 0; j < airway.length; j++) {
//                 if (airway[j].value != "0") {
//                     airway[j].checked = false;}}
//             airway[i].checked = true;}}}
// function checkairway4() {
//     var bool1 = false;
//     for (let i = 0; i < airway.length; i++) {
//             if (airway[i].checked && airway[i].value != "0" && airway[i].value != "-2" && airway[i].value != "-1") {
//                 bool1 = true;}}
//     if (bool1) {
//         document.getElementById("id_airway_4").checked = false;
//         document.getElementById("id_airway_5").checked = false;
//         document.getElementById("id_airway_6").checked = false;}}

// document.getElementById("id_airway_4").addEventListener("change", checkairway3)
// document.getElementById("id_airway_5").addEventListener("change", checkairway1)
// document.getElementById("id_airway_6").addEventListener("change", checkairway2)
// document.getElementById("id_airway_4").addEventListener("change", handleMultipleselect)
// document.getElementById("id_airway_5").addEventListener("change", handleMultipleselect)
// document.getElementById("id_airway_6").addEventListener("change", handleMultipleselect)

// for (let k = 0; k < 4; k++) {
//     airway[k].addEventListener("change", checkairway4);
//     airway[k].addEventListener("change", handleMultipleselect);
// }
//=======================================================================
function handleMultipleselect() {
    console.log("multiple select")
    var bool1 = false;
    var bool2 = false;
    for (let i = 0; i < ecg.length; i++) {
        if (ecg[i].checked && ecg[i].value != "0" && ecg[i].value != "-2" && ecg[i].value != "-1") {
            bool1 = true;}
        else if (ecg[i].checked && (ecg[i].value == "0" || ecg[i].value == "-2" || ecg[i].value == "-1")) {
            bool2 = true;}}
    console.log(bool1)
    console.log(bool2)
    if (bool1 || bool2) {
        document.getElementById("id_ecgopt_0").removeAttribute("required");}
    else {
        document.getElementById("id_ecgopt_0").setAttribute("required", "");
    }
    // var bool1 = false;
    // var bool2 = false;
    // for (let i = 0; i < drugs.length; i++) {
    //     if (drugs[i].checked && drugs[i].value != "0" && drugs[i].value != "-2" && drugs[i].value != "-1") {
    //         bool1 = true;}
    //     else if (drugs[i].checked && (drugs[i].value == "0" || drugs[i].value == "-2" || drugs[i].value == "-1")) {
    //         bool2 = true;}}
    // if (bool1 || bool2) {
    //     document.getElementById("id_allDrugs_0").removeAttribute("required");}
    // var bool1 = false;
    // var bool2 = false;
    // for (let i = 0; i < airway.length; i++) {
    //     if (airway[i].checked && airway[i].value != "0" && airway[i].value != "-2" && airway[i].value != "-1") {
    //         bool1 = true;}
    //     else if (airway[i].checked && (airway[i].value == "0" || airway[i].value == "-2" || airway[i].value == "-1")) {
    //         bool2 = true;}}
    // if (bool1 || bool2) {
    //     document.getElementById("id_airway_0").removeAttribute("required");}
    }

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

// dependent fields
// timestamp
// estimation


// Čas, ko je dispečer/NMP dal navodila za oživljanje po telefonu
function timestampTCPR() {
    // "dispProvidedCPRinst"
    if (document.getElementById("id_dispProvidedCPRinst_0")) {
    if (document.getElementById("id_dispProvidedCPRinst_0").checked) {
        document.getElementById("id_timestampTCPR_0").setAttribute("required", "");
        document.getElementById("id_timestampTCPR_1").setAttribute("required", "");
        document.getElementById("id_estimatedTimestampTCPR_0").setAttribute("required", "");
        document.getElementById("id_estimatedTimestampTCPR_1").setAttribute("required", "");
    }
    else {
        document.getElementById("id_timestampTCPR_0").removeAttribute("required");
        document.getElementById("id_timestampTCPR_1").removeAttribute("required");
        document.getElementById("id_estimatedTimestampTCPR_0").removeAttribute("required");
        document.getElementById("id_estimatedTimestampTCPR_1").removeAttribute("required");
    
    }}
if (document.getElementById("id_dispProvidedCPRinst_0")) {
    document.getElementById("id_dispProvidedCPRinst_0").addEventListener("change", timestampTCPR)
    document.getElementById("id_dispProvidedCPRinst_1").addEventListener("change", timestampTCPR)
    document.getElementById("id_dispProvidedCPRinst_2").addEventListener("change", timestampTCPR)
    document.getElementById("id_dispProvidedCPRinst_3").addEventListener("change", timestampTCPR)
}}

// Čas, ko je pričel očividec z oživljanjem (TPO)
function bystanderCPR() {
    if (document.getElementById("id_cPRbystander3Timestamp_0")) {
        var const1 = document.getElementById("id_bystanderCPR_1").checked || document.getElementById("id_bystanderCPR_2").checked || document.getElementById("id_bystanderCPR_3").checked
        var const2 = document.getElementById("id_bystanderResponse_1").checked || document.getElementById("id_bystanderResponse_2").checked
        // console.log(const1)
        // console.log(const2)
        // console.log(document.getElementById("id_persCPRstart_0").checked)
        if (document.getElementById("id_persCPRstart_0").checked || const1 || const2) {
            document.getElementById("id_cPRbystander3Timestamp_0").setAttribute("required", "");
            document.getElementById("id_cPRbystander3Timestamp_1").setAttribute("required", "");
            document.getElementById("id_estimatedCPRbystander_0").setAttribute("required", "");
            document.getElementById("id_estimatedCPRbystander_1").setAttribute("required", "");
        }
        else {
            document.getElementById("id_cPRbystander3Timestamp_0").removeAttribute("required");
            document.getElementById("id_cPRbystander3Timestamp_1").removeAttribute("required");
            document.getElementById("id_estimatedCPRbystander_0").removeAttribute("required");
            document.getElementById("id_estimatedCPRbystander_1").removeAttribute("required");
        }}}
const bystCPR1 = document.querySelectorAll('input[name="bystanderCPR"]')
const bystCPR2 = document.querySelectorAll('input[name="bystanderResponse"]')
const bystCPR3 = document.querySelectorAll('input[name="persCPRstart"]')
for (let i = 0; i < bystCPR1.length; i++) {bystCPR1[i].addEventListener("change", bystanderCPR)}
for (let i = 0; i < bystCPR2.length; i++) {bystCPR2[i].addEventListener("change", bystanderCPR)}
for (let i = 0; i < bystCPR3.length; i++) {bystCPR3[i].addEventListener("change", bystanderCPR)}

// Čas, ko je pričela oseba, ki jo je DCZ/NMP poslal na kraj zastoja (npr. prvi posredovalec) z oživljanjem (TPO)
function helperCPR() {
    if (document.getElementById("id_cPRhelper3Timestamp_0")) {
        var const1 = document.getElementById("id_helperCPR_1").checked || document.getElementById("id_helperCPR_2").checked || document.getElementById("id_helperCPR_3").checked 
        if (document.getElementById("id_persCPRstart_1").checked || const1) {
            document.getElementById("id_cPRhelper3Timestamp_0").setAttribute("required", "");
            document.getElementById("id_cPRhelper3Timestamp_1").setAttribute("required", "");
            document.getElementById("id_estimatedCPRhelperTimestamp_0").setAttribute("required", "");
            document.getElementById("id_estimatedCPRhelperTimestamp_1").setAttribute("required", "");
        }
        else {
            document.getElementById("id_cPRhelper3Timestamp_0").removeAttribute("required");
            document.getElementById("id_cPRhelper3Timestamp_1").removeAttribute("required");
            document.getElementById("id_estimatedCPRhelperTimestamp_0").removeAttribute("required");
            document.getElementById("id_estimatedCPRhelperTimestamp_1").removeAttribute("required");  
        }}}
const helperCPR1 = document.querySelectorAll('input[name="helperCPR"]')
const helperCPR2 = document.querySelectorAll('input[name="persCPRstart"]')
for (let i = 0; i < helperCPR1.length; i++) {helperCPR1[i].addEventListener("change", helperCPR)}
for (let i = 0; i < helperCPR2.length; i++) {helperCPR2[i].addEventListener("change", helperCPR)}

// Čas, ko je pričela služba NMP z oživljanjem
function CPREMS() {
    if (document.getElementById("id_cPREMS3Timestamp_0")) {
        if (document.getElementById("id_cprEms_0").checked) {
            document.getElementById("id_cPREMS3Timestamp_0").setAttribute("required", "");
            document.getElementById("id_cPREMS3Timestamp_1").setAttribute("required", "");
            document.getElementById("id_estimatedCPREMStimestamp_0").setAttribute("required", "");
            document.getElementById("id_estimatedCPREMStimestamp_1").setAttribute("required", "");
        }
        else {
            document.getElementById("id_cPREMS3Timestamp_0").removeAttribute("required");
            document.getElementById("id_cPREMS3Timestamp_1").removeAttribute("required");
            document.getElementById("id_estimatedCPREMStimestamp_0").removeAttribute("required");
            document.getElementById("id_estimatedCPREMStimestamp_1").removeAttribute("required");
        
        }
    }
}
const cprems1 = document.querySelectorAll('input[name="cprEms"]')
for (let i = 0; i < cprems1.length; i++) {cprems1[i].addEventListener("change", CPREMS)}

// Čas prve defibrilacije
function defibTime() {
    if (document.getElementById("id_defibTimestamp_0")) {
        if (document.getElementById("id_AEDshock_0").checked) {
            document.getElementById("id_defibTimestamp_0").setAttribute("required", "");
            document.getElementById("id_defibTimestamp_1").setAttribute("required", "");
            document.getElementById("id_estimatedDefibTimestamp_0").setAttribute("required", "");
            document.getElementById("id_estimatedDefibTimestamp_1").setAttribute("required", "");
        }
        else {
            document.getElementById("id_defibTimestamp_0").removeAttribute("required");
            document.getElementById("id_defibTimestamp_1").removeAttribute("required");
            document.getElementById("id_estimatedDefibTimestamp_0").removeAttribute("required");
            document.getElementById("id_estimatedDefibTimestamp_1").removeAttribute("required");
        }}}
const defib = document.querySelectorAll('input[name="AEDshock"]')
for (let i = 0; i < defib.length; i++) {defib[i].addEventListener("change", defibTime)}


// function drugTimings() {
//     if (document.getElementById("id_drugTimingsTimestamp_0")) {
//         console.log(document.getElementById("id_allDrugs_0").checked || document.getElementById("id_allDrugs_1").checked || document.getElementById("id_allDrugs_2").checked)
//         if (document.getElementById("id_allDrugs_0").checked || document.getElementById("id_allDrugs_1").checked || document.getElementById("id_allDrugs_2").checked) {
//             document.getElementById("id_drugTimingsTimestamp_0").setAttribute("required", "");
//             document.getElementById("id_drugTimingsTimestamp_1").setAttribute("required", "");
//             document.getElementById("id_estimatedDrugTimings_0").setAttribute("required", "");
//             document.getElementById("id_estimatedDrugTimings_1").setAttribute("required", "");
//         }
//         else {
//             document.getElementById("id_drugTimingsTimestamp_0").removeAttribute("required");
//             document.getElementById("id_drugTimingsTimestamp_1").removeAttribute("required");
//             document.getElementById("id_estimatedDrugTimings_0").removeAttribute("required");
//             document.getElementById("id_estimatedDrugTimings_1").removeAttribute("required");
//         }}}
// const drugTimings1 = document.querySelectorAll('input[name="allDrugs"]')
// for (let i = 0; i < drugTimings1.length; i++) {drugTimings1[i].addEventListener("change", drugTimings)}


function rosc() {
    if (document.getElementById("id_roscTimestamp_0")) {
        if (document.getElementById("id_rosc_0").checked) {
            document.getElementById("id_roscTimestamp_0").setAttribute("required", "");
            document.getElementById("id_roscTimestamp_1").setAttribute("required", "");
            document.getElementById("id_estimatedRoscTimestamp_0").setAttribute("required", "");
            document.getElementById("id_estimatedRoscTimestamp_1").setAttribute("required", "");
        }
        else {
            document.getElementById("id_roscTimestamp_0").removeAttribute("required");
            document.getElementById("id_roscTimestamp_1").removeAttribute("required");
            document.getElementById("id_estimatedRoscTimestamp_0").removeAttribute("required");
            document.getElementById("id_estimatedRoscTimestamp_1").removeAttribute("required");
        }}}
const rosc1 = document.querySelectorAll('input[name="rosc"]')
for (let i = 0; i < rosc1.length; i++) {rosc1[i].addEventListener("change", rosc)}

// function cprEnd() {
//     if (document.getElementById("id_endCPR4Timestamp_0")) {
//         if (document.getElementById("id_diedOnField_0").checked) {
//             document.getElementById("id_endCPR4Timestamp_0").setAttribute("required", "");
//             document.getElementById("id_endCPR4Timestamp_1").setAttribute("required", "");
//             document.getElementById("id_estimatedEndCPRtimestamp_1").setAttribute("required", "");
//             document.getElementById("id_estimatedEndCPRtimestamp_1").setAttribute("required", "");
//         }
//         else {
//             document.getElementById("id_endCPR4Timestamp_0").removeAttribute("required");
//             document.getElementById("id_endCPR4Timestamp_1").removeAttribute("required");
//             document.getElementById("id_estimatedEndCPRtimestamp_0").removeAttribute("required");
//             document.getElementById("id_estimatedEndCPRtimestamp_1").removeAttribute("required");
//         }}}
// const cprend1 = document.querySelectorAll('input[name="diedOnField"]')
// for (let i = 0; i < cprend1.length; i++) {cprend1[i].addEventListener("change", cprEnd)}

function handleNoCPR() {
    const fields = document.querySelectorAll('input[name="noCPR"]');
    if (document.getElementById("id_cprEms_1").checked) {
        console.log("tukaj")
        for (let i = 0; i < fields.length; i++) { fields[i].setAttribute("required", "")}
    }
    else {
        for (let i = 0; i < fields.length; i++) { fields[i].removeAttribute("required")}
    }}
const fields2 = document.querySelectorAll('input[name="cprEms"]');
for (let i = 0; i < fields2.length; i++) { fields2[i].addEventListener("change", handleNoCPR)}


window.onload = function require() {
    checkFormReload();
    for (let i = 0; i < textFields.length; i++) {
        document.getElementById(textFields[i]).setAttribute("required", "")
    }
    handleDoubleField();

    document.getElementById("id_dateOfBirth").setAttribute("required", "");
    // document.getElementById("div_id_allDrugs").setAttribute("required", "");
    handleBirthdateField();

    // document.getElementById("id_allDrugs_0").setAttribute("required", "");
    // document.getElementById("id_airway_0").setAttribute("required", "");
    document.getElementById("id_ecgopt_0").setAttribute("required", "");
    handleMultipleselect();
    handleNoCPR();

    timestampTCPR();
    bystanderCPR();
    helperCPR();
    CPREMS();
    defibTime();
    // drugTimings();
    rosc();
    // cprEnd();
}