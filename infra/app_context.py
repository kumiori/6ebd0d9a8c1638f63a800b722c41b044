from __future__ import annotations

from typing import Any, Dict, Optional

import streamlit as st

from config import settings
from infra.notion_repo import NotionRepo, init_notion_repo


@st.cache_resource(show_spinner=False)
def get_notion_repo() -> Optional[NotionRepo]:
    return init_notion_repo(
        token=settings.notion_token,
        sessions_db_id=settings.sessions_db_id,
        players_db_id=settings.players_db_id,
        responses_db_id=settings.responses_db_id,
        proposals_db_id=settings.proposals_db_id,
        decisions_db_id=settings.decisions_db_id,
    )


def get_active_session(repo: Optional[NotionRepo]) -> Dict[str, Any]:
    if not repo:
        return {
            "id": "",
            "code": settings.default_session_code,
            "name": settings.default_session_code,
            "status": "local",
        }
    return repo.get_active_session(settings.default_session_code) or {
        "id": "",
        "code": settings.default_session_code,
        "name": settings.default_session_code,
        "status": "missing",
    }


def ensure_device_id() -> str:
    if "monx26_device_id" not in st.session_state:
        import uuid

        st.session_state["monx26_device_id"] = str(uuid.uuid4())
    return str(st.session_state["monx26_device_id"])


def actor_name() -> str:
    return str(st.session_state.get("monx26_actor", "")).strip()


def set_actor_name(value: str) -> None:
    st.session_state["monx26_actor"] = value.strip()
