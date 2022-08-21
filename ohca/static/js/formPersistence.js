const formFields = document.querySelectorAll('input:not([type="hidden"],[type="submit"],[type="radio"],[type="checkbox"])');
const formChoices = document.querySelectorAll('input[type="radio"],input[type="checkbox"]');
// for some reason dropdowns have to be handeled separately
const formDropdowns = ["id_systemID", "id_localID", "id_cod"];
const fields = document.querySelectorAll(".form-control");

function saveFormToCookie() {
    for (let i = 0; i < formDropdowns.length; i++) {
        if (document.getElementById(formDropdowns[i]) != null) {
            var elt = document.getElementById(formDropdowns[i]);
            if (elt.options[elt.selectedIndex] != null) {
                var eltval = elt.options[elt.selectedIndex].text;
                sessionStorage.setItem(formDropdowns[i], eltval);
                sessionStorage.setItem(formDropdowns[i], document.getElementById(formDropdowns[i]).value);
            }
        }
    }
    for (let i = 0; i < formFields.length; i++) {
        sessionStorage.setItem(formFields[i].id, formFields[i].value);
    }
    for (let i = 0; i < formChoices.length; i++) {
        sessionStorage.setItem(formChoices[i].id, formChoices[i].checked);
    }
}

function loadFormFromCookie() {
    console.log(sessionStorage.length);
    for (let i = 0; i < formDropdowns.length; i++) {
        if (sessionStorage.getItem(formDropdowns[i]) && document.getElementById(formDropdowns[i])) {
            document.getElementById(formDropdowns[i]).value = sessionStorage.getItem(formDropdowns[i]);
        }
    }
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
    console.log(sessionStorage);
    for (let i = 0; i < formFields.length; i++) {
        formFields[i].value = "";
        sessionStorage.setItem(formFields[i].id, "");
    }
    for (let i = 0; i < formChoices.length; i++) {
        formChoices[i].checked = false;
        sessionStorage.setItem(formChoices[i].id, false);
    }
    for (let i = 0; i < formDropdowns.length; i++) {
        if (document.getElementById(formDropdowns[i])) {
            var elt = document.getElementById(formDropdowns[i]);
            // if (elt.options[elt.selectedIndex] != null) {
            console.log(elt.options[elt.selectedIndex])
            // elt.options[elt.selectedIndex] = null;
            elt.selectedIndex = -1;
            sessionStorage.setItem(formDropdowns[i], null);
        }
    }
    // remove succes or error message
    document.querySelectorAll('.alert').forEach(function(a) {
        a.remove()
      })
    saveFormToCookie();
}

function clearCookies() {
    sessionStorage.clear();
}

function getCookie(cookieName) {
    let cookie = {};
    document.cookie.split(';').forEach(function(el) {
      let [key,value] = el.split('=');
      cookie[key.trim()] = value;
    })
    return cookie[cookieName];
  }

// adding extra function for deleting cookies just because
function deleteCookies() {
    var allCookies = document.cookie.split(';');
    
    // The "expire" attribute of every cookie is 
    // Set to "Thu, 01 Jan 1970 00:00:00 GMT"
    for (var i = 0; i < allCookies.length; i++) {
        let [key,value] = allCookies[i].split('=');
        if (key != "csrftoken") {
            document.cookie = allCookies[i] + "=;expires=" + new Date(0).toUTCString();
        }
    }       
}


function checkFormReload() {
    if (document.getElementsByClassName("alert-danger").length >= 1) {
        loadFormFromCookie();
        clearCookies();
        deleteCookies(); 
    } else if (document.getElementsByClassName("alert-success") >= 1) {
        clearCookies();
        deleteCookies();
    } else {
            loadFormFromCookie();
            clearCookies();
            deleteCookies();
        }
        }
        


window.onbeforeunload = function() {
    saveFormToCookie();
    return null

}