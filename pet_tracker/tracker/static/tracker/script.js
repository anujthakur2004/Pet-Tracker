// Default datetime
(function() {
  const dt = document.querySelector('input[name="datetime"]');
  if (dt && !dt.value) {
    const now = new Date();
    now.setSeconds(0, 0);
    const pad = n => String(n).padStart(2, "0");
    dt.value = `${now.getFullYear()}-${pad(now.getMonth()+1)}-${pad(now.getDate())}T${pad(now.getHours())}:${pad(now.getMinutes())}`;
  }
})();

// Reminder at 18:00 if no walk
(function() {
  const reminder = document.getElementById("reminder");
  const text = document.body.innerText;
  const hasWalk = text.includes("walk");
  function check() {
    const now = new Date();
    if (now.getHours() >= 18 && !hasWalk) {
      reminder.classList.remove("hidden");
    } else {
      reminder.classList.add("hidden");
    }
  }
  check();
  setInterval(check, 5 * 60 * 1000);
})();

// Chatbot
(function() {
  const form = document.getElementById("chatForm");
  const input = document.getElementById("chatInput");
  const log = document.getElementById("chatLog");
  if (!form) return;

  function addMsg(role, text) {
    const div = document.createElement("div");
    div.className = "msg " + role;
    div.textContent = text;
    log.appendChild(div);
    log.scrollTop = log.scrollHeight;
  }

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const msg = input.value.trim();
    if (!msg) return;

    addMsg("user", msg);
    input.value = "";
    addMsg("bot", "Thinking...");

    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({message: msg})
      });
      const data = await res.json();
      log.lastChild.textContent = data.ok ? data.reply : (data.error || "Error");
    } catch {
      log.lastChild.textContent = "Network error.";
    }
  });
})();

// Animate summary bars
(function animateBars() {
  const fills = document.querySelectorAll(".bar-fill");
  fills.forEach(el => {
    const v = Number(el.dataset.value || 0);
    // Map values to percentages:
    // Walk: assume max 120 min, Meals/Meds: max 5 each
    let max = 100;
    if (el.dataset.value.includes("min")) { // fallback check
      max = 120;
    }
    const width = Math.min((v / (max || 1)) * 100, 100);
    el.style.width = width + "%";
  });
})();
