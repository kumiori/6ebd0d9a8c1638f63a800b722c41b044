from __future__ import annotations

import streamlit as st

from services.visual_primitives import (
    apply_visual_lab_theme,
    component_id,
    form_note,
    section_label,
    soft_panel,
)
from ui import set_page


set_page("Visual Test Accent Event", "🧪")
apply_visual_lab_theme("e")

section_label("visual test e / accent as event", "E-SECTION-001")
component_id("E-TITLE-STRIKE-001")
st.markdown(
    "<h1 class='vl-title-strike'>Consent is an event</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p class='vl-subtitle'>Pink appears only where action happens: one title strike, one threshold line, active controls.</p>",
    unsafe_allow_html=True,
)

left, right = st.columns([1.35, 0.65], gap="large")
with left:
    section_label("decision movement", "E-FORM-LABEL-001")
    with st.form("visual_accent_event"):
        form_note("No pink borders. The accent arrives at the threshold before action.", "E-FORM-NOTE-001")
        st.text_input("Proposal", placeholder="Name the action")
        st.text_area("Objection or release", placeholder="Write the condition.")
        st.slider("Threshold pressure", 0, 10, 6)
        component_id("E-ACCENT-LINE-001")
        st.markdown("<div class='vl-accent-line'></div>", unsafe_allow_html=True)
        st.form_submit_button("Commit movement", type="primary")

with right:
    soft_panel(
        "Instruction",
        "Treat pink as decision energy. If nothing is happening, there is no pink.",
        "E-PANEL-INSTRUCTION-001",
        variant="sheet",
    )
