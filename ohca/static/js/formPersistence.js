const formFields = document.querySelectorAll('input:not([type="hidden"],[type="submit"],[type="radio"],[type="checkbox"])');
const formChoices = document.querySelectorAll('input[type="radio"],input[type="checkbox"]');

function saveFormToCookie() {
    console.log("HEREE")
    var system = document.getElementById("id_systemID");
    var sysval = system.options[system.selectedIndex].text;
    var local = document.getElementById("id_localID");
    var locval = local.options[local.selectedIndex].text;
    sessionStorage.setItem("id_systemID", sysval);
    sessionStorage.setItem("id_localID", locval);
    sessionStorage.setItem("id_systemID", document.getElementById("id_systemID").value);
    sessionStorage.setItem("id_localID", document.getElementById("id_localID").value);
    for (let i = 0; i < formFields.length; i++) {
        sessionStorage.setItem(formFields[i].id, formFields[i].value);
    }
    for (let i = 0; i < formChoices.length; i++) {
        sessionStorage.setItem(formChoices[i].id, formChoices[i].checked);
    }

}

function loadFormFromCookie() {
    document.getElementById("id_systemID").value = sessionStorage.getItem("id_systemID");
    document.getElementById("id_localID").value = sessionStorage.getItem("id_localID");
    for (let i = 0; i < formFields.length; i++) {
        if (sessionStorage.getItem(formFields[i].id)) {
            formFields[i].value = sessionStorage.getItem(formFields[i].id);
        }
    }
    for (let i = 0; i < formChoices.length; i++) {
        if (sessionStorage.getItem(formChoices[i].id) == "true") {
            formChoices[i].checked = true;
        }
    }
}

function clearAllFields() {
    for (let i = 0; i < formFields.length; i++) {
        formFields[i].value = "";
    }
    for (let i = 0; i < formChoices.length; i++) {
        formFields[i].checked = false;
    }
}

function clearCookies() {
    sessionStorage.clear();
}

function checkFormReload() {
    if (document.getElementsByClassName("alert-danger").length >= 1) {
        console.log("right here");
        loadFormFromCookie();
        clearCookies();
    } else if (document.getElementsByClassName("alert-success") >= 1) {
        console.log("right here 2");
        clearCookies();
    } else {
        console.log("right here 3");
        clearCookies();
    }
}