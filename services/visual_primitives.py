from __future__ import annotations

from pathlib import Path
from typing import Iterable

import streamlit as st

from ui import render_sidebar_nav


ROOT = Path(__file__).resolve().parents[1]
CSS_PATH = ROOT / "assets" / "effects" / "visual_lab.css"


def apply_visual_lab_theme(style: str) -> None:
    css = CSS_PATH.read_text(encoding="utf-8") if CSS_PATH.exists() else ""
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    st.markdown(f"<div class='vl-style-{style}'></div>", unsafe_allow_html=True)
    render_sidebar_nav()


def component_id(component_id: str) -> None:
    st.markdown(
        f"<div class='vl-component-id'>{component_id}</div>",
        unsafe_allow_html=True,
    )


def section_label(text: str, component_id_value: str | None = None) -> None:
    if component_id_value:
        component_id(component_id_value)
    st.markdown(f"<div class='vl-section-label'>{text}</div>", unsafe_allow_html=True)


def hero_title(title: str, subtitle: str = "", component_id_value: str | None = None, *, serif: bool = False) -> None:
    if component_id_value:
        component_id(component_id_value)
    serif_class = " serif" if serif else ""
    st.markdown(f"<h1 class='vl-hero-title{serif_class}'>{title}</h1>", unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p class='vl-subtitle'>{subtitle}</p>", unsafe_allow_html=True)


def soft_panel(
    title: str,
    body: str,
    component_id_value: str,
    *,
    variant: str = "",
) -> None:
    variant_class = f" {variant}" if variant else ""
    st.markdown(
        "\n".join(
            [
                f"<section class='vl-panel{variant_class}'>",
                f"<div class='vl-component-id'>{component_id_value}</div>",
                f"<h2 class='vl-panel-title'>{title}</h2>",
                f"<p class='vl-panel-copy'>{body}</p>",
                "</section>",
            ]
        ),
        unsafe_allow_html=True,
    )


def divider() -> None:
    st.markdown("<div class='vl-divider'></div>", unsafe_allow_html=True)


def form_note(text: str, component_id_value: str | None = None) -> None:
    if component_id_value:
        component_id(component_id_value)
    st.markdown(f"<p class='vl-form-note'>{text}</p>", unsafe_allow_html=True)


def token_strip(tokens: Iterable[str], component_id_value: str) -> None:
    chips = "".join(f"<span class='vl-token'>{token}</span>" for token in tokens)
    st.markdown(
        f"<div class='vl-component-id'>{component_id_value}</div><div class='vl-token-strip'>{chips}</div>",
        unsafe_allow_html=True,
    )
