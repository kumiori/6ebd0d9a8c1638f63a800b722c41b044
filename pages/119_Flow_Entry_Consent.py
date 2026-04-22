from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

import streamlit as st

from services.visual_primitives import apply_visual_lab_theme, component_id, section_label
from ui import set_page


ROOT = Path(__file__).resolve().parents[1]
IMAGE_PATH = ROOT / "assets" / "images" / "monx26_refs" / "share-18075915232.jpg"


def image_data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


set_page("Flow Entry Consent", "🧪")
apply_visual_lab_theme("f")

section_label("flow 1 / entry to consent", "FLOW-ENTRY-CONSENT-001")
component_id("FLOW-ENTRY-HERO-001")
st.markdown(
    "<h1 class='hero-overflow'>Entry asks for consent</h1>",
    unsafe_allow_html=True,
)

image_src = image_data_uri(IMAGE_PATH) if IMAGE_PATH.exists() else ""

st.markdown(
    f"""
<section class="vl-flow-sequence">
  <div class="layout-asym">
    <article class="vl-role-module silent" data-role="SILENT" data-component-id="FLOW-ENTRY-SILENT-001">
      <span class="vl-role-tag">SILENT</span>
      <h2 class="vl-flow-title">Before entry, the room is only structure.</h2>
      <p class="vl-flow-copy">No promise. No pitch. A dark field waits for a threshold to be named.</p>
    </article>
    <article class="vl-role-module memory fragment" data-role="MEMORY" data-component-id="FLOW-ENTRY-MEMORY-001">
      <span class="vl-role-tag">MEMORY</span>
      <div class="vl-image-crop-violent">
        {'<img src="' + image_src + '" alt="Cropped black and white reference" />' if image_src else ''}
      </div>
    </article>
  </div>
  <article class="vl-role-module interruption" data-role="INTERRUPTION" data-component-id="FLOW-ENTRY-INTERRUPTION-001">
    <span class="vl-role-tag">INTERRUPTION</span>
    <h2 class="vl-flow-title">This room asks something from you.</h2>
    <p class="vl-flow-copy">Consent is not background. It interrupts the visual field and changes what can happen next.</p>
  </article>
</section>
""",
    unsafe_allow_html=True,
)

component_id("FLOW-ENTRY-ACTION-001")
st.markdown(
    """
<section class="vl-role-module action" data-role="ACTION" data-component-id="FLOW-ENTRY-ACTION-MODULE-001">
  <span class="vl-role-tag">ACTION</span>
  <h2 class="vl-flow-title"><span class="accent-strike">Consent</span> as threshold</h2>
  <p class="vl-flow-copy">Pink is used here because a decision is being made.</p>
</section>
""",
    unsafe_allow_html=True,
)
st.slider("Consent threshold", 0, 10, 6)
st.button("Enter with this threshold", type="primary")
