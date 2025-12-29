const chatBox = document.getElementById("chat-box");
const input = document.getElementById("message");

function addMessage(text, sender) {
  const div = document.createElement("div");
  div.className = sender;
  div.innerHTML = text.replace(/\n/g, "<br>");
  chatBox.appendChild(div);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function showTyping() {
  const div = document.createElement("div");
  div.id = "typing";
  div.className = "bot typing";
  div.innerText = "🤖 typing...";
  chatBox.appendChild(div);
}

function removeTyping() {
  const t = document.getElementById("typing");
  if (t) t.remove();
}

async function sendMessage() {
  const msg = input.value.trim();
  if (!msg) return;

  addMessage(msg, "user");
  input.value = "";

  showTyping();

  const res = await fetch("/api/message", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ message: msg })
  });

  const data = await res.json();
  removeTyping();
  addMessage(data.reply, "bot");
}
