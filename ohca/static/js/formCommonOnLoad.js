const datepickers = document.getElementsByClassName("datepickerinput")

const callTimeStampField = document.getElementById("id_callTimestamp_0")
const dateOfCAField = document.getElementById("id_Date")
callTimeStampField.addEventListener('onchange', updateDateFields())
dateOfCAField.addEventListener('onchange', updateDateFields())

function updateDateFields() {
    const excludedIds = [callTimeStampField.id, dateOfCAField.id, "id_Date_birth"]
    var date = callTimeStampField.
    datepickers.array.forEach(datepicker => {
        if (!(excludedIds.includes(datepicker.id))) {
            datepicker.value = date
        }
    });
}