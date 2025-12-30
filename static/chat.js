const chat = document.getElementById("chat");
const input = document.getElementById("msg");

function add(text, cls) {
  const d = document.createElement("div");
  d.className = cls;
  d.innerHTML = text;
  chat.appendChild(d);
  chat.scrollTop = chat.scrollHeight;
}

function send() {
  const text = input.value.trim();
  if (!text) return;

  add(text, "user");
  input.value = "";

  const typing = document.createElement("div");
  typing.className = "bot";
  typing.innerText = "🩺 Processing...";
  chat.appendChild(typing);

  fetch("/api/message", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message: text})
  })
  .then(r => r.json())
  .then(d => {
    typing.remove();
    add(d.reply, "bot");
  });
}

input.addEventListener("keydown", e => {
  if (e.key === "Enter") send();
});
