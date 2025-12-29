const chatBox = document.getElementById("chat-box");
const input = document.getElementById("message-input");

function appendMessage(text, sender){
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", sender);
  msgDiv.innerText = text;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function sendMessage(){
  const msg = input.value.trim();
  if(!msg) return;
  appendMessage(msg,"user");
  input.value="";
  fetch("/api/message",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({message:msg})
  }).then(res=>res.json())
    .then(data=>appendMessage(data.reply,"bot"))
    .catch(()=>appendMessage("⚠️ Bot encountered an error.","bot"));
}

input.addEventListener("keypress",e=>{if(e.key==="Enter") sendMessage();});
