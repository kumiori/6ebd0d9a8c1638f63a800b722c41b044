from __future__ import annotations

import streamlit as st

from services.css_demo import render_css_demo
from ui import apply_theme, heading, set_page


set_page("Test Anchor Positioning", "🧪")
apply_theme()
heading(
    "css expansion",
    "Anchor positioning",
    "Floating notes anchored to a trigger, with CSS feature detection and a fallback path.",
)

render_css_demo(
    r"""
<style>
.anchor-stage {
  position: relative;
  min-height: 360px;
}
.decision-node {
  anchor-name: --decision-node;
  margin: 110px auto 0;
  width: min(320px, 100%);
  border: 2px solid var(--orange);
  border-radius: 8px;
  background: #080808;
  padding: 18px;
}
.anchored-note {
  position: absolute;
  left: calc(50% + 165px);
  top: 92px;
  width: min(260px, 90%);
  border: 1px solid var(--pink);
  border-radius: 8px;
  background: var(--panel);
  padding: 14px;
}
@supports (position-anchor: --decision-node) {
  .anchored-note {
    position-anchor: --decision-node;
    left: anchor(right);
    top: anchor(top);
    margin-left: 18px;
  }
}
</style>
<main class="demo-shell">
  <div>
    <div class="kicker">native layout primitive</div>
    <h1>Attached context</h1>
    <p>For proposal cards, moderation controls, and help text that should stay attached to the relevant object.</p>
  </div>
  <section class="panel anchor-stage">
    <article class="decision-node">
      <span class="tag">proposal</span>
      <h2>Open the courtyard after midnight</h2>
      <p>Needs facilitation context, risks, and current constraints.</p>
    </article>
    <aside class="anchored-note">
      <strong>Facilitator note</strong>
      <p>This note is positioned from the proposal anchor when supported. Otherwise it falls back to absolute positioning.</p>
    </aside>
  </section>
</main>
""",
    height=620,
)
