from __future__ import annotations

import streamlit as st

from services.visual_primitives import (
    apply_visual_lab_theme,
    component_id,
    divider,
    form_note,
    hero_title,
    section_label,
    soft_panel,
    token_strip,
)
from ui import set_page


set_page("Visual Test Score", "🧪")
apply_visual_lab_theme("b")

section_label("visual test b / score field", "B-SECTION-001")
hero_title(
    "Lines cross before decisions settle",
    "A more poster-adjacent composition: serif display appears once, structural lines do the work, and controls remain quiet.",
    "B-HERO-001",
    serif=True,
)

top = st.columns([1.35, 0.65], gap="large")
with top[0]:
    soft_panel(
        "Field state",
        "The interface behaves like a score: each contribution becomes a mark, each decision a shift in the composition.",
        "B-PANEL-FIELD-001",
        variant="score",
    )
with top[1]:
    soft_panel(
        "Live",
        "25 avril 2026. Porte 9. Signals enter before the room resolves.",
        "B-PANEL-LIVE-001",
        variant="sheet",
    )

divider()

section_label("decision score", "B-FORM-LABEL-001")
with st.form("visual_score_decision"):
    form_note("This form tests rhythm: section label, inscription, option, action.", "B-FORM-NOTE-001")
    st.text_input("Proposal title", placeholder="Name the possible action")
    st.text_area("Rationale", placeholder="Context, consequence, objection, threshold.")
    col_a, col_b = st.columns(2)
    with col_a:
        st.selectbox("Movement", ["open", "amend", "consent", "block", "delegate"])
    with col_b:
        st.selectbox("Visibility", ["public", "facilitation", "private note"])
    st.form_submit_button("Record movement", type="primary")

divider()
component_id("B-CUE-LIST-001")
st.markdown(
    """
<ul class="vl-cue-list">
  <li><strong>Line:</strong> every section is separated by structure, not glow.</li>
  <li><strong>Accent:</strong> pink appears only where the user acts.</li>
  <li><strong>Poster echo:</strong> serif title and geometric scaffolding stay restrained.</li>
</ul>
""",
    unsafe_allow_html=True,
)
token_strip(["knot", "line", "fracture", "threshold", "stage"], "B-TOKENS-001")
