from __future__ import annotations

import streamlit as st

from services.visual_primitives import (
    apply_visual_lab_theme,
    divider,
    form_note,
    hero_title,
    section_label,
    soft_panel,
)
from ui import set_page


set_page("Visual Test Cue Sheet", "🧪")
apply_visual_lab_theme("c")

section_label("visual test c / backstage cue sheet", "C-SECTION-001")
hero_title(
    "Backbone for the room",
    "A quieter operator-facing style: narrow column, cue sheet panels, neutral borders, and actions kept grounded.",
    "C-HERO-001",
)

main, aside = st.columns([1.1, 0.9], gap="large")

with main:
    section_label("access without spectacle", "C-ACCESS-LABEL-001")
    soft_panel(
        "Embedded access panel",
        "This tests replacing the dominant modal with a page-level panel. The panel is top-aligned, matte, and operational.",
        "C-PANEL-ACCESS-001",
        variant="sheet",
    )
    with st.form("visual_cue_access"):
        form_note("The key flow should feel like entering a score, not a checkout funnel.", "C-FORM-NOTE-001")
        st.text_input("Name or handle", placeholder="anonymous")
        st.text_input("Intention", placeholder="one short line")
        st.text_input("Email reminder", placeholder="optional")
        st.form_submit_button("Create access key", type="primary")

with aside:
    soft_panel(
        "Operator cues",
        "Use this side as a live checklist: session state, room state, next action, unresolved objections.",
        "C-PANEL-CUES-001",
        variant="print",
    )
    divider()
    st.checkbox("Session open")
    st.checkbox("Audience entry visible")
    st.checkbox("Decision threshold named")
    st.checkbox("Facilitator assigned")

divider()

section_label("coordination modules", "C-MODULE-LABEL-001")
cards = st.columns(3, gap="medium")
with cards[0]:
    soft_panel("Need", "A short inscription from the room.", "C-CARD-NEED-001", variant="sheet")
with cards[1]:
    soft_panel("Offer", "A resource, person, space, or tool.", "C-CARD-OFFER-001", variant="sheet")
with cards[2]:
    soft_panel("Block", "A concrete objection requiring movement.", "C-CARD-BLOCK-001", variant="sheet")
