from __future__ import annotations

import streamlit as st

from services.visual_primitives import apply_visual_lab_theme, component_id, hero_title, section_label
from ui import set_page


set_page("Flow Backstage Control", "🧪")
apply_visual_lab_theme("d")

section_label("flow 3 / backstage to control", "FLOW-BACKSTAGE-CONTROL-001")
hero_title(
    "Operate the system",
    "A sequence of states: narrow silent layout, checklist carrier, decision threshold, then assignment action.",
    "FLOW-BACKSTAGE-HERO-001",
)

st.markdown(
    """
<section class="vl-flow-sequence layout-narrow">
  <article class="vl-role-module silent" data-role="SILENT" data-component-id="FLOW-BACKSTAGE-SILENT-001">
    <span class="vl-role-tag">SILENT</span>
    <h2 class="vl-flow-title">Backstage is narrow on purpose.</h2>
    <p class="vl-flow-copy">Control screens should feel operational, not public-facing.</p>
  </article>
  <article class="vl-provocation" data-role="INTERRUPTION" data-component-id="FLOW-BACKSTAGE-PROVOCATION-001">
    <span>DECISION</span>
    <span class="accent-strike">THR-</span>
  </article>
</section>
""",
    unsafe_allow_html=True,
)

left, right = st.columns([0.78, 1.22], gap="large")
with left:
    component_id("FLOW-BACKSTAGE-CHECKLIST-001")
    st.markdown(
        """
<section class="vl-role-module carrier" data-role="CARRIER" data-component-id="FLOW-BACKSTAGE-CARRIER-CHECKLIST-001">
  <span class="vl-role-tag">CARRIER</span>
  <h2 class="vl-flow-title">Cue sheet</h2>
  <ul class="vl-checklist">
    <li>Room open</li>
    <li>Facilitator assigned</li>
    <li>Decision window named</li>
    <li>Public trace prepared</li>
  </ul>
</section>
""",
        unsafe_allow_html=True,
    )

with right:
    st.markdown(
        """
<section class="vl-role-module interruption" data-role="INTERRUPTION" data-component-id="FLOW-BACKSTAGE-INTERRUPTION-001">
  <span class="vl-role-tag">INTERRUPTION</span>
  <h2 class="vl-flow-title">Decision threshold</h2>
  <p class="vl-flow-copy">If the threshold is crossed, the system stops collecting and starts assigning.</p>
</section>
""",
        unsafe_allow_html=True,
    )
    component_id("FLOW-BACKSTAGE-ACTION-001")
    st.markdown("<div class='vl-dominance-action' data-role='ACTION' data-component-id='FLOW-BACKSTAGE-DOMINANCE-ACTION-001'>ASSIGN</div>", unsafe_allow_html=True)
    with st.form("flow_backstage_control"):
        st.toggle("Open assignment mode", value=True)
        st.selectbox("Assign next movement to", ["facilitation", "documentation", "technical", "hosting"])
        st.slider("Decision pressure", 0, 10, 7)
        st.form_submit_button("Assign", type="primary")
