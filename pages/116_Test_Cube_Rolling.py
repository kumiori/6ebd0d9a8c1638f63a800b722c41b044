from __future__ import annotations

import base64
import mimetypes
from pathlib import Path
from textwrap import dedent

import streamlit as st

from services.visual_primitives import apply_visual_lab_theme
from ui import set_page


ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "assets" / "effects" / "cube_roll.css"
REF_DIR = ROOT / "assets" / "images" / "monx26_refs"
FACE_IMAGES = [
    REF_DIR / "share-18075915232.jpg",
    REF_DIR / "share-22310120337.jpg",
    REF_DIR / "share-22372810115.jpg",
    REF_DIR / "share-22373420349.jpg",
    REF_DIR / "roll_left.jpg",
    REF_DIR / "roll_right.jpg",
]


def _data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "image/jpeg"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def _cube_html() -> str:
    css = CSS_PATH.read_text(encoding="utf-8")
    images = [_data_uri(path) for path in FACE_IMAGES if path.exists()]
    if len(images) < 6:
        raise RuntimeError("Cube test requires six local face images.")
    js_images = "[" + ",".join(repr(src) for src in images[:6]) + "]"
    return f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>{css}</style>
</head>
<body>
  <div id="scene" data-component-id="G-CUBE-SCENE-001">
    <div id="cube">
      <div class="face" data-face="top" data-i="0"></div>
      <div class="face" data-face="front" data-i="1"></div>
      <div class="face" data-face="right" data-i="2"></div>
      <div class="face" data-face="back" data-i="3"></div>
      <div class="face" data-face="left" data-i="4"></div>
      <div class="face" data-face="bottom" data-i="5"></div>
    </div>
  </div>
  <div id="hud" data-component-id="G-CUBE-HUD-001">
    <div id="hud_pct">000%</div>
    <div class="progress-bar"><div class="progress-fill" id="prog_fill"></div></div>
    <div class="scene-label" id="scene_name">ENTRY</div>
  </div>
  <div id="scene_strip" data-component-id="G-CUBE-STRIP-001">
    <a href="#s0" class="scene-dot active"></a>
    <a href="#s1" class="scene-dot"></a>
    <a href="#s2" class="scene-dot"></a>
    <a href="#s3" class="scene-dot"></a>
    <a href="#s4" class="scene-dot"></a>
    <a href="#s5" class="scene-dot"></a>
  </div>
  <div id="face_caption" data-component-id="G-CUBE-CAPTION-001">
    <div id="face_caption_num">01</div>
    <div id="face_caption_name">ENTRY</div>
  </div>
  <div id="scroll_container" data-component-id="G-CUBE-SECTIONS-001">
    {_SECTIONS}
  </div>
  <script>
    const IMAGE_SRCS = {js_images};
{dedent(_CUBE_JS)}
  </script>
</body>
</html>
"""


_SECTIONS = r"""
<section id="s0">
  <div class="text-card">
    <div class="tag reveal">Cube score</div>
    <h1 class="reveal">ROLL THE FIELD</h1>
    <p class="body-text reveal">A cube becomes a moving archive. Each turn reveals a different face of the collective instrument.</p>
    <div class="cta-row reveal"><a class="cta" href="#s1">Enter</a></div>
  </div>
</section>
<section id="s1">
  <div class="text-card right">
    <div class="tag reveal">01 — Threshold</div>
    <h2 class="reveal">THE DOOR IS A FACE</h2>
    <p class="body-text reveal">The object rolls instead of sliding. Navigation becomes physical, almost theatrical.</p>
    <div class="cta-row reveal"><a class="cta-back" href="#s0">Back</a><a class="cta" href="#s2">Turn</a></div>
  </div>
</section>
<section id="s2">
  <div class="text-card">
    <div class="tag reveal">02 — Signal</div>
    <h2 class="reveal">THE ROOM LEAVES MARKS</h2>
    <p class="body-text reveal">Image, text, and decision can become faces of the same object.</p>
    <div class="cta-row reveal"><a class="cta-back" href="#s1">Back</a><a class="cta" href="#s3">Turn</a></div>
  </div>
</section>
<section id="s3">
  <div class="text-card right">
    <div class="tag reveal">03 — Decision</div>
    <h2 class="reveal">A FACE SETTLES</h2>
    <p class="body-text reveal">Scrolling can map to decision phases: entry, proposal, objection, consent, delegation.</p>
    <div class="cta-row reveal"><a class="cta-back" href="#s2">Back</a><a class="cta" href="#s4">Turn</a></div>
  </div>
</section>
<section id="s4">
  <div class="text-card">
    <div class="tag reveal">04 — Archive</div>
    <h2 class="reveal">A MEMORY HAS EDGES</h2>
    <p class="body-text reveal">The roll can become an image browser, a proposal sequence, or a score for public participation.</p>
    <div class="cta-row reveal"><a class="cta-back" href="#s3">Back</a><a class="cta" href="#s5">Turn</a></div>
  </div>
</section>
<section id="s5">
  <div class="text-card right">
    <div class="tag reveal">05 — Return</div>
    <h2 class="reveal">BEGIN AGAIN</h2>
    <p class="body-text reveal">The cube is an experiment in navigation as ritual: not efficient, but memorable.</p>
    <div class="cta-row reveal"><a class="cta-back" href="#s4">Back</a><a class="cta" href="#s0">Again</a></div>
  </div>
</section>
"""


_CUBE_JS = r"""
const FACE_NAMES = ["ENTRY", "THRESHOLD", "SIGNAL", "DECISION", "ARCHIVE", "RETURN"];
const STOPS = [
  { rx: 90, ry: 0 },
  { rx: 0, ry: 0 },
  { rx: 0, ry: -90 },
  { rx: 0, ry: -180 },
  { rx: 0, ry: -270 },
  { rx: -90, ry: -360 },
];

const cube = document.getElementById("cube");
const faces = [...document.querySelectorAll(".face")];
const sections = [...document.querySelectorAll("section")];
const dots = [...document.querySelectorAll(".scene-dot")];
const hudPct = document.getElementById("hud_pct");
const progFill = document.getElementById("prog_fill");
const sceneName = document.getElementById("scene_name");
const captionNum = document.getElementById("face_caption_num");
const captionName = document.getElementById("face_caption_name");

faces.forEach((face, i) => {
  const img = new Image();
  img.src = IMAGE_SRCS[i];
  img.alt = FACE_NAMES[i] || "";
  face.appendChild(img);
});

function clamp(v, min, max) {
  return Math.min(Math.max(v, min), max);
}

function easeInOut(t) {
  return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
}

function sectionTops() {
  return sections.map((section) => section.getBoundingClientRect().top + window.scrollY);
}

let tops = sectionTops();
let maxScroll = Math.max(1, document.documentElement.scrollHeight - innerHeight);

function resize() {
  tops = sectionTops();
  maxScroll = Math.max(1, document.documentElement.scrollHeight - innerHeight);
}
window.addEventListener("resize", resize);

function activeIndex() {
  const mid = window.scrollY + innerHeight * 0.5;
  let idx = 0;
  for (let i = 0; i < tops.length; i++) {
    if (mid >= tops[i]) idx = i;
  }
  return clamp(idx, 0, STOPS.length - 1);
}

function setCube(progress) {
  const t = progress * (STOPS.length - 1);
  const i = Math.min(Math.floor(t), STOPS.length - 2);
  const f = easeInOut(t - i);
  const a = STOPS[i];
  const b = STOPS[i + 1];
  const rx = a.rx + (b.rx - a.rx) * f;
  const ry = a.ry + (b.ry - a.ry) * f;
  cube.style.transform = `rotateX(${rx}deg) rotateY(${ry}deg)`;
}

function update() {
  const progress = clamp(window.scrollY / maxScroll, 0, 1);
  const pct = Math.round(progress * 100);
  const idx = activeIndex();
  hudPct.textContent = String(pct).padStart(3, "0") + "%";
  progFill.style.width = pct + "%";
  sceneName.textContent = FACE_NAMES[idx];
  captionNum.textContent = String(idx + 1).padStart(2, "0");
  captionName.textContent = FACE_NAMES[idx];
  dots.forEach((dot, i) => dot.classList.toggle("active", i === idx));
  setCube(progress);
}

window.addEventListener("scroll", update, { passive: true });

document.addEventListener("click", (event) => {
  const link = event.target.closest('a[href^="#s"]');
  if (!link) return;
  const target = document.querySelector(link.getAttribute("href"));
  if (!target) return;
  event.preventDefault();
  target.scrollIntoView({ behavior: "smooth", block: "start" });
});

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) entry.target.classList.add("visible");
    });
  },
  { threshold: 0.1 }
);
document.querySelectorAll(".reveal").forEach((el) => observer.observe(el));

resize();
update();
"""


set_page("Test Cube Rolling", "🧪")
apply_visual_lab_theme("f")

st.markdown("<div class='vl-component-id'>G-CUBE-ROLL-001</div>", unsafe_allow_html=True)
st.markdown("<div class='vl-section-label'>visual test g / rolling cube</div>", unsafe_allow_html=True)
st.markdown("<h1 class='vl-hero-title'>Cube navigation as score</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='vl-subtitle'>Scroll inside the frame. The cube rolls through image faces while text cards act as movements.</p>",
    unsafe_allow_html=True,
)

try:
    st.iframe(_cube_html(), height=860)
except RuntimeError as exc:
    st.error(str(exc))
