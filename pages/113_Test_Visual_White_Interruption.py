from __future__ import annotations

import streamlit as st

from services.visual_primitives import (
    apply_visual_lab_theme,
    component_id,
    divider,
    hero_title,
    section_label,
    soft_panel,
)
from ui import set_page


set_page("Visual Test White Interruption", "🧪")
apply_visual_lab_theme("d")

section_label("visual test d / white interruption", "D-SECTION-001")
hero_title(
    "A printed page enters the dark",
    "One pale plane interrupts the field. Everything else stays matte, dark, and structural.",
    "D-HERO-001",
)

left, right = st.columns([0.62, 1.38], gap="large")
with left:
    soft_panel(
        "Before the rupture",
        "Signals remain quiet until a threshold has to be named.",
        "D-PANEL-DARK-001",
        variant="sheet",
    )
with right:
    component_id("D-INTERRUPTION-001")
    st.markdown(
        """
<section class="vl-block-interruption">
  <h2>Decision threshold</h2>
  <p>A decision is not a mood. It is the moment where an objection either transforms the proposal or releases action.</p>
</section>
""",
        unsafe_allow_html=True,
    )

divider()
cols = st.columns([1.2, 0.8], gap="large")
with cols[0]:
    section_label("field notes", "D-NOTES-LABEL-001")
    st.text_area("What must be clarified before action?", placeholder="Name the unresolved condition.")
with cols[1]:
    soft_panel(
        "Rule",
        "Only one pale block appears on this screen. It is the rupture.",
        "D-PANEL-RULE-001",
    )
