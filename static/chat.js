const chatBox = document.getElementById("chat-box");
const input = document.getElementById("message-input");

function appendMessage(text, sender="bot") {
    const div = document.createElement("div");
    div.innerText = text;
    div.className = sender==="bot" ? "bot-message" : "user-message";
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

async function sendMessage() {
    const msg = input.value.trim();
    if(!msg) return;
    appendMessage(msg, "user");
    input.value = "";

    const typing = document.createElement("div");
    typing.innerText = "...";
    typing.className = "bot-message";
    chatBox.appendChild(typing);

    try {
        const res = await fetch("/api/message", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({message: msg})
        });
        const data = await res.json();
        chatBox.removeChild(typing);
        appendMessage(data.reply, "bot");
    } catch(e) {
        chatBox.removeChild(typing);
        appendMessage("⚠️ Bot encountered an error. Please try again.", "bot");
    }
}

function quickAction(type) {
    if(type==="scan") sendQuick("Check medicine: ");
    if(type==="storage") sendQuick("How should I store ");
    if(type==="side_effects") sendQuick("Side effects of ");
}

function sendQuick(text) {
    input.value = text;
    sendMessage();
}

input.addEventListener("keypress", e => { if(e.key==="Enter") sendMessage(); });
