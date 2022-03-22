import { TypingDNA } from "./typingdna.js";
import { AutocompleteDisabler } from "./autocomplete-disabler.js";

// https://github.com/TypingDNA/autocomplete-disabler

const tdna = new TypingDNA();

const autocompleteDisabler = new AutocompleteDisabler({
  showTypingVisualizer: true,
  showTDNALogo: true,
});
autocompleteDisabler.disableAutocomplete();
autocompleteDisabler.disableCopyPaste();

const typingPatternsButton = document.getElementById("typing-patterns-btn");
const email = document.getElementById("email");
const password = document.getElementById("password");
const id_obj = document.querySelector("#user_tid").value;
const frm = document.getElementById('typing-patterns-form');
var payload = {};

typingPatternsButton.addEventListener("click", () => {
    const text = email.value + password.value;
    tdna.addTarget("email");
    tdna.addTarget("password"); 
    sendPattern(text);
});


function sendPattern(text){
    const pattern = tdna.getTypingPattern({
        type: 1,
        text: text
    })
    if (id_obj.length > 0){
      payload = {pattern: pattern, user_tid: id_obj};
    }
    else {
      console.log(id_obj);
      console.log(id_obj.length);
      payload = {pattern: pattern, user_tid: localStorage.getItem('user_tid')};
    }
    console.log(payload);
    fetch("/sendtypingdata", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        credentials: 'include',
        body: JSON.stringify(payload)
    })
    .then((response) => response.json())
    .then((data) => {
        console.log(data);
        if (data.message_code == 10) {
          alert(
            "In order to verify your identity, you will be required to fill this form a couple of times."
          );
          frm.reset();
        } 
        else {
          if (data.result == 1) {
            alert(
              "TypingDNA indicated that there was HIGH confidence in your login pattern"
            );
            window.parent.postMessage('Verified', '*');
          } else {
            alert(
              "TypingDNA indicated that there was LOW confidence in your login pattern"
            );
          }
        }
      });
    tdna.reset();
}