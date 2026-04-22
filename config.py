from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Any

import streamlit as st


def _secret(section: str, key: str, env_key: str = "") -> str:
    env_name = env_key or key.upper()
    if os.getenv(env_name):
        return str(os.getenv(env_name, "")).strip()
    try:
        value: Any = st.secrets.get(section, {}).get(key, "")
    except Exception:
        value = ""
    return str(value or "").strip()


@dataclass(frozen=True)
class Settings:
    app_name: str = "monx26"
    page_title: str = "monx26 collective"
    default_session_code: str = "MONX26"
    notion_token: str = ""
    sessions_db_id: str = ""
    players_db_id: str = ""
    responses_db_id: str = ""
    proposals_db_id: str = ""
    decisions_db_id: str = ""
    debug: bool = False


def load_settings() -> Settings:
    debug_raw = _secret("app", "debug", "MONX26_DEBUG").lower()
    default_session_code = (
        _secret("notion", "monx26_default_session_code", "MONX26_DEFAULT_SESSION_CODE")
        or _secret("notion", "default_session_code", "MONX26_DEFAULT_SESSION_CODE")
        or "MONX26"
    )
    return Settings(
        default_session_code=default_session_code,
        notion_token=_secret("notion", "token", "NOTION_TOKEN"),
        sessions_db_id=_secret("notion", "monx26_sessions_db_id", "MONX26_SESSIONS_DB_ID"),
        players_db_id=_secret("notion", "monx26_players_db_id", "MONX26_PLAYERS_DB_ID"),
        responses_db_id=_secret("notion", "monx26_responses_db_id", "MONX26_RESPONSES_DB_ID"),
        proposals_db_id=_secret("notion", "monx26_proposals_db_id", "MONX26_PROPOSALS_DB_ID"),
        decisions_db_id=_secret("notion", "monx26_decisions_db_id", "MONX26_DECISIONS_DB_ID"),
        debug=debug_raw in {"1", "true", "yes", "on"},
    )


settings = load_settings()
