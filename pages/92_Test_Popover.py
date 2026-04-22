from __future__ import annotations

import streamlit as st

from services.css_demo import render_css_demo
from ui import apply_theme, heading, set_page


set_page("Test Popover", "🧪")
apply_theme()
heading(
    "css expansion",
    "Popover API",
    "Native light-dismiss overlays for help, context, menus, and facilitation callouts.",
)

render_css_demo(
    r"""
<style>
[popover] {
  max-width: 340px;
  border: 1px solid var(--pink);
  border-radius: 8px;
  background: #070707;
  color: var(--ink);
  padding: 18px;
  box-shadow: 0 18px 70px rgba(0, 0, 0, 0.65);
}
[popover]::backdrop {
  background: rgba(0, 0, 0, 0.35);
}
</style>
<main class="demo-shell">
  <div>
    <div class="kicker">native non-modal overlay</div>
    <h1>Light dismiss context</h1>
    <p>Click the buttons. Escape and outside-click close the popovers without custom JavaScript.</p>
  </div>
  <section class="panel row">
    <button popovertarget="proposal-help">What does consent mean?</button>
    <button popovertarget="visibility-help" class="secondary">Visibility rules</button>
    <div id="proposal-help" popover>
      <h2>Consent</h2>
      <p>Consent means no unresolved objection remains strong enough to block action.</p>
    </div>
    <div id="visibility-help" popover>
      <h2>Visibility</h2>
      <p>Public signals can be shown to the room. Facilitation notes remain available to operators.</p>
    </div>
  </section>
</main>
""",
    height=520,
)
