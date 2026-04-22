from __future__ import annotations

import streamlit as st

from config import settings
from infra.app_context import get_active_session, get_notion_repo
from ui import apply_theme, heading, render_system_status, set_page


set_page("Backbone", "■")
apply_theme()

repo = get_notion_repo()
session = get_active_session(repo)
render_system_status(
    bool(repo), bool(session.get("id") or session.get("status") == "local")
)

heading(
    "backend overview",
    "Keep the collective infrastructure legible.",
    "This page is for operators: database wiring, session state, and the next implementation checkpoints.",
)

col_a, col_b, col_c = st.columns(3)
col_a.metric("Session", session.get("code") or "MONX26")
col_b.metric("Database", "connected" if repo else "local")
col_c.metric("Mode", "debug" if settings.debug else "standard")

st.subheader("Database wiring")
rows = [
    ("sessions", settings.sessions_db_id),
    ("players", settings.players_db_id),
    ("responses", settings.responses_db_id),
    ("proposals", settings.proposals_db_id),
    ("decisions", settings.decisions_db_id),
]
for name, value in rows:
    st.write(f"`{name}`: {'configured' if value else 'missing'}")

st.subheader("Next checkpoints")
st.checkbox("Notion databases created and shared with integration", value=bool(repo))
st.checkbox("Audience response schema finalized", value=bool(settings.responses_db_id))
st.checkbox("Proposal lifecycle states agreed", value=False)
st.checkbox("Decision thresholds and facilitation rules agreed", value=False)
st.checkbox("Public-facing copy and visual identity pass", value=False)

if settings.debug:
    st.subheader("Session payload")
    st.json(session)
