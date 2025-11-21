async function sendQuery() {
  const inputEl = document.getElementById("userInput");
  const input = inputEl.value;
  const chat = document.getElementById("chat");

  if (!input.trim()) return;

  chat.innerHTML += `
    <div class="message user">${escapeHtml(input)}</div>
  `;

  let typingBubble = document.createElement("div");
  typingBubble.className = "message bot typing";
  typingBubble.textContent = "WiseChicken is thinking...";
  chat.appendChild(typingBubble);

  chat.scrollTop = chat.scrollHeight;

  // disable input while waiting
  const sendBtn = document.getElementById("sendBtn");
  sendBtn.disabled = true;
  inputEl.disabled = true;

  try {
    const response = await fetch("http://127.0.0.1:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: input })
    });

    const data = await response.json();

    if (typingBubble.parentElement) chat.removeChild(typingBubble);

    chat.innerHTML += `
      <div class="message bot">${escapeHtml(data.answer || "No answer")}</div>
    `;
  } 
  catch (error) {
    if (typingBubble.parentElement) chat.removeChild(typingBubble);
    chat.innerHTML += `
      <div class="message bot" style="color:red;">Error: ${escapeHtml(String(error))}</div>
    `;
  }

  inputEl.value = "";
  sendBtn.disabled = false;
  inputEl.disabled = false;
  inputEl.focus();
  chat.scrollTop = chat.scrollHeight;
}

// small helper to avoid injecting raw HTML
function escapeHtml(text) {
  return String(text)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("userInput");
  const sendBtn = document.getElementById("sendBtn");
  const themeToggle = document.getElementById("themeToggle");

  // send on Enter (Shift+Enter for newline)
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendQuery();
    }
  });

  sendBtn.addEventListener("click", sendQuery);

  // theme toggle with persistence
  const saved = localStorage.getItem("wc_theme");
  if (saved === "dark") document.body.classList.add("dark");

  function updateThemeButton() {
    themeToggle.textContent = document.body.classList.contains("dark") ? "☀️" : "🌙";
  }

  themeToggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");
    const isDark = document.body.classList.contains("dark");
    localStorage.setItem("wc_theme", isDark ? "dark" : "light");
    updateThemeButton();
  });

  updateThemeButton();
  input.focus();
});