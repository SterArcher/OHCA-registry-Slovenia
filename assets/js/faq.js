// READ Q AND A FROM CSV
var CSVurl = "https://siohca.um.si/assets/js/questionsAndAnswers.csv";
var request = new XMLHttpRequest();  
request.open("GET", CSVurl, false);   
request.send(null);  
var csvData = new Array();
var jsonObject = request.responseText.split('\n');
for (var i = 1; i < jsonObject.length; i++) {
     csvData.push(jsonObject[i].split(';'));
}
console.log(csvData);


// INSERT QUESTION, ANSWER, ICONS  
const questions = csvData.map(x => x[0]).flat(2);
const answers = csvData.map(x => x[1]).flat(2);
console.log(questions);
for (let i=1;i<(questions.length+1);i++){
     var question = questions[i-1];
     var num = i.toString();
     var tableRow = document.getElementById("faq-table");
     var questionCode = "<h6>" + question + "</h6><div class=\"faq-answer\"><h7 id=\"a" + num + "\"></h7></div>";
     var buttonCode = "<button id=\"b" + num + "\"><svg version=\"1.0\" xmlns=\"http://www.w3.org/2000/svg\" width=\"12pt\" viewBox=\"0 0 512.000000 512.000000\" preserveAspectRatio=\"xMidYMid meet\"><g transform=\"translate(0.000000,512.000000) scale(0.100000,-0.100000)\" fill=\"#000000\" stroke=\"none\" style=\"fill:var(--text-main);\"><path d=\"M4980 3893 c-17 -3 -405 -384 -1223 -1201 l-1197 -1197 -1188 1187 c-653 652 -1197 1191 -1209 1197 -88 45 -191 -47 -154 -137 7 -15 571 -586 1254 -1269 918 -917 1249 -1242 1269 -1245 16 -3 40 -3 55 -1 21 4 352 329 1275 1252 1098 1097 1248 1250 1253 1283 15 80 -52 145 -135 131z\"/></g></svg></button>";
     var copyCode = "<span class=\"tooltiptext\" id=\"myTooltip" + num + "\">Kopiraj povezavo do vprašanja</span><div class=\"faq-copy\" style=\"display:block;\"><button> <svg version=\"1.0\" xmlns=\"http://www.w3.org/2000/svg\" width=\"12pt\" height=\"12pt\" viewBox=\"0 0 512.000000 512.000000\" preserveAspectRatio=\"xMidYMid meet\"><g transform=\"translate(0.000000,512.000000) scale(0.100000,-0.100000)\" fill=\"#000000\" stroke=\"none\" style=\"fill:var(--text-main);  opacity: 0.75;\"><path d=\"M1720 5104 c-155 -42 -269 -173 -293 -337 -10 -67 -9 -78 10 -113 26 -50 72 -77 129 -76 77 1 127 52 139 144 10 68 47 104 118 113 28 3 585 5 1237 3 1298 -3 1205 1 1248 -60 16 -21 17 -160 20 -1749 2 -1370 0 -1734 -10 -1765 -15 -45 -66 -84 -110 -84 -38 0 -104 -34 -119 -61 -37 -70 -29 -136 21 -184 25 -24 40 -30 93 -33 158 -10 314 95 379 255 l23 58 0 1790 c0 1710 -1 1792 -18 1843 -36 103 -132 202 -237 245 l-55 22 -1260 2 c-1086 2 -1268 0 -1315 -13z\"/> <path d=\"M785 4202 c-108 -37 -202 -129 -247 -239 l-23 -58 0 -1790 c0 -1710 1 -1792 18 -1843 36 -103 132 -202 237 -245 l55 -22 1254 -3 c1366 -3 1319 -4 1417 53 97 57 174 166 194 276 7 37 9 643 8 1815 l-3 1759 -23 58 c-46 113 -140 201 -256 240 -45 16 -162 17 -1315 16 -1167 0 -1270 -2 -1316 -17z m2564 -276 c15 -8 37 -28 47 -43 18 -27 19 -76 19 -1768 0 -1646 -1 -1742 -18 -1768 -9 -15 -29 -35 -44 -44 -26 -17 -98 -18 -1243 -18 -1315 0 -1259 -2 -1297 54 -17 25 -18 109 -21 1752 -2 1368 0 1735 10 1765 8 24 26 47 47 61 l34 23 1219 0 c1045 0 1223 -2 1247 -14z\"/></g></svg> </button> </div>";
     tableRow.innerHTML += "<tr><td id=\"q" + num + "\" class=\"question\">" + questionCode + "</td>" + "<td id=\"button" + num + "\" class=\"faq-button\">" + buttonCode + "</td>" +"<td class=\"tooltip\" id=\"copy" + num + "\">" + copyCode + "</td></tr>";
}

// OPEN QUESTION OF ID LINK
const questionURL = window.location.href;
for (let i=1;i<(answers.length+1);i++){
     var num = i.toString();
     if (questionURL == "https://siohca.um.si/faq/#q" + num){
          document.getElementById('a' + num).innerText = answers[i-1];
          document.getElementById('a' + num).style.opacity = "1";
          document.getElementById('a' + num).style.transition = "all 0.3s";
          document.getElementById('b' + num).style.transform = "rotate(-180deg)";
          document.getElementById('b' + num).style.transition = "all 0.5s";
     }
}

// HANDLE ANSWER
for (let i=1;i<(answers.length+1);i++){
     showAnswerOnButtonClick(i);
     showAnswerOnQuestionClick(i);
}
      
function showAnswerOnButtonClick(i){
     var num = i.toString();
     var question = document.getElementById('q' + num);
     question.addEventListener('click', function() {
          if( document.getElementById('a' + num).innerText == answers[i-1]){
               document.getElementById('a' + num).innerText = "";
               document.getElementById('a' + num).style.opacity = "0";
               document.getElementById('a' + num).style.transition = "all 0.3s";
               document.getElementById('b' + num).style.transform = "";
      
          } else {
               document.getElementById('a' + num).innerText = answers[i-1];
               document.getElementById('a' + num).style.opacity = "1";
               document.getElementById('a' + num).style.transition = "all 0.3s";
               document.getElementById('b' + num).style.transform = "rotate(-180deg)";
               document.getElementById('b' + num).style.transition = "all 0.5s";
          }   
      }) 
}

function showAnswerOnQuestionClick(i){
     var num = i.toString();
     var button = document.getElementById('button' + num);
     button.addEventListener('click', function() {
          if( document.getElementById('a' + num).innerText == answers[i-1]){
               document.getElementById('a' + num).innerText = "";
               document.getElementById('a' + num).style.opacity = "0";
               document.getElementById('a' + num).style.transition = "all 0.3s";
               document.getElementById('b' + num).style.transform = "";
     
          } else {
               document.getElementById('a' + num).innerText = answers[i-1];
               document.getElementById('a' + num).style.opacity = "1";
               document.getElementById('a' + num).style.transition = "all 0.3s";
               document.getElementById('b' + num).style.transform = "rotate(-180deg)";
               document.getElementById('b' + num).style.transition = "all 0.5s";
          }  
      })
}


// COPY LINK
for (let i=1;i<(questions.length+1);i++){
     handleCopyIconClick(i);
     handleMouseOut(i);
}

function handleCopyIconClick(i){
     var num = i.toString();
     var field = document.getElementById("copy" + num);
     field.addEventListener('click', function(){
          navigator.clipboard.writeText("https://siohca.um.si/faq#q" + num);
          var tooltip = document.getElementById("myTooltip" + num);
          tooltip.innerHTML = "Kopirana povezava do vprašanja!";
     })
}

function handleMouseOut(i){
     var num = i.toString();
     var field = document.getElementById("copy" + num);
     field.addEventListener('mouseout', function(){
          var tooltip = document.getElementById("myTooltip" + num);
          tooltip.innerHTML = "Kopiraj";
     })
}


//const questions = ["Če pride do zastoja v neki ambulanti družinske medicine ali dežurni periferni ambulanti, je tak bolnik vključen v študijo, saj je aktivirana NMP (kaj je v tem primeru kraj srčnega zastoja - drugo?). Kaj pa če pride do zastoja v ambulanti dežurne medicine ali dežurni ambulanti (tako v UC, kot izven UC), je bolnik vključen v študijo?",
//"Kako izpolnimo polje \"Potrjen srčni zastoj\"?", "Kako izpolnimo polje \"Nujna vožnja\"?", "Kako izpolnimo polje \"Mehanski stiski prsnega koša\" v primeru, da naprava ni bila uporabljena?", "Kako izpolnimo polje \"Začetni/prvi ritem (EuReCa3)\" v primeru, da AED ni bil uporabljen?"];
//const answers = ["Bolnik je vključen v študijo. Lokacija zastoja: drugo.", "Pri potrjenem srčnem zastoju je mišljeno, da je potrjen s strani NMP in ne dispečerja. Lahko se zgodi, da dispečer daje navodila za TPO, ko NMP prispe na kraj dogodka ugotovi, da ni bil srčni zastoj ampak le stanje, ki ga je posnemalo.", "V primeru, da je naročen mrtvogled, izberemo NE. V primeru, da gre za nujno vožnjo s prižganimi modrimi lučmi in sireno, izberemo DA.", "V tem primeru obkrožite \"Neznano/ni podatka\".", "Izberite odgovor ne glede ali je bil uporabljen AED ali ne ali če je prvi ritem prepoznan s strani NMP z npr. Lifepack."]