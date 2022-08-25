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

    // else {
    //     document.getElementById('Pop').disabled = false;
    //     document.getElementById('Rock').disabled = false;
    //     document.getElementById('Jazz').disabled = false;
    //     document.getElementById('Classical').disabled = false;
    // }








window.onclick = function() {
    handleClick("id_ph", ph_ids);
    handleClick("id_lactate", lactate_ids);
    handleClick("id_ttmTemp", ttmTemp_ids);
    handleClick("id_shocks", shocks_ids);
    handleClick("id_targetBP", targetBP_ids);
}