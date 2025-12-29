const startBtn = document.getElementById('startBtn');
const chatContainer = document.getElementById('chatContainer');
const chatMessages = document.getElementById('chatMessages');
const chatInput = document.getElementById('chatInput');
const sendBtn = document.getElementById('sendBtn');

// Show chat with fade effect
startBtn.addEventListener('click', () => {
    startBtn.style.display = 'none';
    chatContainer.style.display = 'flex';
    setTimeout(() => {
        chatContainer.style.opacity = '1';
        appendBotMessage("Hello! I'm MedCheck AI 🤖. I can help with medicine info and health advice.");
    }, 50);
});

// Predefined bot responses
const botResponses = {
    hi: "Hello! How can I assist you with your health today?",
    hello: "Hi there! Need guidance on medications or health?",
    "how are you": "I'm ready to help you with medicine info and healthcare queries!",
    bye: "Goodbye! Stay healthy and safe!",
    default: "Sorry, I didn't understand that. Try asking about medicines or health tips."
};

function getBotResponse(message) {
    message = message.toLowerCase();
    for (let key in botResponses) {
        if (message.includes(key)) return botResponses[key];
    }
    return botResponses['default'];
}

// Append user or bot message
function appendMessage(text, className) {
    const msg = document.createElement('div');
    msg.classList.add('message', className);
    msg.innerText = text;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Append bot message with typing indicator
function appendBotMessage(text) {
    const typing = document.createElement('div');
    typing.id = 'typingIndicator';
    typing.innerText = "MedCheck AI is typing...";
    chatMessages.appendChild(typing);
    chatMessages.scrollTop = chatMessages.scrollHeight;

    setTimeout(() => {
        chatMessages.removeChild(typing);
        appendMessage(text, 'botMsg');
    }, 800); // typing delay
}

// Send message function
function sendMessage() {
    const message = chatInput.value.trim();
    if (!message) return;
    appendMessage(message, 'userMsg');
    chatInput.value = '';

    const botReply = getBotResponse(message);

    // If using Flask backend, replace above with fetch:
    /*
    fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message })
    })
    .then(res => res.json())
    .then(data => appendBotMessage(data.reply));
    */
    
    appendBotMessage(botReply);
}

// Event listeners
sendBtn.addEventListener('click', sendMessage);
chatInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});


