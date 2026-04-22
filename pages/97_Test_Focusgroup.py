from __future__ import annotations

import streamlit as st

from services.css_demo import render_css_demo
from ui import apply_theme, heading, set_page


set_page("Test Focusgroup", "🧪")
apply_theme()
heading(
    "css expansion",
    "Focusgroup proposal",
    "Future declarative arrow-key navigation, with a tiny fallback for today.",
)

render_css_demo(
    r"""
<style>
.toolbar {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}
.toolbar button:focus-visible {
  outline: 3px solid var(--orange);
  outline-offset: 3px;
}
</style>
<main class="demo-shell">
  <div>
    <div class="kicker">future html primitive</div>
    <h1>Arrow-key toolbar</h1>
    <p>The markup includes <code>focusgroup</code>. The fallback below makes it usable in current browsers.</p>
  </div>
  <section class="panel">
    <div class="toolbar" role="toolbar" focusgroup="inline wrap" aria-label="Decision tools">
      <button>Keep</button>
      <button>Drop</button>
      <button>Amend</button>
      <button>Delegate</button>
    </div>
  </section>
</main>
<script>
const buttons = [...document.querySelectorAll(".toolbar button")];
buttons.forEach((button, index) => {
  button.tabIndex = index === 0 ? 0 : -1;
  button.addEventListener("keydown", (event) => {
    if (!["ArrowRight", "ArrowLeft"].includes(event.key)) return;
    event.preventDefault();
    const dir = event.key === "ArrowRight" ? 1 : -1;
    const next = (index + dir + buttons.length) % buttons.length;
    buttons[index].tabIndex = -1;
    buttons[next].tabIndex = 0;
    buttons[next].focus();
  });
});
</script>
""",
    height=520,
)
