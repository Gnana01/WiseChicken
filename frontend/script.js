async function sendQuery() {
  const input = document.getElementById("userInput").value;
  const chat = document.getElementById("chat");

  if (!input.trim()) return;

  chat.innerHTML += `
    <div class="message user">${input}</div>
  `;

  let typingBubble = document.createElement("div");
  typingBubble.className = "message bot typing";
  typingBubble.textContent = "WiseChicken is thinking...";
  chat.appendChild(typingBubble);

  chat.scrollTop = chat.scrollHeight;

  try {
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: input })
    });

    const data = await response.json();

    chat.removeChild(typingBubble);

    chat.innerHTML += `
      <div class="message bot">${data.answer}</div>
    `;
  } 
  catch (error) {
    chat.removeChild(typingBubble);
    chat.innerHTML += `
      <div class="message bot" style="color:red;">Error: ${error}</div>
    `;
  }

  document.getElementById("userInput").value = "";
  chat.scrollTop = chat.scrollHeight;
}