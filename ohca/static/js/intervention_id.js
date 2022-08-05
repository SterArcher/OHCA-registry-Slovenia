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
                handleIDchange();
                checkValidity();
            }

        } else if (event.key === "Delete" || event.key === "Clear") {
            inputs[i].value = '';
            handleIDchange();
            checkValidity();
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
        checkValidity();
    });

}

function checkValidity() {
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].classList.remove("correct");
        inputs[i].classList.remove("incorrect");
        if (inputs[i].value.length !== 0) {
            if (i == 0) {
                if (inputs[i].value == 0) {
                    inputs[i].classList.add("correct");
                } else {
                    inputs[i].classList.add("incorrect");
                }
            } else if (i == 1) {
                if (inputs[i].value > 2) {
                    inputs[i].classList.add("incorrect");
                } else {
                    inputs[i].classList.add("correct");
                }
            } else if (i == 4) {
                if (inputs[i].value < 2) {
                    inputs[i].classList.add("correct");
                } else {
                    inputs[i].classList.add("incorrect");
                }
            } else if (i == 5) {
                if (inputs[i - 1].value == 0 || (inputs[i - 1].value == 1 && inputs[i].value <= 2)) {
                    inputs[i].classList.add("correct");
                } else {
                    inputs[i - 1].classList.add("incorrect");
                    inputs[i].classList.add("incorrect");
                }
            } else if (i == 6) {
                if (inputs[i].value <= 2 || (inputs[i].value <= 3 && (inputs[5].value != 2 && inputs[4] == 0))) {
                    inputs[i].classList.add("correct");
                } else {
                    inputs[i].classList.add("incorrect");
                }
            } else if (i == 7) {
                day = '' + inputs[6].value + inputs[7].value;
                month = '' + inputs[4].value + inputs[5].value;
                year = '20' + inputs[2].value + inputs[3].value;
                if ((month == 2 && day <= 28) || ([1, 3, 5, 7, 8, 10, 12].includes(parseInt(month)) && day <= 32) || ([4, 6, 9, 11].includes(parseInt(month)) && day <= 31) || (month == 2 && day == 29 && leapyear(year))) {
                    inputs[i].classList.add("correct");
                } else {
                    inputs[i].classList.add("incorrect");
                }
            } else if (i > 7 || i == 2 || i == 3) {
                if (inputs[i].value.length == 1) {
                    inputs[i].classList.add("correct");
                } else {
                    inputs[i].classList.add("incorrect");
                }
            }
        }
    }
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
            switch (inputs[1].value) {
                case '1':
                    document.getElementById('dsz').innerHTML = "Ljubljana";
                    break;
                case '2':
                    document.getElementById('dsz').innerHTML = "Maribor";
                    break;
                default:
                    document.getElementById('dsz').innerHTML = "-----";
            }
        } else {
            document.getElementById('dsz').innerHTML = "-----";
        }
    } else {
        document.getElementById('dsz').innerHTML = "-----";
    }

    year = '----';
    month = '--';
    day = '--';
    // Handle year
    if (b3 && b4) {
        year = '20';
        year += String(inputs[2].value) + String(inputs[3].value);
    }
    // Handle month
    if (b5 && b6) {
        month = '';
        month += String(inputs[4].value) + String(inputs[5].value);
    }
    // Handle day
    if (b7 && b8) {
        day = '';
        day += String(inputs[6].value) + String(inputs[7].value);
    }
    // Handle date change
    if (b3 && b4 && b5 && b6 && b7 && b8) {
        document.getElementById('id_Date').value = year + '-' + month + '-' + day;
        document.getElementById('id_Date').dispatchEvent(new Event('change'));
    }
    document.getElementById('dateInt').innerHTML = day + '/' + month + '/' + year;

    // Handle intervention number
    if (b9 && b10 && b11 & b12) {
        intNum = String(inputs[8].value) + String(inputs[9].value) + String(inputs[10].value) + String(inputs[11].value);
        document.getElementById('intNum').innerHTML = parseInt(intNum);
    } else {
        document.getElementById('intNum').innerHTML = "-----";
    }
}

function leapyear(year) {
    return (year % 100 === 0) ? (year % 400 === 0) : (year % 4 === 0);
}