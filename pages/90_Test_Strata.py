from __future__ import annotations

import json
from pathlib import Path
from textwrap import dedent

import streamlit as st

from ui import apply_theme, heading, set_page


ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "assets" / "effects" / "strata.css"


def _load_css() -> str:
    if not CSS_PATH.exists():
        return ""
    return CSS_PATH.read_text(encoding="utf-8")


def _sidebar_config() -> dict:
    with st.sidebar:
        st.header("Strata parameters")
        seed = st.number_input("Seed", min_value=0, max_value=999999, value=32, step=1)

        st.subheader("Canvas")
        width = st.slider("SVG width", 360, 1400, 750, 10)
        height = st.slider("SVG height", 480, 1800, 1000, 10)
        frame_width = st.slider("Frame width", 0, 80, 24, 2)
        frame_color = st.color_picker("Frame color", "#f5f3ef")

        st.subheader("Contours")
        layers = st.slider("Layers", 12, 220, 130, 1)
        density = st.slider("Point density", 0.8, 8.0, 2.0, 0.1)
        band_size = st.slider("Band size", 1, 24, 7, 1)
        fit_margin = st.slider("Fit margin", 0.0, 0.35, 0.12, 0.01)

        st.subheader("Palette")
        palette = st.selectbox(
            "Palette set",
            ["poster red", "poster neon", "clay field", "warm fracture"],
            index=0,
        )

        st.subheader("Swirl field")
        attractor_count = st.slider("Attractor count", 0, 16, 7, 1)
        radius_min = st.slider("Attractor radius min", 120, 6000, 800, 20)
        radius_max = st.slider("Attractor radius max", 300, 14000, 3000, 50)
        angle_min = st.slider("Swirl angle min", 0, 260, 40, 1)
        angle_max = st.slider("Swirl angle max", 0, 360, 150, 1)
        falloff_exponent = st.slider("Falloff exponent", 0.5, 5.0, 1.7, 0.1)
        spread_exponent = st.slider("Spread exponent", 0.5, 5.0, 2.4, 0.1)
        show_attractors = st.checkbox("Show attractors", value=False)

    radius_min, radius_max = sorted((radius_min, radius_max))
    angle_min, angle_max = sorted((angle_min, angle_max))

    return {
        "seed": seed,
        "width": width,
        "height": height,
        "frameWidth": frame_width,
        "frameColor": frame_color,
        "palette": palette,
        "params": {
            "layers": layers,
            "density": density,
            "bandSize": band_size,
            "fitMargin": fit_margin,
            "attractorCount": attractor_count,
            "radiusMin": radius_min,
            "radiusMax": radius_max,
            "angleMin": angle_min,
            "angleMax": angle_max,
            "falloffExponent": falloff_exponent,
            "spreadExponent": spread_exponent,
            "showAttractors": show_attractors,
        },
    }


def _strata_html(config: dict) -> str:
    css = _load_css()
    js = dedent(_STRATA_JS).replace("__STRATA_CONFIG__", json.dumps(config))
    return f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>{css}</style>
</head>
<body>
  <div class="artwork">
    <div class="svg-container" id="svg-container"></div>
    <div class="controls">
      <span class="seed-label" id="seed-display"></span>
      <input type="number" id="seed-input" class="seed-input" />
      <button id="btn-random" class="btn">Random</button>
    </div>
  </div>

  <script>
{js}
  </script>
</body>
</html>
"""


_STRATA_JS = r"""
const SVG_NS = "http://www.w3.org/2000/svg";
const config = __STRATA_CONFIG__;
const W = config.width;
const H = config.height;
const params = config.params;

const palettes = {
  "poster red": ["#d94f5e", "#102231", "#ead49a", "#f28580", "#c83653", "#f4bd84"],
  "poster neon": ["#e0589d", "#090909", "#f08b2d", "#ead49a", "#173242", "#d9579f"],
  "clay field": ["#dc555e", "#142936", "#ecd8a7", "#f08b2d", "#ef8177", "#7f233d"],
  "warm fracture": ["#d64d5c", "#0d2330", "#f1d89a", "#f08b8a", "#c93f58", "#f1b16c"],
};

function mulberry32(seed) {
  let s = seed | 0;
  return () => {
    s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function createRandom(seed) {
  const value = mulberry32(seed);
  return {
    value,
    range: (a, b) => a + value() * (b - a),
    rangeFloor: (a, b) => Math.floor(a + value() * (b - a)),
    pick: (arr) => arr[Math.floor(value() * arr.length)],
  };
}

function makeEl(name, attrs = {}) {
  const el = document.createElementNS(SVG_NS, name);
  for (const [key, value] of Object.entries(attrs)) {
    el.setAttribute(key, String(value));
  }
  return el;
}

function polyToD(poly) {
  if (!poly || poly.length < 3) return "";
  let d = `M${poly[0].x.toFixed(2)},${poly[0].y.toFixed(2)}`;
  for (let i = 1; i < poly.length; i++) {
    d += `L${poly[i].x.toFixed(2)},${poly[i].y.toFixed(2)}`;
  }
  return d + "Z";
}

function applyAttractors(attractors, points, diag) {
  for (const at of attractors) {
    const { cx, cy, r, a, fe, se } = at;
    for (const pt of points) {
      const dx = pt.x - cx;
      const dy = pt.y - cy;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < 1e-6) continue;
      const swirlT = Math.pow(1 - Math.min(dist / r, 1), fe);
      const globalT = Math.pow(1 - Math.min(dist / diag, 1), se);
      const theta = Math.atan2(dy, dx) + swirlT * a * globalT;
      pt.x = cx + Math.cos(theta) * dist;
      pt.y = cy + Math.sin(theta) * dist;
    }
  }
}

function spawnAttractors(random) {
  const out = [];
  for (let i = 0; i < params.attractorCount; i++) {
    out.push({
      cx: random.range(0, W),
      cy: random.range(0, H),
      r: random.range(params.radiusMin, params.radiusMax),
      a: (Math.PI / 180) * random.range(params.angleMin, params.angleMax) * random.pick([-1, 1]),
      fe: params.falloffExponent,
      se: params.spreadExponent,
    });
  }
  return out;
}

function refit(points) {
  if (!points.length) return;
  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
  for (const p of points) {
    minX = Math.min(minX, p.x);
    maxX = Math.max(maxX, p.x);
    minY = Math.min(minY, p.y);
    maxY = Math.max(maxY, p.y);
  }
  const bw = maxX - minX || 1;
  const bh = maxY - minY || 1;
  const targetW = W * (1 - 2 * params.fitMargin);
  const targetH = H * (1 - 2 * params.fitMargin);
  const s = Math.min(targetW / bw, targetH / bh);
  const ox = (W - s * bw) / 2 - s * minX;
  const oy = (H - s * bh) / 2 - s * minY;
  for (const p of points) {
    p.x = ox + p.x * s;
    p.y = oy + p.y * s;
  }
}

function generateContours() {
  const contours = [];
  const allPoints = [];
  const cx = W / 2;
  const cy = H / 2;
  const diag = Math.sqrt(W * W + H * H);
  const maxR = diag * 0.6;
  const spacing = params.density;
  const rStep = maxR / params.layers;

  for (let layer = 1; layer <= params.layers; layer++) {
    const rx = layer * rStep;
    const ry = layer * rStep * (H / W);
    const circ = Math.PI * 2 * Math.max(rx, ry);
    const n = Math.max(28, Math.ceil(circ / spacing));
    const pts = [];
    for (let i = 0; i <= n; i++) {
      const a = (i / n) * Math.PI * 2;
      pts.push({ x: cx + Math.cos(a) * rx, y: cy + Math.sin(a) * ry });
    }
    contours.push(pts);
    allPoints.push(...pts);
  }
  return { contours, allPoints, diag };
}

function draw(seed) {
  const random = createRandom(seed);
  const palette = palettes[config.palette] || palettes["poster red"];
  const bg = palette[0];
  const inks = palette.slice(1);
  const container = document.getElementById("svg-container");
  container.innerHTML = "";

  const svg = makeEl("svg", {
    viewBox: `0 0 ${W} ${H}`,
    width: W,
    height: H,
    role: "img",
    "aria-label": "Generative strata artwork",
  });
  container.appendChild(svg);

  svg.appendChild(makeEl("rect", { x: 0, y: 0, width: W, height: H, fill: bg }));

  const { contours, allPoints, diag } = generateContours();
  const attractors = spawnAttractors(random);
  applyAttractors(attractors, allPoints, diag);
  refit(allPoints);

  for (let i = contours.length - 1; i >= 0; i--) {
    const color = inks[Math.floor(i / params.bandSize) % inks.length];
    const d = polyToD(contours[i]);
    if (!d) continue;
    svg.appendChild(makeEl("path", {
      d,
      fill: color,
      stroke: "none",
    }));
  }

  if (params.showAttractors) {
    for (const at of attractors) {
      svg.appendChild(makeEl("circle", {
        cx: at.cx,
        cy: at.cy,
        r: Math.min(at.r, diag * 0.5),
        fill: "none",
        stroke: "#ff2e88",
        "stroke-width": 3,
        opacity: 0.52,
      }));
      svg.appendChild(makeEl("circle", {
        cx: at.cx,
        cy: at.cy,
        r: 7,
        fill: "#ff2e88",
        opacity: 0.82,
      }));
    }
  }

  if (config.frameWidth > 0) {
    svg.appendChild(makeEl("rect", {
      x: 0,
      y: 0,
      width: W,
      height: H,
      fill: "none",
      stroke: config.frameColor,
      "stroke-width": config.frameWidth,
    }));
  }
  document.getElementById("seed-display").textContent = "#" + seed;
}

function boot() {
  const input = document.getElementById("seed-input");
  const btn = document.getElementById("btn-random");
  const initial = config.seed;
  input.value = initial;
  draw(initial);

  btn.addEventListener("click", () => {
    const seed = Math.floor(Math.random() * 1000000);
    input.value = seed;
    draw(seed);
  });
  input.addEventListener("change", () => {
    draw(Number(input.value) || 0);
  });
}

boot();
"""


set_page("Test Strata", "🧪")
apply_theme()
strata_config = _sidebar_config()

heading(
    "test page",
    "Strata field",
    "A browser-side generative SVG test adapted from the CodePen reference.",
)

st.iframe(_strata_html(strata_config), height=780)
