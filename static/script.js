const chatBox = document.getElementById("chat-box");
const form = document.getElementById("chat-form");
const input = document.getElementById("user-input");

let typingBubble = null;

function addBubble(text, sender, isTyping = false) {
  const bubble = document.createElement("div");
  bubble.className = `message ${sender === "user" ? "user-msg" : "bot-msg"}`;

  if (isTyping) {
    bubble.classList.add("typing");
    bubble.innerHTML = `
      <div class="typing-dots">
        <span class="dot"></span>
        <span class="dot"></span>
        <span class="dot"></span>
      </div>`;
    typingBubble = bubble;
  } else {
    bubble.innerHTML = `<div class="markdown-body">${marked.parse(text)}</div>`;
  }

  chatBox.appendChild(bubble);
  chatBox.scrollTop = chatBox.scrollHeight;
}

function removeTyping() {
  if (typingBubble && typingBubble.parentElement) {
    typingBubble.remove();
    typingBubble = null;
  }
}

function fadeOutWelcome() {
  const welcome = document.getElementById("welcome-message");
  if (welcome) {
    welcome.style.transition = "opacity 0.4s ease, transform 0.4s ease";
    welcome.style.opacity = "0";
    welcome.style.transform = "translateY(-10px)";
    setTimeout(() => welcome.remove(), 400); // Fully remove after fade
  }
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const userMessage = input.value.trim();
  if (!userMessage) return;

  fadeOutWelcome(); // ✨ Smoothly hide welcome message

  addBubble(userMessage, "user");
  input.value = "";

  addBubble("", "bot", true); // Show typing dots

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: userMessage })
    });

    const data = await response.json();
    removeTyping();
    addBubble(data.response || "⚠️ No response.", "bot");
  } catch (err) {
    console.error("❌ Chat error:", err);
    removeTyping();
    addBubble("⚠️ Something went wrong. Try again later.", "bot");
  }
});
