import { TypingDNA } from "./typingdna.js";

const tdna = new TypingDNA();

const typingPatternsButton = document.getElementById("typing-patterns-btn");
const email = document.getElementById("email").value;
const password = document.getElementById("password").value;

const getCookieValue = (name) => (
    document.cookie.match('(^|;)\\s*' + name + '\\s*=\\s*([^;]+)')?.pop() || ''
)

typingPatternsButton.addEventListener("click", () => {
    const text = email + password;
    tdna.addTarget("email");
    tdna.addTarget("password"); 
    sendPattern(text);
});


function sendPattern(text){
    const pattern = tdna.getTypingPattern({
        type: 1,
        text: text
    })
    fetch("/sendtypingdata", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        credentials: 'include',
        body: JSON.stringify({pattern: pattern, user_tid: localStorage.getItem('user_tid')})
    })
    .then((response) => console.log(response.json()))
}