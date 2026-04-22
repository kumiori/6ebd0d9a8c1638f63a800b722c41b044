from __future__ import annotations

import streamlit as st

from services.css_demo import render_css_demo
from ui import apply_theme, heading, set_page


set_page("Test Select Customization", "🧪")
apply_theme()
heading(
    "css expansion",
    "Customizable select",
    "A forward-looking native select styling experiment with graceful fallback.",
)

render_css_demo(
    r"""
<style>
.native-select {
  max-width: 420px;
}
@supports (appearance: base-select) {
  .native-select {
    appearance: base-select;
  }
  .native-select::picker(select) {
    border: 1px solid var(--pink);
    border-radius: 8px;
    background: #080808;
    color: var(--ink);
  }
  .native-select option {
    padding: 12px;
  }
}
</style>
<main class="demo-shell">
  <div>
    <div class="kicker">native form control</div>
    <h1>Select without rebuilding select</h1>
    <p>This is mostly future-facing, but the fallback is still a normal accessible select.</p>
  </div>
  <section class="panel grid">
    <label>Proposal status
      <select class="native-select">
        <option>New signal</option>
        <option>Under discussion</option>
        <option>Needs amendment</option>
        <option>Consent reached</option>
        <option>Blocked</option>
      </select>
    </label>
    <p class="note">If your browser supports customizable selects, the picker itself will follow the app skin.</p>
  </section>
</main>
""",
    height=520,
)
