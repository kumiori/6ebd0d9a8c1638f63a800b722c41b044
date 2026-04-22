from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

import streamlit as st

from services.visual_primitives import apply_visual_lab_theme, component_id, section_label
from ui import set_page


ROOT = Path(__file__).resolve().parents[1]
IMAGE_PATH = ROOT / "assets" / "images" / "monx26_refs" / "share-22372810115.jpg"


def image_data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


set_page("Flow Break Version", "🧪")
apply_visual_lab_theme("f")

image_src = image_data_uri(IMAGE_PATH) if IMAGE_PATH.exists() else ""

section_label("break version / same flows under pressure", "FLOW-BREAK-VERSION-001")
st.markdown("<h1 class='hero-overflow' data-component-id='FLOW-BREAK-HERO-001'>BREAK VERSION</h1>", unsafe_allow_html=True)

st.markdown(
    f"""
<section class="vl-break-version">
  <div class="layout-asym">
    <article class="vl-role-module silent" data-role="SILENT" data-component-id="FLOW-BREAK-SILENT-001">
      <span class="vl-role-tag">SILENT</span>
      <h2 class="vl-flow-title">Entry does not explain itself.</h2>
    </article>
    <article class="vl-role-module memory fragment" data-role="MEMORY" data-component-id="FLOW-BREAK-MEMORY-001">
      <span class="vl-role-tag">MEMORY</span>
      <div class="vl-image-crop-violent">
        {'<img src="' + image_src + '" alt="Cropped black and white reference" />' if image_src else ''}
      </div>
    </article>
  </div>

  <article class="vl-role-module interruption" data-role="INTERRUPTION" data-component-id="FLOW-BREAK-INTERRUPTION-001">
    <span class="vl-role-tag">INTERRUPTION</span>
    <h2 class="vl-flow-title">Consent enters from outside the grid.</h2>
  </article>

  <div class="layout-asym flip">
    <article class="vl-role-module carrier" data-role="CARRIER" data-component-id="FLOW-BREAK-CARRIER-001">
      <span class="vl-role-tag">CARRIER</span>
      <h2 class="vl-flow-title">The field records the disturbance.</h2>
      <p class="vl-flow-copy">The trace is not a receipt. It is a fragment left behind.</p>
    </article>
    <article class="vl-role-module action" data-role="ACTION" data-component-id="FLOW-BREAK-ACTION-BLOCK-001">
      <span class="vl-role-tag">ACTION</span>
      <div class="vl-action-too-big">SEND</div>
    </article>
  </div>

  <article class="vl-provocation" data-role="INTERRUPTION" data-component-id="FLOW-BREAK-PROVOCATION-001">
    <span>DECISION</span>
    <span class="accent-strike">THR-</span>
  </article>
</section>
""",
    unsafe_allow_html=True,
)

component_id("FLOW-BREAK-ACTION-001")
st.slider("Pressure", 0, 10, 8)
st.button("Commit the break", type="primary")
