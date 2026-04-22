from __future__ import annotations

import streamlit as st

from services.css_demo import render_css_demo
from ui import apply_theme, heading, set_page


set_page("Test Scroll Animation", "🧪")
apply_theme()
heading(
    "css expansion",
    "Scroll-driven animations",
    "Progressive enhancement for reports, public narratives, and decision timelines.",
)

render_css_demo(
    r"""
<style>
.scroll-demo {
  height: 540px;
  overflow-y: auto;
  scroll-snap-type: y proximity;
}
.reveal-card {
  min-height: 360px;
  display: grid;
  align-content: center;
  border-bottom: 1px solid var(--line-soft);
  animation: reveal linear both;
  animation-timeline: view();
  animation-range: entry 0% cover 38%;
}
@keyframes reveal {
  from { opacity: 0.18; transform: translateY(34px) scale(0.96); }
  to { opacity: 1; transform: translateY(0) scale(1); }
}
@media (prefers-reduced-motion: reduce) {
  .reveal-card { animation: none; }
}
</style>
<main class="demo-shell">
  <div>
    <div class="kicker">compositor-friendly</div>
    <h1>Timeline reveal</h1>
    <p>Scroll the panel. Modern browsers attach the animation to view progress without JS scroll listeners.</p>
  </div>
  <section class="panel scroll-demo">
    <article class="reveal-card"><span class="tag">signal</span><h2>Someone names a need</h2></article>
    <article class="reveal-card"><span class="tag">proposal</span><h2>The room shapes a possible action</h2></article>
    <article class="reveal-card"><span class="tag">decision</span><h2>Consent or objection becomes visible</h2></article>
    <article class="reveal-card"><span class="tag">coordination</span><h2>Work moves to accountable hands</h2></article>
  </section>
</main>
""",
    height=760,
)
