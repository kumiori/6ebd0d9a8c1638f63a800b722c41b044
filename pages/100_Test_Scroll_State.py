from __future__ import annotations

import streamlit as st

from services.css_demo import render_css_demo
from ui import apply_theme, heading, set_page


set_page("Test Scroll State", "🧪")
apply_theme()
heading(
    "css expansion",
    "Scroll-state queries",
    "CSS reacting to stuck, snapped, and scrollable state without observers.",
)

render_css_demo(
    r"""
<style>
.scrollbox {
  height: 460px;
  overflow: auto;
  border: 1px solid var(--line-soft);
  border-radius: 8px;
}
.sticky {
  container-type: scroll-state;
  position: sticky;
  top: 0;
  z-index: 2;
  background: #090909;
  border-bottom: 1px solid var(--line-soft);
  padding: 12px;
}
@container scroll-state(stuck: top) {
  .sticky-inner {
    box-shadow: 0 12px 22px rgba(240, 90, 166, 0.3);
  }
}
.snap-row {
  display: flex;
  gap: 12px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  padding: 14px;
}
.snap-card {
  container-type: scroll-state;
  flex: 0 0 72%;
  min-height: 170px;
  scroll-snap-align: center;
  border: 1px solid var(--line);
  border-radius: 8px;
  padding: 18px;
}
@container not scroll-state(snapped: x) {
  .snap-content {
    opacity: 0.42;
    transform: scale(0.96);
  }
}
.spacer {
  min-height: 520px;
  padding: 20px;
}
</style>
<main class="demo-shell">
  <div>
    <div class="kicker">scroll-state container queries</div>
    <h1>Sticky and snapped awareness</h1>
    <p>Experimental: Chrome supports useful parts; other browsers fall back to static styling.</p>
  </div>
  <section class="panel scrollbox">
    <header class="sticky"><div class="sticky-inner">Sticky facilitation header</div></header>
    <div class="snap-row">
      <article class="snap-card"><div class="snap-content"><h2>Signal</h2><p>Current snapped card stays prominent.</p></div></article>
      <article class="snap-card"><div class="snap-content"><h2>Proposal</h2><p>Non-snapped items can fade without JavaScript.</p></div></article>
      <article class="snap-card"><div class="snap-content"><h2>Decision</h2><p>Scroll horizontally to test snapped state.</p></div></article>
    </div>
    <div class="spacer">
      <p>Scroll down to test stuck state. Scroll sideways to test snapped state.</p>
    </div>
  </section>
</main>
""",
    height=720,
)
