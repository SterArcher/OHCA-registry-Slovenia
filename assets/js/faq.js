const Button1 = document.getElementById('button1');
const Question1 = document.getElementById('q1');
const Answer1 =  "Bolnik je vključen v štuudijo. Lokacija zastoja: drugo.";
Button1.addEventListener('click', function() {
    if( document.getElementById('a1').innerText == Answer1){
         document.getElementById('a1').innerText = "";
         document.getElementById('a1').style.opacity = "0";
         document.getElementById('a1').style.transition = "all 0.3s";
         document.getElementById('b1').style.transform = "";

    } else {
         document.getElementById('a1').innerText = Answer1;
         document.getElementById('a1').style.opacity = "1";
         document.getElementById('a1').style.transition = "all 0.3s";
         document.getElementById('b1').style.transform = "rotate(-180deg)";
         document.getElementById('b1').style.transition = "all 0.5s";
    }
})
    Question1.addEventListener('click', function() {
     if( document.getElementById('a1').innerText == Answer1){
          document.getElementById('a1').innerText = "";
          document.getElementById('a1').style.opacity = "0";
          document.getElementById('a1').style.transition = "all 0.3s";
          document.getElementById('b1').style.transform = "";
 
     } else {
          document.getElementById('a1').innerText = Answer1;
          document.getElementById('a1').style.opacity = "1";
          document.getElementById('a1').style.transition = "all 0.3s";
          document.getElementById('b1').style.transform = "rotate(-180deg)";
          document.getElementById('b1').style.transition = "all 0.5s";
     }
    
    })

const Button2 = document.getElementById('button2');
const Question2 = document.getElementById('q2');
const Answer2 = "Pri potrjenem srčnem zastoju je mišljeno, da je potrjen s strani NMP in ne dispečerja. Lahko se zgodi, da dispečer daje navodila za TPO, ko NMP prispe na kraj dogodka ugotovi, da ni bil srčni zastoj ampak le stanje, ki ga je posnemalo.";
Button2.addEventListener('click', function() {
    if( document.getElementById('a2').innerText == Answer2){
         document.getElementById('a2').innerText = "";
         document.getElementById('a2').style.opacity = "0";
         document.getElementById('a2').style.transition = "all 0.3s";
         document.getElementById('b2').style.transform = "";

    } else {
         document.getElementById('a2').innerText = Answer2;
         document.getElementById('a2').style.opacity = "1";
         document.getElementById('a2').style.transition = "all 0.3s";
         document.getElementById('b2').style.transform = "rotate(-180deg)";
         document.getElementById('b2').style.transition = "all 0.5s";
    }
    
})
Question2.addEventListener('click', function() {
     if( document.getElementById('a2').innerText == Answer2){
          document.getElementById('a2').innerText = "";
          document.getElementById('a2').style.opacity = "0";
          document.getElementById('a2').style.transition = "all 0.3s";
          document.getElementById('b2').style.transform = "";
 
     } else {
          document.getElementById('a2').innerText = Answer2;
          document.getElementById('a2').style.opacity = "1";
          document.getElementById('a2').style.transition = "all 0.3s";
          document.getElementById('b2').style.transform = "rotate(-180deg)";
          document.getElementById('b2').style.transition = "all 0.5s";
     }
     
 })

const Button3 = document.getElementById('button3');
const Question3 = document.getElementById('q3');
const Answer3 = "V primeru, da je naročen mrtvogled, izberemo NE. V primeru, da gre za nujno vožnjo s prižganimi modrimi lučmi in sireno, izberemo DA.";
Button3.addEventListener('click', function() {
    if( document.getElementById('a3').innerText == Answer3){
         document.getElementById('a3').innerText = "";
         document.getElementById('a3').style.opacity = "0";
         document.getElementById('a3').style.transition = "all 0.3s";
         document.getElementById('b3').style.transform = "";

    } else {
         document.getElementById('a3').innerText = Answer3;
         document.getElementById('a3').style.opacity = "1";
         document.getElementById('a3').style.transition = "all 0.3s";
         document.getElementById('b3').style.transform = "rotate(-180deg)";
         document.getElementById('b3').style.transition = "all 0.5s";
    }
    
})
Question3.addEventListener('click', function() {
     if( document.getElementById('a3').innerText == Answer3){
          document.getElementById('a3').innerText = "";
          document.getElementById('a3').style.opacity = "0";
          document.getElementById('a3').style.transition = "all 0.3s";
          document.getElementById('b3').style.transform = "";
 
     } else {
          document.getElementById('a3').innerText = Answer3;
          document.getElementById('a3').style.opacity = "1";
          document.getElementById('a3').style.transition = "all 0.3s";
          document.getElementById('b3').style.transform = "rotate(-180deg)";
          document.getElementById('b3').style.transition = "all 0.5s";
     }
     
 })

const Button4 = document.getElementById('button4');
const Question4 = document.getElementById('q4');
const Answer4 = "V tem primeru obkrožite \"Neznano/ni podatka\".";
Button4.addEventListener('click', function() {
    if( document.getElementById('a4').innerText == Answer4){
         document.getElementById('a4').innerText = "";
         document.getElementById('a4').style.opacity = "0";
         document.getElementById('a4').style.transition = "all 0.3s";
         document.getElementById('b4').style.transform = "";

    } else {
         document.getElementById('a4').innerText = Answer4;
         document.getElementById('a4').style.opacity = "1";
         document.getElementById('a4').style.transition = "all 0.3s";
         document.getElementById('b4').style.transform = "rotate(-180deg)";
         document.getElementById('b4').style.transition = "all 0.5s";
    }
    
})
Question4.addEventListener('click', function() {
     if( document.getElementById('a4').innerText == Answer4){
          document.getElementById('a4').innerText = "";
          document.getElementById('a4').style.opacity = "0";
          document.getElementById('a4').style.transition = "all 0.3s";
          document.getElementById('b4').style.transform = "";
 
     } else {
          document.getElementById('a4').innerText = Answer4;
          document.getElementById('a4').style.opacity = "1";
          document.getElementById('a4').style.transition = "all 0.3s";
          document.getElementById('b4').style.transform = "rotate(-180deg)";
          document.getElementById('b4').style.transition = "all 0.5s";
     }
     
 })

const Button5 = document.getElementById('button5');
const Question5 = document.getElementById('q5');
const Answer5 = "Izberite odgovor ne glede ali je bil uporabljen AED ali ne ali če je prvi ritem prepoznan s strani NMP z npr. Lifepack.";
Button5.addEventListener('click', function() {
    if( document.getElementById('a5').innerText == Answer5){
         document.getElementById('a5').innerText = "";
         document.getElementById('a5').style.opacity = "0";
         document.getElementById('a5').style.transition = "all 0.3s";
         document.getElementById('b5').style.transform = "";

    } else {
         document.getElementById('a5').innerText = Answer5;
         document.getElementById('a5').style.opacity = "1";
         document.getElementById('a5').style.transition = "all 0.3s";
         document.getElementById('b5').style.transform = "rotate(-180deg)";
         document.getElementById('b5').style.transition = "all 0.5s";
    }
})
Question5.addEventListener('click', function() {
     if( document.getElementById('a5').innerText == Answer5){
          document.getElementById('a5').innerText = "";
          document.getElementById('a5').style.opacity = "0";
          document.getElementById('a5').style.transition = "all 0.3s";
          document.getElementById('b5').style.transform = "";
 
     } else {
          document.getElementById('a5').innerText = Answer5;
          document.getElementById('a5').style.opacity = "1";
          document.getElementById('a5').style.transition = "all 0.3s";
          document.getElementById('b5').style.transform = "rotate(-180deg)";
          document.getElementById('b5').style.transition = "all 0.5s";
     }
    
})

// COPY LINK
function handleCopy1() {
     navigator.clipboard.writeText("https://siohca.um.si/faq#q1");
     var tooltip = document.getElementById("myTooltip1");
     tooltip.innerHTML = "Kopirana povezava do vprašanja!";
 }
 
 function outCopy1() {
   var tooltip = document.getElementById("myTooltip1");
   tooltip.innerHTML = "Kopiraj";
 }
 function handleCopy2() {
     navigator.clipboard.writeText("https://siohca.um.si/faq#q2");
     var tooltip = document.getElementById("myTooltip2");
     tooltip.innerHTML = "Kopirana povezava do vprašanja!";
 }
 
 function outCopy2() {
   var tooltip = document.getElementById("myTooltip2");
   tooltip.innerHTML = "Kopiraj";
 }
 function handleCopy3() {
     navigator.clipboard.writeText("https://siohca.um.si/faq#q3");
     var tooltip = document.getElementById("myTooltip3");
     tooltip.innerHTML = "Kopirana povezava do vprašanja!";
 }
 
 function outCopy3() {
   var tooltip = document.getElementById("myTooltip3");
   tooltip.innerHTML = "Kopiraj";
 }
 function handleCopy4() {
     navigator.clipboard.writeText("https://siohca.um.si/faq#q4");
     var tooltip = document.getElementById("myTooltip4");
     tooltip.innerHTML = "Kopirana povezava do vprašanja!";
 }
 
 function outCopy4() {
   var tooltip = document.getElementById("myTooltip4");
   tooltip.innerHTML = "Kopiraj";
 }
 function handleCopy5() {
     navigator.clipboard.writeText("https://siohca.um.si/faq#q5");
     var tooltip = document.getElementById("myTooltip5");
     tooltip.innerHTML = "Kopirana povezava do vprašanja!";
 }
 
 function outCopy5() {
   var tooltip = document.getElementById("myTooltip5");
   tooltip.innerHTML = "Kopiraj";
 }