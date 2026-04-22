from __future__ import annotations

from pathlib import Path

import streamlit as st


ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "assets" / "effects" / "css_expansion.css"


def _load_css() -> str:
    if not CSS_PATH.exists():
        return ""
    return CSS_PATH.read_text(encoding="utf-8")


def render_css_demo(body: str, *, height: int = 720, scrolling: bool = True) -> None:
    css = _load_css()
    html = (
        "<!doctype html>"
        "<html lang='en'>"
        "<head>"
        "<meta charset='utf-8' />"
        "<meta name='viewport' content='width=device-width, initial-scale=1' />"
        f"<style>{css}</style>"
        "</head>"
        f"<body>{body}</body>"
        "</html>"
    )
    st.iframe(html, height=height)
