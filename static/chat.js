const chat = document.getElementById("chat");

function add(text, cls) {
  const d = document.createElement("div");
  d.className = cls;
  d.innerHTML = text; // allow emojis
  chat.appendChild(d);
  chat.scrollTop = chat.scrollHeight;
}

function send() {
  const input = document.getElementById("msg");
  const text = input.value.trim();
  if (!text) return;

  add(`💬 ${text}`, "user");
  input.value = "";

  const typing = document.createElement("div");
  typing.className = "bot typing";
  typing.innerText = "🩺 MedCheck AI is typing...";
  chat.appendChild(typing);
  chat.scrollTop = chat.scrollHeight;

  fetch("/api/message", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message: text})
  })
  .then(r => r.json())
  .then(d => {
    typing.remove();
    add(`🩺 ${d.reply}`, "bot");
  })
  .catch(() => {
    typing.remove();
    add("⚠️ Server error. Please try again.", "bot");
  });
}
