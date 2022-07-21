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
        } else if (event.key != "ArrowLeft" && event.key != "ArrowRight") {
            inputs[i].setAttribute("type", "number");
            inputs[i].value = ''; // Bug Fix: allow user to change a random otp digit after pressing it
        }
    });
    inputs[i].addEventListener('input', function() {
        inputs[i].value = inputs[i].value; // Converts to Upper case. Remove .toUpperCase() if conversion isnt required.
        if (i === inputs.length - 1 && inputs[i].value !== '') {
            return true;
        } else if (inputs[i].value !== '') {
            inputs[i + 1].focus();
        }
    });

}