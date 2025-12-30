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

  // Use timeout to prevent long hangs
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 5000);

  fetch("/api/message", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({message: text}),
    signal: controller.signal
  })
  .then(r => r.json())
  .then(d => {
    clearTimeout(timeout);
    typing.remove();
    add(d.reply, "bot");
  })
  .catch(() => {
    typing.remove();
    add("⚠️ Request timed out or server error.", "bot");
  });
}

// Enter key sends message only if input is not empty
input.addEventListener("keydown", e => {
  if (e.key === "Enter" && input.value.trim() !== "") send();
});
