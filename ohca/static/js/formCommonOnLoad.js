const datepickers = document.getElementsByClassName("datepickerinput")

const callTimeStampField = document.getElementById("id_callTimestamp_0")
const dateOfCAField = document.getElementById("id_Date")
callTimeStampField.addEventListener('onchange', updateDateFields(callTimeStampField.value))
dateOfCAField.addEventListener('onchange', updateDateFields(dateOfCAField.value))

function updateDateFields(date) {
    const excludedIds = [callTimeStampField.id, dateOfCAField.id, "id_Date_birth"]
    for (let i = 0; i < datepickers.length; i++) {
        if (!(excludedIds.includes(datepickers[i].id))) {
            datepickers[i].value = date
        }
    };
}