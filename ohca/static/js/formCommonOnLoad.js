const datepickers = document.getElementsByClassName("datepickerinput")

const callTimeStampField = document.getElementById("id_callTimestamp_0")
const dateOfCAField = document.getElementById("id_dateOfCA")
if (callTimeStampField) {
    callTimeStampField.addEventListener('change', function() { updateDateFields(callTimeStampField) })
}
if (dateOfCAField) {
    dateOfCAField.addEventListener('change', function() { updateDateFields(dateOfCAField) })
}

function updateDateFields(caller) {
    let date = caller.value
    const excludedIds = ["id_dateOfBirth"]
    for (let i = 0; i < datepickers.length; i++) {
        if (!(excludedIds.includes(datepickers[i].id) || datepickers[i].id == caller.id)) {
            datepickers[i].value = date
        }
    };
}

function addTextBoxUnit(tbID) {
    inner = document.createElement("span");
    inner.classList.add("input-group-text");
    inner.innerText = "°C";
    unit = document.createElement("div");
    unit.classList.add("input-group-append");
    unit.appendChild(inner);
    ttmTempDiv = document.getElementById(tbID).parentElement;
    ttmTempDiv.classList.add("input-group");
    ttmTempDiv.appendChild(unit);
}

addTextBoxUnit("id_ttmTemp");