from __future__ import annotations

import streamlit as st

from infra.app_context import (
    actor_name,
    ensure_device_id,
    get_active_session,
    get_notion_repo,
    set_actor_name,
)
from ui import apply_theme, heading, render_system_status, set_page


set_page("Participate", "○")
apply_theme()

repo = get_notion_repo()
session = get_active_session(repo)
device_id = ensure_device_id()
render_system_status(
    bool(repo), bool(session.get("id") or session.get("status") == "local")
)

heading(
    "audience interface",
    "Send a signal into the collective field.",
    "Presence, proposals, needs, offers, and friction points should be captured while they are still alive.",
)

name = st.text_input("Name or handle", value=actor_name(), placeholder="anonymous")
set_actor_name(name)

kind = st.selectbox(
    "What are you sending?",
    ["presence", "proposal", "need", "offer", "friction", "question", "signal"],
)
content = st.text_area(
    "Message",
    placeholder="Write the thing that should enter the room.",
    height=140,
)

col_a, col_b = st.columns([1, 1])
with col_a:
    intensity = st.slider("Intensity", 0, 10, 5)
with col_b:
    visibility = st.selectbox("Visibility", ["public", "facilitation", "private note"])

payload = {
    "device_id": device_id,
    "intensity": intensity,
    "visibility": visibility,
    "session_code": session.get("code", "MONX26"),
}

if st.button("Send", type="primary", use_container_width=True):
    if not content.strip():
        st.error("Write a message first.")
    elif repo and repo.responses_db_id:
        repo.create_response(
            session_id=session.get("id", ""),
            kind=kind,
            content=content.strip(),
            actor=name.strip(),
            payload=payload,
        )
        st.success("Sent to Database.")
    else:
        st.session_state.setdefault("monx26_local_responses", []).append(
            {
                "kind": kind,
                "content": content.strip(),
                "actor": name.strip(),
                "payload": payload,
            }
        )
        st.success("Saved locally for this session. Configure Database to persist it.")

with st.expander("Local session buffer", expanded=False):
    st.json(st.session_state.get("monx26_local_responses", []))
