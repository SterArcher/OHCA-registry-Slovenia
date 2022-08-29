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


// ===========================================


function handleTreatmentWithdrawn() {
    var val = document.getElementById("id_treatmentWithdrawn_0").checked;
    // var death2 = document.getElementById("id_survival30d_1");
    if (val) {

        document.getElementById("id_treatmentWithdrawnTimestamp_0").setAttribute("required", "");
        document.getElementById("id_treatmentWithdrawnTimestamp_1").setAttribute("required", "");
    }
    else {
        document.getElementById("id_treatmentWithdrawnTimestamp_0").removeAttribute("required");
        document.getElementById("id_treatmentWithdrawnTimestamp_1").removeAttribute("required");
    }}
document.getElementById("id_treatmentWithdrawn_0").addEventListener("change", handleTreatmentWithdrawn)
document.getElementById("id_treatmentWithdrawn_1").addEventListener("change", handleTreatmentWithdrawn)
document.getElementById("id_treatmentWithdrawn_2").addEventListener("change", handleTreatmentWithdrawn)
document.getElementById("id_treatmentWithdrawn_3").addEventListener("change", handleTreatmentWithdrawn)

function handleDiscDate() {
    var val = document.getElementById("id_survivalDischarge_0").checked;
    console.log(val)
    if (val) {
        document.getElementById("id_discDate").setAttribute("required", "");
    }
    else {
        document.getElementById("id_discDate").removeAttribute("required");
    }}
document.getElementById("id_survivalDischarge_0").addEventListener("change", handleDiscDate)
document.getElementById("id_survivalDischarge_1").addEventListener("change", handleDiscDate)
document.getElementById("id_survivalDischarge_2").addEventListener("change", handleDiscDate)
document.getElementById("id_survivalDischarge_3").addEventListener("change", handleDiscDate)



window.onload = function require() {
    checkFormReload();
    handleTreatmentWithdrawn();
    handleDiscDate();
}