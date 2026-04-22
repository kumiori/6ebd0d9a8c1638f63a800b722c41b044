from __future__ import annotations

import base64
import mimetypes
from pathlib import Path

import streamlit as st

from services.visual_primitives import (
    apply_visual_lab_theme,
    component_id,
    divider,
    hero_title,
    section_label,
)
from ui import set_page


ROOT = Path(__file__).resolve().parents[1]
IMAGE_PATH = ROOT / "assets" / "poster_tree_reference.png"
REF_DIR = ROOT / "assets" / "images" / "monx26_refs"
REFERENCE_IMAGES = [
    ("F-REF-HORIZONTAL-001", REF_DIR / "share-18075915232.jpg", "Hard-frame horizontal reference"),
    ("F-REF-HORIZONTAL-002", REF_DIR / "share-22310120337.jpg", "Hard-frame horizontal reference"),
    ("F-REF-VERTICAL-001", REF_DIR / "share-22372810115.jpg", "Hard-frame vertical reference"),
    ("F-REF-VERTICAL-002", REF_DIR / "share-22373420349.jpg", "Hard-frame vertical reference"),
]
ROLL_PATH = REF_DIR / "roll.jpg"
ROLL_LEFT_PATH = REF_DIR / "roll_left.jpg"
ROLL_RIGHT_PATH = REF_DIR / "roll_right.jpg"


def image_data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    payload = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:{mime};base64,{payload}"


set_page("Visual Test Poster Bleed", "🧪")
apply_visual_lab_theme("f")

section_label("visual test f / poster bleed", "F-SECTION-001")
hero_title(
    "Memory as structure",
    "One image system only: ghost image, hard frame, and controlled text-over-image variants.",
    "F-HERO-001",
)

if not IMAGE_PATH.exists():
    st.warning(
        "Place a black-and-white tree image at assets/poster_tree_reference.png to render this test with the intended poster material."
    )
    st.stop()

missing_refs = [path for _, path, _ in REFERENCE_IMAGES if not path.exists()]
if missing_refs or not ROLL_LEFT_PATH.exists() or not ROLL_RIGHT_PATH.exists():
    st.warning("Some image references are missing from assets/images/monx26_refs.")

image_src = image_data_uri(IMAGE_PATH)

component_id("F-IMAGE-STAGE-001")
st.markdown(
    f"""
<section class="vl-image-stage">
  <div class="vl-morph-field" aria-hidden="true">
    <div class="vl-morph-blob pink"></div>
    <div class="vl-morph-blob orange"></div>
    <div class="vl-morph-blob line"></div>
  </div>
  <div class="vl-image-content">
    <div class="vl-section-label">moving field</div>
    <h2 class="vl-panel-title">The background is not illustration. It is pressure under structure.</h2>
    <p class="vl-panel-copy">Slow color masses drift behind the text. No ghost photograph in this stage.</p>
  </div>
</section>
""",
    unsafe_allow_html=True,
)

divider()

left, right = st.columns([0.85, 1.15], gap="large")
with left:
    component_id("F-HARD-FRAME-001")
    st.markdown(
        f"""
<figure class="vl-hard-frame">
  <img src="{image_src}" alt="Black and white tree reference" />
  <figcaption class="vl-image-caption">Hard frame. No radius. No glow. Printed matter.</figcaption>
</figure>
""",
        unsafe_allow_html=True,
    )
with right:
    component_id("F-TEXT-OVER-IMAGE-001")
    st.markdown(
        f"""
<section class="vl-image-overlay">
  <img src="{image_src}" alt="" />
  <h2>Every signal leaves a trace.</h2>
  <p>Only one block uses text over image. The rest of the page stays structural.</p>
</section>
""",
        unsafe_allow_html=True,
    )

divider()

section_label("strict reference frames", "F-REFERENCE-LABEL-001")
frames = []
for component, path, caption in REFERENCE_IMAGES:
    if not path.exists():
        continue
    klass = "vertical" if "VERTICAL" in component else ""
    frames.append(
        f"""
<figure class="vl-ref-frame {klass}">
  <div class="vl-component-id">{component}</div>
  <img src="{image_data_uri(path)}" alt="{caption}" />
  <figcaption class="vl-image-caption">{caption}. Border retained, no radius.</figcaption>
</figure>
"""
    )
st.markdown(f"<section class='vl-image-grid'>{''.join(frames)}</section>", unsafe_allow_html=True)

if ROLL_LEFT_PATH.exists() and ROLL_RIGHT_PATH.exists():
    divider()
    component_id("F-ROLL-SPLIT-001")
    roll_left_src = image_data_uri(ROLL_LEFT_PATH)
    roll_right_src = image_data_uri(ROLL_RIGHT_PATH)
    st.markdown(
        f"""
<section class="vl-roll-split">
  <figure class="vl-roll-half left">
    <img src="{roll_left_src}" alt="Left half of roll reference" />
  </figure>
  <figure class="vl-roll-half right">
    <img src="{roll_right_src}" alt="Right half of roll reference" />
  </figure>
</section>
<p class="vl-form-note">Roll reference treated as two vertical image fields: left and right halves.</p>
""",
        unsafe_allow_html=True,
    )
