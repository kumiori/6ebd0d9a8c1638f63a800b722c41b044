from __future__ import annotations

from pathlib import Path

import streamlit as st

from services.visual_primitives import apply_visual_lab_theme
from ui import set_page


ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "assets" / "effects" / "reorder_cards.css"


def _reorder_html() -> str:
    css = CSS_PATH.read_text(encoding="utf-8")
    return f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <style>{css}</style>
</head>
<body>
  <div id="app"></div>
  <script type="module">
    import React, {{ useEffect, useState }} from "https://esm.sh/react@19";
    import {{ createRoot }} from "https://esm.sh/react-dom@19/client";
    import {{ Reorder, resize }} from "https://esm.sh/motion@12.23.24/react";

    const e = React.createElement;
    const whileDrag = {{
      scale: 1.045,
      boxShadow: "0 10px 28px rgba(0, 0, 0, 0.28)",
      zIndex: 20,
    }};

    const initialItems = [
      {{ id: "entry", type: "identity", title: "entry", left: "host", right: "visitor", top: "access key", bottom: "anonymous" }},
      {{ id: "signal", type: "word", title: "signal\\nfield" }},
      {{ id: "proposal", type: "identity", title: "proposal", left: "need", right: "offer", top: "public note", bottom: "session buffer" }},
      {{ id: "decision", type: "word", title: "decision\\nscore" }},
    ];

    function IdentityCard({{ layer }}) {{
      return e(
        Reorder.Item,
        {{ value: layer, whileDrag, className: "field-card identity", "data-component-id": "I-REORDER-IDENTITY-CARD-001" }},
        e("div", {{ className: "face-letter" }}, layer.title.slice(0, 1)),
        e("div", {{ className: "edge-label top" }}, layer.top),
        e("div", {{ className: "edge-label left" }}, layer.left),
        e("div", {{ className: "edge-label right" }}, layer.right),
        e("div", {{ className: "edge-label bottom" }}, layer.bottom),
      );
    }}

    function WordCard({{ layer }}) {{
      return e(
        Reorder.Item,
        {{ value: layer, whileDrag, className: "field-card alt", "data-component-id": "I-REORDER-WORD-CARD-001" }},
        e(
          "div",
          {{ className: "face-logo" }},
          layer.title.split("\\n").map((line, index) =>
            e(React.Fragment, {{ key: line }}, index > 0 ? e("br") : null, line)
          ),
        ),
      );
    }}

    function App() {{
      const [items, setItems] = useState(initialItems);
      const [axis, setAxis] = useState(window.innerWidth < 768 ? "y" : "x");

      useEffect(() => {{
        const unsubscribe = resize(({{ width }}) => {{
          setAxis(width < 768 ? "y" : "x");
        }});
        return () => unsubscribe();
      }}, []);

      return e(
        React.Fragment,
        null,
        e(
          "main",
          {{ className: "reorder-shell", "data-component-id": "I-REORDER-SHELL-001" }},
          e(
            "section",
            {{ className: "intro" }},
            e("p", {{ className: "kicker" }}, "Motion test / reorder cards"),
            e("h1", null, "Drag the order of the field"),
            e("p", null, "A small test for tactile coordination: participants can reorder roles, phases, or agenda cards without leaving the page."),
          ),
          e(
            Reorder.Group,
            {{ axis, values: items, onReorder: setItems, className: "reorder-group", "data-component-id": "I-REORDER-GROUP-001" }},
            items.map((item) =>
              item.type === "identity"
                ? e(IdentityCard, {{ key: item.id, layer: item }})
                : e(WordCard, {{ key: item.id, layer: item }})
            ),
          ),
          e("div", {{ className: "axis-note", "data-component-id": "I-REORDER-AXIS-NOTE-001" }}, axis === "x" ? "desktop axis: horizontal" : "mobile axis: vertical"),
        ),
        e("div", {{ className: "paper-shadow", "aria-hidden": "true" }}),
      );
    }}

    createRoot(document.getElementById("app")).render(e(App));
  </script>
</body>
</html>
"""


set_page("Test Reorder Cards", "🧪")
apply_visual_lab_theme("e")

st.markdown("<div class='vl-component-id'>I-REORDER-CARDS-001</div>", unsafe_allow_html=True)
st.markdown("<div class='vl-section-label'>visual test i / reorder cards</div>", unsafe_allow_html=True)
st.markdown("<h1 class='vl-hero-title'>Tactile ordering for collective work</h1>", unsafe_allow_html=True)
st.markdown(
    "<p class='vl-subtitle'>Drag the cards inside the frame. Desktop uses horizontal reorder; mobile switches to vertical.</p>",
    unsafe_allow_html=True,
)

st.iframe(_reorder_html(), height=760)
