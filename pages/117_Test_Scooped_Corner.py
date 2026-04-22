from __future__ import annotations

from pathlib import Path

import streamlit as st

from services.visual_primitives import apply_visual_lab_theme
from ui import set_page


ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "assets" / "effects" / "scooped_corner.css"


def _scooped_html() -> str:
    css = CSS_PATH.read_text(encoding="utf-8")
    return f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>{css}</style>
</head>
<body>
  <main class="content-container" data-component-id="H-SCOOP-PLANE-001">
    <section class="content" data-component-id="H-SCOOP-CONTENT-001">
      <p class="kicker">CSS expansion / corner geometry</p>
      <h1>Scooped field note</h1>
      <p class="lead" data-component-id="H-SCOOP-LEAD-001">
        A test for <code>corner-shape</code>, <code>color-mix()</code>, container queries,
        and a triangular structural mark built with modern <code>clip-path</code>.
      </p>
      <p>
        This variant turns the playful CodePen gesture into a printed interruption:
        pale matter enters the black field, one corner is cut into an instrument,
        and the text behaves like a programme note rather than a promotional card.
      </p>
      <p>
        Use it for declarations, principles, thresholds, or any moment where the
        interface should feel like paper placed on a dark stage. Unsupported browsers
        fall back to standard rounded corners and a polygon triangle.
      </p>
      <div class="tech-list" aria-label="Tested CSS features" data-component-id="H-SCOOP-TECH-CHIPS-001">
        <span>corner-shape</span>
        <span>container queries</span>
        <span>color-mix</span>
        <span>clip-path shape</span>
      </div>
    </section>
    <aside class="shape-column" aria-hidden="true" data-component-id="H-SCOOP-TRIANGLE-001">
      <div class="shape"></div>
    </aside>
    <div class="index-mark">117</div>
  </main>
</body>
</html>
"""


set_page("Test Scooped Corner", "🧪")
apply_visual_lab_theme("d")

st.markdown("<div class='vl-component-id'>H-SCOOP-CORNER-001</div>", unsafe_allow_html=True)
st.markdown("<div class='vl-section-label'>visual test h / scooped corner</div>", unsafe_allow_html=True)
st.markdown("<h1 class='vl-hero-title serif'>Scooped geometry as editorial plane</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='vl-subtitle'>A controlled adaptation of the corner-shape demo using MONX26 tokens and one pale interruption.</p>",
    unsafe_allow_html=True,
)

st.iframe(_scooped_html(), height=780)
