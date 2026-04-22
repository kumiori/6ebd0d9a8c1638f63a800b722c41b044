from __future__ import annotations

import streamlit as st

from services.visual_primitives import (
    apply_visual_lab_theme,
    divider,
    form_note,
    hero_title,
    section_label,
    soft_panel,
    token_strip,
)
from ui import set_page


set_page("Visual Test Editorial", "🧪")
apply_visual_lab_theme("a")

section_label("visual test a / printed programme", "A-SECTION-001")
hero_title(
    "Enter the collective score",
    "An editorial layout: restrained hierarchy, matte panels, asymmetrical composition, and pink reserved for one action.",
    "A-HERO-001",
)

left, right = st.columns([0.78, 1.22], gap="large")
with left:
    soft_panel(
        "Operating principles",
        "Presence first. Signals are recorded as traces, then proposals become decisions through visible movement.",
        "A-PANEL-PRINCIPLES-001",
        variant="print",
    )
    divider()
    token_strip(
        ["presence", "signal", "proposal", "decision", "coordination"],
        "A-TOKENS-001",
    )

with right:
    section_label("signal inscription", "A-FORM-LABEL-001")
    form_note("Short prompts, wide rhythm, no modal dominance.", "A-FORM-NOTE-001")
    with st.form("visual_editorial_signal"):
        st.text_input("Name or handle", placeholder="anonymous")
        st.selectbox("Signal type", ["presence", "proposal", "need", "offer", "friction"])
        st.text_area("Inscription", placeholder="Write the thing that should enter the room.")
        st.slider("Intensity", 0, 10, 4)
        st.form_submit_button("Send signal", type="primary")

divider()

cols = st.columns(3, gap="medium")
with cols[0]:
    soft_panel("Cue", "A compact cue card for a facilitator or performer.", "A-CARD-CUE-001")
with cols[1]:
    soft_panel("Threshold", "A matte container with neutral border, not a shiny card.", "A-CARD-THRESHOLD-001", variant="alt")
with cols[2]:
    soft_panel("Trace", "Small serif moments are used sparingly, not as constant drama.", "A-CARD-TRACE-001")
