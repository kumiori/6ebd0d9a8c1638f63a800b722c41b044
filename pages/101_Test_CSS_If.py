from __future__ import annotations

import streamlit as st

from services.css_demo import render_css_demo
from ui import apply_theme, heading, set_page


set_page("Test CSS If", "🧪")
apply_theme()
heading(
    "css expansion",
    "Native CSS if",
    "Experimental component logic direction, shown with practical style-query fallback.",
)

render_css_demo(
    r"""
<style>
.variant-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 14px;
}
.variant {
  --variant: neutral;
  container-name: variant;
  container-type: normal;
  border: 1px solid var(--line-soft);
  border-radius: 8px;
  background: var(--panel);
  padding: 16px;
}
.variant[data-variant="primary"] {
  --variant: primary;
  border-color: var(--pink);
}
.variant[data-variant="warning"] {
  --variant: warning;
  border-color: var(--orange);
}
@supports (background: if(style(--variant: primary): red; else: blue)) {
  .variant {
    background: if(style(--variant: primary): #f05aa6; else: #111116);
  }
}
</style>
<main class="demo-shell">
  <div>
    <div class="kicker">experimental css logic</div>
    <h1>Component state in CSS</h1>
    <p>This is not production-ready. The useful idea is local component logic via style queries and future CSS conditionals.</p>
  </div>
  <section class="variant-grid">
    <article class="variant" data-variant="neutral"><h2>Neutral</h2><p>Fallback uses attributes and custom properties.</p></article>
    <article class="variant" data-variant="primary"><h2>Primary</h2><p>Future CSS if() could choose values from component state.</p></article>
    <article class="variant" data-variant="warning"><h2>Warning</h2><p>Useful for decision states and facilitation flags.</p></article>
  </section>
</main>
""",
    height=600,
)
