from __future__ import annotations

import html

import streamlit as st

from services.visual_primitives import apply_visual_lab_theme, component_id, hero_title, section_label
from ui import set_page


set_page("Flow Field Expression", "🧪")
apply_visual_lab_theme("e")

section_label("flow 2 / field to expression", "FLOW-FIELD-EXPRESSION-001")
hero_title(
    "Input leaves a mark",
    "A sequence of states: carrier form, silent labels, action send, then a memory trace.",
    "FLOW-FIELD-HERO-001",
)

left, right = st.columns([1.42, 0.58], gap="large")
with left:
    component_id("FLOW-FIELD-CARRIER-001")
    st.markdown(
        """
<section class="vl-role-module carrier" data-role="CARRIER" data-component-id="FLOW-FIELD-CARRIER-MODULE-001">
  <span class="vl-role-tag">CARRIER</span>
  <h2 class="vl-flow-title">Signal inscription</h2>
  <p class="vl-flow-copy">The form is not CRM. It is a place where a contribution enters the field.</p>
</section>
""",
        unsafe_allow_html=True,
    )
    with st.form("flow_field_expression"):
        st.markdown(
            """
<div class="vl-role-module silent" data-role="SILENT" data-component-id="FLOW-FIELD-SILENT-LABELS-001">
  <span class="vl-role-tag">SILENT</span>
  <p class="vl-flow-copy">Labels stay quiet. They orient, they do not perform.</p>
</div>
""",
            unsafe_allow_html=True,
        )
        name = st.text_input("Name or handle", placeholder="anonymous")
        kind = st.selectbox("What are you sending?", ["presence", "proposal", "need", "offer", "friction"])
        message = st.text_area("Message", placeholder="Write the thing that should enter the room.")
        intensity = st.slider("Intensity", 0, 10, 5)
        submitted = st.form_submit_button("Send signal", type="primary")

with right:
    st.markdown(
        """
<section class="vl-role-module memory" data-role="MEMORY" data-component-id="FLOW-FIELD-MEMORY-PLACEHOLDER-001">
  <span class="vl-role-tag">MEMORY</span>
  <h2 class="vl-flow-title">Trace</h2>
  <p class="vl-flow-copy">After action, the system should show that the signal has not vanished.</p>
</section>
""",
        unsafe_allow_html=True,
    )

if submitted:
    safe_name = html.escape(name or "anonymous")
    safe_kind = html.escape(kind)
    safe_message = html.escape(message or "No message body.")
    echo = html.escape((message or kind or "trace").upper())
    st.markdown(
        f"""
<section class="vl-trace-message" data-role="MEMORY" data-component-id="FLOW-FIELD-MEMORY-TRACE-001">
  <span class="vl-role-tag">MEMORY</span>
  <p><strong>{safe_name}</strong> sent <span class="accent-strike">{safe_kind}</span> at intensity {intensity}.</p>
  <p>{safe_message}</p>
  <span class="vl-trace-echo">{echo}</span>
</section>
""",
        unsafe_allow_html=True,
    )
