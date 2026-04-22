from __future__ import annotations

import streamlit as st

from services.css_demo import render_css_demo
from ui import apply_theme, heading, set_page


set_page("Test Masonry", "🧪")
apply_theme()
heading(
    "css expansion",
    "Masonry / Grid Lanes",
    "A signal wall layout experiment with CSS columns fallback and future grid-lanes hook.",
)

render_css_demo(
    r"""
<style>
.masonry {
  columns: 3 220px;
  column-gap: 14px;
}
.masonry-card {
  break-inside: avoid;
  margin: 0 0 14px;
  border: 1px solid var(--line-soft);
  border-radius: 8px;
  background: var(--panel);
  padding: 14px;
}
@supports (grid-template-rows: masonry) {
  .masonry {
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
    grid-template-rows: masonry;
  }
  .masonry-card {
    margin: 0;
  }
}
</style>
<main class="demo-shell">
  <div>
    <div class="kicker">native packed layout</div>
    <h1>Signal wall</h1>
    <p>Useful for uneven audience fragments, artifacts, and proposals.</p>
  </div>
  <section class="masonry">
    <article class="masonry-card"><span class="tag">need</span><p>We need a quiet space after the performance.</p></article>
    <article class="masonry-card"><span class="tag">offer</span><p>I can help with sound check and teardown. I have a small mixer and two mics.</p></article>
    <article class="masonry-card"><span class="tag">question</span><p>Who decides the order of performances?</p></article>
    <article class="masonry-card"><span class="tag">signal</span><p>The room feels ready but not aligned.</p></article>
    <article class="masonry-card"><span class="tag">proposal</span><p>Move the decision block before the open mic so late arrivals can still join the performance.</p></article>
    <article class="masonry-card"><span class="tag">friction</span><p>The entrance flow is unclear.</p></article>
  </section>
</main>
""",
    height=660,
)
