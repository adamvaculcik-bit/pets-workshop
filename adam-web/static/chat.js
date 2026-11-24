// Mobilní menu
const menuBtn = document.querySelector(".menu-btn");
const menu = document.querySelector(".menu");
menuBtn.addEventListener("click", () => {
  const open = menu.classList.toggle("open");
  menuBtn.setAttribute("aria-expanded", open);
});
menu.addEventListener("click", (e) => {
  if (e.target.tagName === "A") menu.classList.remove("open");
});

// AI chat
const log = document.getElementById("chat-log");
const form = document.getElementById("chat-form");
const input = document.getElementById("chat-input");
const sendBtn = form.querySelector("button");
const history = [];

function addMessage(text, cls) {
  const el = document.createElement("div");
  el.className = "msg " + cls;
  el.textContent = text;
  log.appendChild(el);
  log.scrollTop = log.scrollHeight;
  return el;
}

async function send(text) {
  text = text.trim();
  if (!text || sendBtn.disabled) return;
  addMessage(text, "user");
  history.push({ role: "user", content: text });
  input.value = "";
  input.style.height = "";
  sendBtn.disabled = true;

  const bot = addMessage("", "bot typing");
  let answer = "";
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: history }),
    });
    if (!res.ok || !res.body) throw new Error("HTTP " + res.status);

    const reader = res.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const events = buffer.split("\n\n");
      buffer = events.pop();
      for (const ev of events) {
        if (!ev.startsWith("data: ")) continue;
        const data = JSON.parse(ev.slice(6));
        if (data.text) {
          answer += data.text;
          bot.textContent = answer;
          log.scrollTop = log.scrollHeight;
        } else if (data.error) {
          bot.classList.add("error");
          bot.textContent = data.error;
        }
      }
    }
  } catch (err) {
    bot.classList.add("error");
    bot.textContent = "Spojení se nezdařilo. Zkuste to prosím znovu.";
  } finally {
    bot.classList.remove("typing");
    sendBtn.disabled = false;
    if (answer) {
      history.push({ role: "assistant", content: answer });
    } else {
      history.pop(); // neúspěšný dotaz z historie odebereme
    }
  }
}

form.addEventListener("submit", (e) => {
  e.preventDefault();
  send(input.value);
});
input.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    send(input.value);
  }
});
input.addEventListener("input", () => {
  input.style.height = "auto";
  input.style.height = input.scrollHeight + "px";
});
document.querySelectorAll(".chip").forEach((chip) =>
  chip.addEventListener("click", () => {
    document.getElementById("asistent").scrollIntoView();
    send(chip.textContent);
  })
);
