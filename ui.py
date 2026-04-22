from __future__ import annotations

import streamlit as st

from config import settings


NAV_GROUPS = [
    (
        "Core",
        "●",
        [
            ("app.py", "Home", "🏠"),
            ("pages/01_Participate.py", "Participate", "🗣️"),
            ("pages/02_Decisions.py", "Decisions", "⚖️"),
            ("pages/03_Backbone.py", "Backbone", "🧭"),
        ],
    ),
    (
        "Experience Flows",
        "◉",
        [
            ("pages/119_Flow_Entry_Consent.py", "Entry → Consent", "🚪"),
            ("pages/120_Flow_Field_Expression.py", "Field → Expression", "✍️"),
            ("pages/121_Flow_Backstage_Control.py", "Backstage → Control", "🎛️"),
            ("pages/122_Flow_Break_Version.py", "Break Version", "⚡"),
        ],
    ),
    (
        "Visual Language",
        "◆",
        [
            ("pages/110_Test_Visual_Editorial.py", "Editorial", "📰"),
            ("pages/111_Test_Visual_Score.py", "Score", "🎼"),
            ("pages/112_Test_Visual_Cue_Sheet.py", "Cue Sheet", "📋"),
            ("pages/113_Test_Visual_White_Interruption.py", "White Interruption", "⬜"),
            ("pages/114_Test_Visual_Accent_Event.py", "Accent Event", "💗"),
            ("pages/115_Test_Visual_Poster_Bleed.py", "Poster Bleed", "🖼️"),
        ],
    ),
    (
        "Interaction Tests",
        "▣",
        [
            ("pages/90_Test_Strata.py", "Strata", "🌀"),
            ("pages/116_Test_Cube_Rolling.py", "Cube Rolling", "🎲"),
            ("pages/117_Test_Scooped_Corner.py", "Scooped Corner", "✂️"),
            ("pages/118_Test_Reorder_Cards.py", "Reorder Cards", "🃏"),
            ("pages/123_Test_Fragment_Board.py", "Fragment Board", "🧩"),
        ],
    ),
    (
        "CSS Expansion",
        "▧",
        [
            ("pages/91_Test_Anchor_Positioning.py", "Anchor Positioning", "⚓"),
            ("pages/92_Test_Popover.py", "Popover", "💬"),
            ("pages/93_Test_Dialog.py", "Dialog", "🪟"),
            ("pages/94_Test_Scroll_Driven.py", "Scroll Driven", "↕️"),
            ("pages/95_Test_View_Transitions.py", "View Transitions", "🔁"),
            ("pages/96_Test_Select_Customization.py", "Select Styling", "🎚️"),
            ("pages/97_Test_Focusgroup.py", "Focusgroup", "⌨️"),
            ("pages/98_Test_Masonry_Grid_Lanes.py", "Masonry", "🧱"),
            ("pages/99_Test_Field_Sizing.py", "Field Sizing", "📏"),
            ("pages/100_Test_Scroll_State.py", "Scroll State", "📍"),
            ("pages/101_Test_CSS_If.py", "CSS If", "❔"),
        ],
    ),
]


def set_page(title: str = "", icon: str = "⬛") -> None:
    st.set_page_config(
        page_title=f"{title} · {settings.page_title}" if title else settings.page_title,
        page_icon=icon,
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def render_sidebar_nav() -> None:
    st.sidebar.markdown("<div class='monx-nav-title'>MONX26</div>", unsafe_allow_html=True)
    for group_label, group_icon, links in NAV_GROUPS:
        st.sidebar.markdown(
            f"<div class='monx-nav-group'>{group_icon} {group_label}</div>",
            unsafe_allow_html=True,
        )
        for target, label, icon in links:
            st.sidebar.page_link(target, label=label, icon=icon)
    st.sidebar.divider()


def apply_theme() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,100..900;1,9..144,100..900&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');
        :root {
            --monx-font-display: "Fraunces", Georgia, "Times New Roman", serif;
            --monx-font-body: "Poppins", -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            --monx-bg: #030303;
            --monx-bg-2: #090909;
            --monx-sidebar: #252730;
            --monx-sidebar-hover: #3b3d46;
            --monx-ink: #f3f0eb;
            --monx-muted: #b8b2aa;
            --monx-faint: rgba(243, 240, 235, 0.12);
            --monx-field: #202129;
            --monx-field-border: #3a3b44;
            --monx-pink: #d9579f;
            --monx-pink-hot: #f05aa6;
            --monx-orange: #ff8b2b;
            --monx-red: #ef524c;
        }
        html,
        body,
        [data-testid="stAppViewContainer"],
        [data-testid="stApp"] {
            background: var(--monx-bg);
            color: var(--monx-ink);
            font-family: var(--monx-font-body);
        }
        .stApp {
            background:
                linear-gradient(118deg, transparent 0 34%, rgba(217, 87, 159, 0.12) 34.2% 34.45%, transparent 34.7%),
                linear-gradient(62deg, transparent 0 48%, rgba(243, 240, 235, 0.10) 48.1% 48.32%, transparent 48.55%),
                linear-gradient(145deg, transparent 0 64%, rgba(217, 87, 159, 0.10) 64.1% 64.32%, transparent 64.55%),
                var(--monx-bg);
        }
        [data-testid="stHeader"] {
            background: rgba(3, 3, 3, 0.88);
        }
        .block-container {
            max-width: 1100px;
            padding-top: 3.2rem;
        }
        [data-testid="stSidebar"] {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            min-width: 0 !important;
            max-width: 0 !important;
            transform: translateX(-100%) !important;
        }
        [data-testid="stSidebarCollapsedControl"],
        [data-testid="collapsedControl"],
        button[title="Open sidebar"],
        button[aria-label="Open sidebar"],
        button[title="Close sidebar"],
        button[aria-label="Close sidebar"] {
            display: none !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }
        section[data-testid="stSidebar"] {
            display: none !important;
        }
        [data-testid="stAppViewContainer"] > .main,
        [data-testid="stAppViewContainer"] main {
            margin-left: 0 !important;
        }
        [data-testid="stSidebar"] * {
            color: #e2e0dc;
        }
        [data-testid="stSidebar"] [data-testid="stPageLink"] a {
            border-radius: 6px;
        }
        [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover,
        [data-testid="stSidebar"] [data-testid="stPageLink"] a[aria-current="page"] {
            background: var(--monx-sidebar-hover);
        }
        [data-testid="stSidebar"] hr {
            border-color: rgba(255, 255, 255, 0.12);
        }
        [data-testid="stSidebarNav"] {
            display: none;
        }
        .monx-nav-title {
            margin: 0 0 0.9rem;
            color: var(--monx-orange);
            font-family: var(--monx-font-display);
            font-size: 1.55rem;
            font-weight: 860;
            letter-spacing: 0;
            line-height: 0.9;
        }
        .monx-nav-group {
            margin: 1.15rem 0 0.35rem;
            color: var(--monx-muted);
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.14em;
            text-transform: uppercase;
        }
        [data-testid="stSidebar"] [data-testid="stPageLink"] {
            margin-bottom: 0.05rem;
        }
        h1, h2, h3 {
            letter-spacing: 0;
            color: var(--monx-ink);
        }
        h1 {
            font-family: var(--monx-font-display);
            font-size: clamp(2.8rem, 6vw, 5.4rem);
            line-height: 0.92;
            font-weight: 860;
            text-transform: none;
            color: var(--monx-ink);
            text-shadow: none;
        }
        h2, h3 {
            font-family: var(--monx-font-display);
            font-weight: 820;
        }
        p, label, span, div, li {
            color: var(--monx-ink);
            font-family: var(--monx-font-body);
        }
        .monx-kicker {
            text-transform: uppercase;
            font-size: 0.78rem;
            letter-spacing: 0.14em;
            color: var(--monx-orange);
            font-weight: 700;
        }
        .monx-panel {
            border: 1px solid rgba(217, 87, 159, 0.55);
            border-radius: 8px;
            padding: 1rem;
            background: rgba(0, 0, 0, 0.72);
            box-shadow: inset 0 0 0 1px rgba(255, 139, 43, 0.12);
        }
        .monx-muted {
            color: var(--monx-muted);
        }
        .monx-manifesto {
            position: relative;
            margin: 2.4rem 0 2rem;
            padding: clamp(1.4rem, 3vw, 2.4rem);
            border: 1px solid rgba(92, 39, 70, 0.72);
            background:
                linear-gradient(118deg, transparent 0 49%, rgba(217, 87, 159, 0.14) 49.1% 49.32%, transparent 49.55%),
                rgba(10, 10, 12, 0.78);
        }
        .monx-manifesto__label {
            margin-bottom: 1.15rem;
            color: var(--monx-orange) !important;
            font-size: 0.78rem;
            font-weight: 800;
            letter-spacing: 0.2em;
            text-transform: uppercase;
        }
        .monx-manifesto p {
            max-width: 76ch;
            margin: 0 0 1rem;
            color: #e8e1dc !important;
            font-size: clamp(1rem, 1.6vw, 1.15rem);
            line-height: 1.78;
        }
        .monx-manifesto p strong {
            color: var(--monx-ink) !important;
            font-weight: 800;
        }
        .monx-manifesto__closing {
            margin-top: 1.35rem !important;
            color: var(--monx-ink) !important;
            font-family: var(--monx-font-display) !important;
            font-size: clamp(1.6rem, 3.6vw, 2.8rem) !important;
            font-weight: 850 !important;
            line-height: 1.03 !important;
        }
        [data-testid="stMarkdownContainer"],
        [data-testid="stCaptionContainer"],
        [data-testid="stText"],
        [data-testid="stMetricLabel"],
        [data-testid="stMetricValue"],
        [data-testid="stHeadingWithActionElements"] {
            color: var(--monx-ink);
        }
        [data-testid="stCaptionContainer"],
        .stCaptionContainer,
        small {
            color: var(--monx-muted) !important;
        }
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea,
        [data-baseweb="select"] > div {
            background: var(--monx-field) !important;
            color: var(--monx-ink) !important;
            border: 1px solid var(--monx-field-border) !important;
            border-radius: 6px !important;
        }
        [data-testid="stTextInput"] input:focus,
        [data-testid="stTextArea"] textarea:focus,
        [data-baseweb="select"] > div:focus-within {
            border-color: var(--monx-pink-hot) !important;
            box-shadow: 0 0 0 1px rgba(240, 90, 166, 0.35) !important;
        }
        [data-testid="stTextInput"] label,
        [data-testid="stTextArea"] label,
        [data-testid="stSelectbox"] label,
        [data-testid="stSlider"] label {
            color: var(--monx-muted) !important;
        }
        [data-testid="stSlider"] [data-testid="stTickBar"] {
            color: var(--monx-muted) !important;
        }
        [data-testid="stSlider"] div[role="slider"] {
            background-color: var(--monx-pink-hot) !important;
            border-color: var(--monx-pink-hot) !important;
        }
        [data-testid="stSlider"] [data-baseweb="slider"] > div > div {
            background-color: rgba(243, 240, 235, 0.20);
        }
        div.stButton > button {
            border-radius: 6px;
            border: 1px solid rgba(240, 90, 166, 0.65);
            background: rgba(0, 0, 0, 0.55);
            color: var(--monx-ink);
        }
        div.stButton > button[kind="primary"],
        [data-testid="stFormSubmitButton"] button[kind="primary"],
        [data-testid="stDownloadButton"] button {
            background: var(--monx-pink-hot) !important;
            color: #050505 !important;
            border: 1px solid var(--monx-pink-hot) !important;
            border-radius: 6px !important;
            font-weight: 700 !important;
        }
        div.stButton > button[kind="primary"]:hover,
        [data-testid="stFormSubmitButton"] button[kind="primary"]:hover,
        [data-testid="stDownloadButton"] button:hover {
            background: var(--monx-orange) !important;
            border-color: var(--monx-orange) !important;
        }
        [data-testid="stExpander"],
        [data-testid="stAlert"],
        [data-testid="stForm"] {
            background: rgba(0, 0, 0, 0.58) !important;
            border: 1px solid var(--monx-faint) !important;
            border-radius: 8px !important;
        }
        [data-testid="stAlert"] * {
            color: var(--monx-ink) !important;
        }
        div[role="dialog"],
        [data-testid="stDialog"] {
            background:
                linear-gradient(135deg, transparent 0 42%, rgba(217, 87, 159, 0.16) 42.1% 42.35%, transparent 42.6%),
                linear-gradient(64deg, transparent 0 61%, rgba(255, 139, 43, 0.13) 61.1% 61.35%, transparent 61.6%),
                #050505 !important;
            color: var(--monx-ink) !important;
            border: 2px solid var(--monx-pink-hot) !important;
            border-radius: 8px !important;
            box-shadow: 0 18px 70px rgba(0, 0, 0, 0.62) !important;
        }
        div[role="dialog"] *,
        [data-testid="stDialog"] * {
            color: var(--monx-ink) !important;
        }
        div[role="dialog"] h1,
        div[role="dialog"] h2,
        div[role="dialog"] h3,
        [data-testid="stDialog"] h1,
        [data-testid="stDialog"] h2,
        [data-testid="stDialog"] h3 {
            color: var(--monx-ink) !important;
            font-family: var(--monx-font-display);
            font-weight: 840;
            text-transform: none;
        }
        div[role="dialog"] p,
        div[role="dialog"] li,
        [data-testid="stDialog"] p,
        [data-testid="stDialog"] li {
            color: #e7e1dc !important;
        }
        div[role="dialog"] button,
        [data-testid="stDialog"] button {
            border-radius: 6px !important;
        }
        div[role="dialog"] button[aria-label="Close"],
        [data-testid="stDialog"] button[aria-label="Close"] {
            background: transparent !important;
            border: 1px solid rgba(240, 90, 166, 0.7) !important;
            color: var(--monx-ink) !important;
        }
        div[role="dialog"] div.stButton > button[kind="primary"],
        [data-testid="stDialog"] div.stButton > button[kind="primary"] {
            background: var(--monx-pink-hot) !important;
            color: #050505 !important;
            border-color: var(--monx-pink-hot) !important;
        }
        a {
            color: var(--monx-orange);
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    render_sidebar_nav()


def heading(kicker: str, title: str, body: str = "") -> None:
    st.markdown(f"<div class='monx-kicker'>{kicker}</div>", unsafe_allow_html=True)
    st.title(title)
    if body:
        st.markdown(f"<p class='monx-muted'>{body}</p>", unsafe_allow_html=True)


def status_pill(label: str, ok: bool) -> None:
    color = "#d9579f" if ok else "#ef524c"
    st.markdown(
        f"<span style='border:1px solid {color};color:{color};border-radius:8px;padding:0.2rem 0.5rem'>{label}</span>",
        unsafe_allow_html=True,
    )


def render_system_status(repo_ready: bool, session_ready: bool) -> None:
    with st.sidebar:
        st.caption("System")
        status_pill("Notion connected" if repo_ready else "Notion not connected", repo_ready)
        st.write("")
        status_pill("Session found" if session_ready else "Session pending", session_ready)
