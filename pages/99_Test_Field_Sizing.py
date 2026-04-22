from __future__ import annotations

import streamlit as st

from services.css_demo import render_css_demo
from ui import apply_theme, heading, set_page


set_page("Test Field Sizing", "🧪")
apply_theme()
heading(
    "css expansion",
    "Field sizing",
    "Auto-growing text inputs for proposals, notes, and audience signals.",
)

render_css_demo(
    r"""
<style>
.grow-field {
  field-sizing: content;
  min-height: 8rem;
  max-height: 30rem;
  overflow-y: auto;
}
</style>
<main class="demo-shell">
  <div>
    <div class="kicker">native content sizing</div>
    <h1>Textarea grows with the thought</h1>
    <p>Type multiple lines. Supported browsers grow the field without JavaScript.</p>
  </div>
  <section class="panel grid">
    <label>Proposal body
      <textarea class="grow-field">Start with a compact note, then keep typing...</textarea>
    </label>
    <p class="note">Fallback: normal textarea resize behavior.</p>
  </section>
</main>
""",
    height=560,
)
