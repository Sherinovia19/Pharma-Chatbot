const chatBox = document.getElementById("chat-box");
const input = document.getElementById("message-input");
const dashboard = document.getElementById("dashboard-cards");

function appendMessage(text, sender="bot") {
    const div = document.createElement("div");
    div.innerText = text;
    div.className = sender==="bot" ? "bot-message" : "user-message";
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

function addDashboardCard(med, status) {
    const div = document.createElement("div");
    div.className = "dashboard-card " + status;
    div.innerText = `${med} - ${status.replace("-"," ").toUpperCase()}`;
    dashboard.prepend(div);
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

        let status = "safe";
        if(data.reply.toLowerCase().includes("expired") || data.reply.toLowerCase().includes("recalled")) status = "expired";
        else if(data.reply.toLowerCase().includes("near expiry")) status = "near-expiry";

        addDashboardCard(msg, status);
        appendMessage(data.reply, "bot");
    } catch(e) {
        chatBox.removeChild(typing);
        appendMessage("⚠️ Bot encountered an error. Please try again.", "bot");
    }
}

input.addEventListener("keypress", e => { if(e.key==="Enter") sendMessage(); });
