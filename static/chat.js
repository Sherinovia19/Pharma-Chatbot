const chat = document.getElementById("chat");

function add(text, cls) {
  const d = document.createElement("div");
  d.className = cls;
  d.innerText = text;
  chat.appendChild(d);
  chat.scrollTop = chat.scrollHeight;
}

function send() {
  const input = document.getElementById("msg");
  const text = input.value.trim();
  if (!text) return;

  add(text, "user");
  input.value = "";

  const typing = document.createElement("div");
  typing.className = "bot";
  typing.innerText = "🩺 MedCheck AI is typing...";
  chat.appendChild(typing);

  fetch("/api/message", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message: text })
  })
  .then(res => res.json())
  .then(data => {
    typing.remove();
    add(data.reply, "bot");
  })
  .catch(() => {
    typing.remove();
    add("⚠️ Server error", "bot");
  });
}
