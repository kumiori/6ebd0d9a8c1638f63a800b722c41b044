from __future__ import annotations

import streamlit as st

from services.css_demo import render_css_demo
from ui import apply_theme, heading, set_page


set_page("Test View Transitions", "🧪")
apply_theme()
heading(
    "css expansion",
    "View Transitions API",
    "A browser-native route/state transition candidate for custom audience components.",
)

render_css_demo(
    r"""
<style>
::view-transition-old(root),
::view-transition-new(root) {
  animation-duration: 420ms;
}
.state-card {
  min-height: 280px;
  display: grid;
  align-content: center;
  gap: 12px;
}
.state-card[data-state="decision"] {
  background: #d9579f;
  color: #050505;
}
.state-card[data-state="signal"] {
  background: #111116;
}
.state-card[data-state="decision"] * {
  color: #050505;
}
</style>
<main class="demo-shell">
  <div>
    <div class="kicker">same-document transition</div>
    <h1>State morph</h1>
    <p>Click to move between signal and decision. Browsers with View Transitions animate the DOM change.</p>
  </div>
  <section class="panel">
    <article id="card" class="box state-card" data-state="signal">
      <span class="tag">signal</span>
      <h2>A concern enters the room</h2>
      <p>Click the button to transform the state.</p>
    </article>
    <p><button id="toggle">Toggle state</button></p>
  </section>
</main>
<script>
const card = document.getElementById("card");
const toggle = document.getElementById("toggle");
function update() {
  const decision = card.dataset.state !== "decision";
  card.dataset.state = decision ? "decision" : "signal";
  card.innerHTML = decision
    ? "<span class='tag'>decision</span><h2>The room commits</h2><p>Named state changes can become page transitions later.</p>"
    : "<span class='tag'>signal</span><h2>A concern enters the room</h2><p>Click the button to transform the state.</p>";
}
toggle.addEventListener("click", () => {
  if (document.startViewTransition) document.startViewTransition(update);
  else update();
});
</script>
""",
    height=650,
)
