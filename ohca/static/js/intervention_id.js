// Switch between fields
const inputs = document.querySelectorAll('[id^=id_i].numberinput');

console.log(inputs);
for (let i = 0; i < inputs.length; i++) {
    inputs[i].setAttribute("maxlength", 1);
    inputs[i].addEventListener('keydown', function(event) {
        if (event.key === "Backspace") {

            if (inputs[i].value == '') {
                if (i != 0) {
                    inputs[i - 1].focus();
                }
            } else {
                inputs[i].value = '';
            }

        } else if (event.key === "ArrowLeft" && i !== 0) {
            inputs[i - 1].focus();
        } else if (event.key === "ArrowRight" && i !== inputs.length - 1) {
            inputs[i + 1].focus();
        } else if (event.key === "Enter") {
            document.getElementById("id_Patient_name").focus();
        } else if (event.key !== "Tab") {
            inputs[i].setAttribute("type", "number");
            inputs[i].value = '';
        }
    });

    inputs[i].addEventListener('input', function() {
        inputs[i].value = inputs[i].value;
        handleIDchange();
        if (i === inputs.length - 1 && inputs[i].value !== '') {
            document.getElementById("id_Patient_name").focus();
        } else if (inputs[i].value !== '') {
            inputs[i + 1].focus();
        }
    });

}

function handleIDchange() {
    b1 = (inputs[0].value.length != 0);
    b2 = (inputs[1].value.length != 0);
    b3 = (inputs[2].value.length != 0);
    b4 = (inputs[3].value.length != 0);
    b5 = (inputs[4].value.length != 0);
    b6 = (inputs[5].value.length != 0);
    b7 = (inputs[6].value.length != 0);
    b8 = (inputs[7].value.length != 0);
    b9 = (inputs[8].value.length != 0);
    b10 = (inputs[9].value.length != 0);
    b11 = (inputs[10].value.length != 0);
    b12 = (inputs[11].value.length != 0);

    // Handle dispatch centre
    if (b1 && b2) {
        if (inputs[0].value == 0) {
            if (inputs[1].value == 1) {
                document.getElementById('dsz').innerHTML = "Ljubljana";
            } else if (inputs[1].value == 2) {
                document.getElementById('dsz').innerHTML = "Maribor";
            } else {
                document.getElementById('dsz').innerHTML = "-----";
            }
        } else {
            document.getElementById('dsz').innerHTML = "-----";
        }
    }

    year = ''
    month = ''
    day = ''
        // Handle year
    if (b3 && b4) {
        year = '20';
        year += String(inputs[2].value) + String(inputs[3].value);
    }
    // Handle month
    if (b5 && b6) {
        month += String(inputs[4].value) + String(inputs[5].value);
    }
    // Handle day
    if (b7 && b8) {
        day += String(inputs[6].value) + String(inputs[7].value);
    }
    // Handle date change
    if (b3 && b4 && b5 && b6 && b7 && b8) {
        document.getElementById('id_Date').value = year + '-' + month + '-' + day;
    }

    // Handle intervention number
    if (b9 && b10 && b11 & b12) {
        intNum = String(inputs[8].value) + String(inputs[9].value) + String(inputs[10].value) + String(inputs[11].value);
        document.getElementById('intNum').innerHTML = parseInt(intNum);
    }
}