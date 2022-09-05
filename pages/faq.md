---
layout: Post
title: Pogosta vprašanja in odgovori
permalink: /faq/
content-type: eg
---
<style>
button {
    background:none;
    margin:none;
    border:none;
    padding:0.75em 0.1em 0 0;
}
.question {
    padding: 0.75em 0.9em 0em 0em !important;
    width:90%;
}
h7 {
    opacity: 0;
}
h1 {
    padding: 0em 0em 0.5em 0em;
}
.faq-button {
    width:5%;
}
.faq-copy {
    width:5%;
}
.faq-button:hover {
  opacity: 0.5;
}
.faq-copy:hover {
  opacity: 0.5;
}
.faq-answer {
    padding: 2% 0 2%;
}
.content table td {
    padding: 0 0 0 0;
}
.tooltip .tooltiptext {
  font-size: 13px;
  visibility: hidden;
  width: 100px;
  background-color: #555;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px;
  position: absolute;
  z-index: 1;
  bottom: 120%;
  left: 50%;
  margin-left: -35px;
  opacity: 0;
  transition: opacity 0.3s;
}
.tooltip:hover .tooltiptext {
  visibility: visible;
  opacity: 1;
}
</style>

<table>
    <tr>
        <td id="q1" class="question"></td>
        <td id="button1" class="faq-button"></td>
        <td class="tooltip" id="copy1" onclick="handleCopy1()" onmouseout="outCopy1()">
            <div class="faq-copy" id="check1" style="display:none; padding-top:3px;">
                <button>
                    <svg width="17" viewBox="0 0 101 102" fill="var(--text-main)" xmlns="http://www.w3.org/2000/svg">
                        <g clip-path="url(#clip0_120_268)" style="stroke:var(--text-main);  fill:var(--text-main);  opacity: 0.75;">
                        <path d="M39.073 75.6191C39.347 75.8921 39.717 76.0451 40.103 76.0451C40.117 76.0451 40.131 76.0451 40.144 76.0451C40.545 76.0341 40.922 75.8581 41.189 75.5591L85.393 26.0481C85.929 25.4481 85.877 24.5271 85.276 23.9921C84.676 23.4561 83.755 23.5091 83.22 24.1081L40.042 72.4701L17.254 49.6871C16.685 49.1181 15.763 49.1181 15.195 49.6871C14.626 50.2561 14.626 51.1781 15.195 51.7471L39.073 75.6191Z"  stroke-width="2.0"/>
                        <path d="M98.544 0H1.45701C0.653007 0 0.00100708 0.652 0.00100708 1.457V99.712C0.00100708 100.517 0.653007 101.169 1.45701 101.169H98.544C99.349 101.169 100 100.517 100 99.712V1.457C100 0.652 99.349 0 98.544 0ZM97.088 98.255H2.91301V2.912H97.088V98.255Z" stroke-width="2.0"/>
                        </g>
                        <defs>
                        <clipPath id="clip0_120_268">
                        <rect width="100.353" height="101.168" fill="var(--text-main)"/>
                        </clipPath>
                        </defs>
                    </svg>
                </button>
            </div>
        </td> 
    </tr>   
    <tr>
        <td id="q2" class="question"></td>
        <td id="button2" class="faq-button"></td>
        <td class="tooltip" id="copy2" onclick="handleCopy2()" onmouseout="outCopy2()"></td> 
    </tr>
    <tr>
        <td id="q3" class="question"></td>
        <td id="button3" class="faq-button"></td>
        <td class="tooltip"  id="copy3" onclick="handleCopy3()" onmouseout="outCopy3()"></td> 
    </tr>
    <tr>
        <td id="q4" class="question"></td>
        <td id="button4" class="faq-button"></td>
        <td class="tooltip" id="copy4" onclick="handleCopy4()" onmouseout="outCopy4()"></td> 
    </tr>
    <tr>
        <td id="q5" class="question"></td>
        <td id="button5" class="faq-button"></td>
        <td class="tooltip" id="copy5" onclick="handleCopy5()" onmouseout="outCopy5()"></td> 
    </tr>
</table>
<script src="https://siohca.um.si/assets/js/faq.js"></script>