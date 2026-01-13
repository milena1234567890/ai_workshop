function sendMessage() {
    const input = document.getElementById("userInput");
    const message = input.value.trim();
    if (!message) return;

    const chatMessages = document.getElementById("chatMessages");

    // User message
    const userDiv = document.createElement("div");
    userDiv.className = "user-message";
    userDiv.textContent = message;
    chatMessages.appendChild(userDiv);

    input.value = "";

    // Send to backend
    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        const botDiv = document.createElement("div");
        botDiv.className = "bot-message";
        botDiv.textContent = data.reply;
        chatMessages.appendChild(botDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });
}
