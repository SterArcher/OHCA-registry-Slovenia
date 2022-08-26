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




// if (document.getElementsByClassName("alert-danger").length >= 1) {
// console.log(document.getElementsByClassName("alert-danger").outerText)
// }

// handle question about AED and first monitored rhytm

// bystanderAED and firstMonitoredRhy

var aed1 = document.getElementById("id_bystanderAED_0");
var aed2 = document.getElementById("id_bystanderAED_1");
var aed3 = document.getElementById("id_bystanderAED_2");

aed1.addEventListener("change", function() {
    if (aed1.checked) {
        document.getElementById('id_firstMonitoredRhy_0').disabled = true;
        // document.getElementById('id_firstMonitoredRhy_1').disabled = true;
        document.getElementById('id_firstMonitoredRhy_1').checked = true;
        document.getElementById('id_firstMonitoredRhy_1').disabled = false;
        document.getElementById('id_firstMonitoredRhy_2').disabled = true;
        document.getElementById('id_firstMonitoredRhy_3').disabled = true;
        document.getElementById('id_firstMonitoredRhy_4').disabled = true;
        document.getElementById('id_firstMonitoredRhy_5').disabled = true;
        document.getElementById('id_firstMonitoredRhy_6').disabled = true;
        document.getElementById('id_firstMonitoredRhy_7').disabled = true;
        document.getElementById('id_firstMonitoredRhy_8').disabled = true;
    }
})

aed2.addEventListener("change", function() {
    if (aed2.checked) {
        document.getElementById('id_firstMonitoredRhy_1').disabled = true;
        // document.getElementById('id_firstMonitoredRhy_1').disabled = true;
        document.getElementById('id_firstMonitoredRhy_0').checked = true;
        document.getElementById('id_firstMonitoredRhy_0').disabled = false;
        document.getElementById('id_firstMonitoredRhy_2').disabled = true;
        document.getElementById('id_firstMonitoredRhy_3').disabled = true;
        document.getElementById('id_firstMonitoredRhy_4').disabled = true;
        document.getElementById('id_firstMonitoredRhy_5').disabled = true;
        document.getElementById('id_firstMonitoredRhy_6').disabled = true;
        document.getElementById('id_firstMonitoredRhy_7').disabled = true;
        document.getElementById('id_firstMonitoredRhy_8').disabled = true;
    }
})

aed3.addEventListener("change", function() {
    if (aed3.checked) {
        document.getElementById('id_firstMonitoredRhy_0').checked = false;
        document.getElementById('id_firstMonitoredRhy_1').checked = false;
        document.getElementById('id_firstMonitoredRhy_1').disabled = true;
        // document.getElementById('id_firstMonitoredRhy_1').disabled = true;
        document.getElementById('id_firstMonitoredRhy_0').disabled = true;
        document.getElementById('id_firstMonitoredRhy_2').disabled = false;
        document.getElementById('id_firstMonitoredRhy_3').disabled = false;
        document.getElementById('id_firstMonitoredRhy_4').disabled = false;
        document.getElementById('id_firstMonitoredRhy_5').disabled = false;
        document.getElementById('id_firstMonitoredRhy_6').disabled = false;
        document.getElementById('id_firstMonitoredRhy_7').disabled = false;
        document.getElementById('id_firstMonitoredRhy_8').disabled = false;
    }
}
)

document.getElementById("id_bystanderAED_3").addEventListener("change", function() {
    if (document.getElementById("id_bystanderAED_3").checked) {
        document.getElementById('id_firstMonitoredRhy_0').checked = false;
        document.getElementById('id_firstMonitoredRhy_1').checked = false;
        document.getElementById('id_firstMonitoredRhy_1').disabled = false;
        document.getElementById('id_firstMonitoredRhy_0').disabled = false;
        document.getElementById('id_firstMonitoredRhy_2').disabled = false;
        document.getElementById('id_firstMonitoredRhy_3').disabled = false;
        document.getElementById('id_firstMonitoredRhy_4').disabled = false;
        document.getElementById('id_firstMonitoredRhy_5').disabled = false;
        document.getElementById('id_firstMonitoredRhy_6').disabled = false;
        document.getElementById('id_firstMonitoredRhy_7').disabled = false;
        document.getElementById('id_firstMonitoredRhy_8').disabled = false;
    }
})

document.getElementById("id_bystanderAED_4").addEventListener("change", function() {
    if (document.getElementById("id_bystanderAED_3").checked) {
        document.getElementById('id_firstMonitoredRhy_0').checked = false;
        document.getElementById('id_firstMonitoredRhy_1').checked = false;
        document.getElementById('id_firstMonitoredRhy_1').disabled = false;
        document.getElementById('id_firstMonitoredRhy_0').disabled = false;
        document.getElementById('id_firstMonitoredRhy_2').disabled = false;
        document.getElementById('id_firstMonitoredRhy_3').disabled = false;
        document.getElementById('id_firstMonitoredRhy_4').disabled = false;
        document.getElementById('id_firstMonitoredRhy_5').disabled = false;
        document.getElementById('id_firstMonitoredRhy_6').disabled = false;
        document.getElementById('id_firstMonitoredRhy_7').disabled = false;
        document.getElementById('id_firstMonitoredRhy_8').disabled = false;
    }
})


window.onclick = function() {
    handleClick("id_ph", ph_ids);
    handleClick("id_lactate", lactate_ids);
    handleClick("id_ttmTemp", ttmTemp_ids);
    handleClick("id_shocks", shocks_ids);
    handleClick("id_targetBP", targetBP_ids);
}


//------------------ DISPLAY/HIDE/REQUIRED INPUT FIELDS

// cprEMS - noCPR
const noCPRblock = document.getElementById("div_id_noCPR");
function handleNoCPR() {
    const noCPRfields = ["id_noCPR_0", "id_noCPR_1", "id_noCPR_2", "id_noCPR_3", "id_noCPR_4", "id_noCPR_5", "id_noCPR_6", "id_noCPR_7"];
    if(document.getElementById('id_cprEms_0').checked){
        noCPRblock.style.display = 'block';
        for(let i = 0; i < noCPRfields.length; i++){
            document.getElementById(noCPRfields[i]).setAttribute("required", "");
        }
    }
    else if (document.getElementById('id_cprEms_1').checked || document.getElementById('id_cprEms_2').checked || document.getElementById('id_cprEms_3').checked){
        noCPRblock.style.display = 'none';
        for(let i = 0; i < noCPRfields.length; i++){
            document.getElementById(noCPRfields[i]).removeAttribute("required");
        }
    }
    else{
        noCPRblock.style.display = 'block'; 
    }

}

const cprRadioButtons = document.querySelectorAll('input[name="cprEms"]');
cprRadioButtons.forEach(radio => {
  radio.addEventListener('click', handleNoCPR);
});


// reaWitnesses - bystanderCPR
const reaWitnessesBlock = document.getElementById("div_id_bystanderCPR");
function handleWitnesses() {
    const bystanderCPRfields = ["id_bystanderCPR_0", "id_bystanderCPR_1", "id_bystanderCPR_2", "id_bystanderCPR_3", "id_bystanderCPR_4", "id_bystanderCPR_5"];
    if(document.getElementById('id_reaWitnesses_0').checked){
        reaWitnessesBlock.style.display = 'none';
        for (const field in bystanderCPRfields){
            document.getElementById(field).removeAttribute("required");
        }
    }
    else if (document.getElementById('id_reaWitnesses_1').checked || document.getElementById('id_reaWitnesses_2').checked || document.getElementById('id_reaWitnesses_3').checked || document.getElementById('id_reaWitnesses_4').checked || document.getElementById('id_reaWitnesses_5').checked){
        reaWitnessesBlock.style.display = 'block';
        for (const field in bystanderCPRfields){
            document.getElementById(field).setAttribute("required", "");
        }
    }
    else{
        reaWitnessesBlock.style.display = 'block'; 
    }
}

const witnessesRadioButtons = document.querySelectorAll('input[name="reaWitnesses"]');
witnessesRadioButtons.forEach(radio => {
  radio.addEventListener('click', handleWitnesses);
});


// transportToHospital - hospitalName
const hospitalNameBlock = document.getElementById("div_id_hospitalName");
function handleHospitalName(){
    if(document.getElementById('id_transportToHospital_0').checked){
        hospitalNameBlock.style.display = 'none';
        document.getElementById("id_hospitalName").removeAttribute("required");
    }
    else if (document.getElementById('id_transportToHospital_1').checked || document.getElementById('id_transportToHospital_2').checked  || document.getElementById('id_transportToHospital_3').checked ){
        hospitalNameBlock.style.display = 'block';
        document.getElementById("id_hospitalName").setAttribute("required", "");
    }
    else{
        hospitalNameBlock.style.display = 'block';
    }
}

const transportToHospitalRadioButtons = document.querySelectorAll('input[name="transportToHospital"]');
transportToHospitalRadioButtons.forEach(radio => {
    radio.addEventListener('click', handleHospitalName);
})


const estimatedAgeBlock = document.getElementById("div_id_estimatedAge");
function handleEstimatedAge(){
    if(document.getElementById('id_dateOfBirth').value == ""){
        estimatedAgeBlock.style.display = 'block';
        document.getElementById("id_estimatedAge").removeAttribute("required");
    }
    else{
        estimatedAgeBlock.style.display = 'none';
        
        document.getElementById("id_estimatedAge").setAttribute("required", "");
    }
}

const dateOfBirthInput = document.querySelectorAll('input[name="dateOfBirth"]');
dateOfBirthInput.forEach(radio => {
    radio.addEventListener('click', handleEstimatedAge);
})


// // persCPRstart + cPRbystander3Timestamp + estimatedCPRbystander
const persCPRstart = document.getElementById("div_id_persCPRstart");

const bystander = document.getElementById("id_persCPRstart_0");
const bystanderDispatch = document.getElementById("id_persCPRstart_1");
const ems = document.getElementById("id_persCPRstart_2");

function handlePersCPR() {
    console.log("tukej")
    if (bystander.checked) {
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
    }

    if (bystanderDispatch.checked) {
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
    }
    if (ems.checked) {
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

bystander.addEventListener("change", handlePersCPR)
bystanderDispatch.addEventListener("change", handlePersCPR)
ems.addEventListener("change", handlePersCPR)


// const persCPRstartInput = document.querySelectorAll('input[name="persCPRstart"]');
// persCPRstartInput.forEach(radio => {
//     radio.addEventListener('click', handlePersCPRstart);
// })


