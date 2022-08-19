const formFields = document.querySelectorAll('input:not([type="hidden"],[type="submit"],[type="radio"],[type="checkbox"])');
const formChoices = document.querySelectorAll('input[type="radio"],input[type="checkbox"]');

function saveFormToCookie() {
    for (let i = 0; i < formFields.length; i++) {
        sessionStorage.setItem(formFields[i].id, formFields[i].value);
    }
    for (let i = 0; i < formChoices.length; i++) {
        sessionStorage.setItem(formChoices[i].id, formFields[i].checked);
    }
}

function loadFormFromCookie() {
    for (let i = 0; i < formFields.length; i++) {
        if (sessionStorage.getItem(formFields[i].id)) {
            formFields[i].value = sessionStorage.getItem(formFields[i].id);
        }
    }
    for (let i = 0; i < formChoices.length; i++) {
        if (sessionStorage.getItem(formChoices[i].id)) {
            formFields[i].checked = sessionStorage.getItem(formChoices[i].id);
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
    if (document.getElementsByClassName("alert-danger")) {
        loadFormFromCookie();
    } else if (document.getElementsByClassName("alert-success")) {
        clearCookies();
    } else {
        clearCookies();
    }
}