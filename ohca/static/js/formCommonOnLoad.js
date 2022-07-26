const datepickers = document.getElementsByClassName("datepickerinput")

const callTimeStampField = document.getElementById("id_callTimestamp_0")
const dateOfCAField = document.getElementById("id_Date")
callTimeStampField.addEventListener('change', function() { updateDateFields(callTimeStampField) })
dateOfCAField.addEventListener('change', function() { updateDateFields(dateOfCAField) })

function updateDateFields(caller) {
    let date = caller.value
    const excludedIds = ["id_Date_birth"]
    for (let i = 0; i < datepickers.length; i++) {
        if (!(excludedIds.includes(datepickers[i].id) || datepickers[i].id == caller.id)) {
            datepickers[i].value = date
        }
    };
}