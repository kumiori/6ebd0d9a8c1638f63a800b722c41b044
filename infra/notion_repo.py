from __future__ import annotations

import json
import re
import time
from datetime import datetime, timezone
from functools import lru_cache
from typing import Any, Dict, List, Optional

import streamlit as st

try:
    from notion_client import Client
    from notion_client.errors import APIResponseError
except ImportError:  # pragma: no cover
    Client = Any  # type: ignore

    class APIResponseError(Exception):  # type: ignore
        status: int = 0


HASH_FUNCS: Dict[Any, Any] = {}
if isinstance(Client, type):
    HASH_FUNCS[Client] = lambda _: 0


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _clean_notion_id(value: Optional[str]) -> str:
    raw = (value or "").strip().strip("\"'")
    if not raw:
        return ""
    dashed = re.search(
        r"([0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12})",
        raw,
    )
    if dashed:
        return dashed.group(1).lower()
    compact = re.search(r"([0-9a-fA-F]{32})", raw)
    if compact:
        token = compact.group(1).lower()
        return f"{token[0:8]}-{token[8:12]}-{token[12:16]}-{token[16:20]}-{token[20:32]}"
    return raw


def _execute_with_retry(func: Any, *args: Any, **kwargs: Any) -> Any:
    last_error: Optional[Exception] = None
    for attempt in range(3):
        try:
            return func(*args, **kwargs)
        except APIResponseError as err:  # type: ignore[misc]
            last_error = err
            if getattr(err, "status", None) != 429 or attempt == 2:
                break
            time.sleep(0.5 * (2**attempt))
    if last_error:
        raise last_error
    raise RuntimeError("Notion request failed.")


@lru_cache(maxsize=128)
def _resolve_data_source_id(client: Client, database_or_source_id: str) -> str:
    clean_id = _clean_notion_id(database_or_source_id)
    if not clean_id:
        return ""

    databases_endpoint = getattr(client, "databases", None)
    db_retrieve = getattr(databases_endpoint, "retrieve", None) if databases_endpoint else None
    if callable(db_retrieve):
        try:
            db = _execute_with_retry(db_retrieve, clean_id)
            data_sources = db.get("data_sources", []) if isinstance(db, dict) else []
            if data_sources and isinstance(data_sources[0], dict):
                return _clean_notion_id(data_sources[0].get("id")) or clean_id
            return clean_id
        except Exception:
            pass

    data_sources_endpoint = getattr(client, "data_sources", None)
    ds_retrieve = getattr(data_sources_endpoint, "retrieve", None) if data_sources_endpoint else None
    if callable(ds_retrieve):
        try:
            _execute_with_retry(ds_retrieve, clean_id)
            return clean_id
        except Exception:
            pass
    return clean_id


@st.cache_data(ttl=10, show_spinner=False, hash_funcs=HASH_FUNCS)
def _cached_query(client: Client, database_id: str, **kwargs: Any) -> Dict[str, Any]:
    data_source_id = _resolve_data_source_id(client, database_id)
    if not data_source_id:
        return {"results": []}
    data_sources_endpoint = getattr(client, "data_sources", None)
    ds_query = getattr(data_sources_endpoint, "query", None) if data_sources_endpoint else None
    if not callable(ds_query):
        raise AttributeError("notion-client 3.x with data_sources.query is required.")
    return _execute_with_retry(ds_query, data_source_id=data_source_id, **kwargs)


def clear_notion_cache() -> None:
    _cached_query.clear()
    _resolve_data_source_id.cache_clear()


def _title(value: str) -> Dict[str, Any]:
    return {"title": [{"type": "text", "text": {"content": value[:2000]}}]}


def _rich_text(value: str) -> Dict[str, Any]:
    return {"rich_text": [{"type": "text", "text": {"content": value[:2000]}}]}


def _select(value: str) -> Dict[str, Any]:
    return {"select": {"name": value[:100]}}


def _date(value: str) -> Dict[str, Any]:
    return {"date": {"start": value}}


def _relation(page_id: str) -> Dict[str, Any]:
    return {"relation": [{"id": page_id}]} if page_id else {"relation": []}


def _extract_text(prop: Dict[str, Any]) -> str:
    values = prop.get("title") or prop.get("rich_text") or []
    if not isinstance(values, list):
        return ""
    return "".join(str(item.get("plain_text", "")) for item in values if isinstance(item, dict))


def _extract_select(prop: Dict[str, Any]) -> str:
    select = prop.get("select") if isinstance(prop, dict) else None
    return str(select.get("name", "")) if isinstance(select, dict) else ""


class NotionRepo:
    def __init__(
        self,
        client: Client,
        sessions_db_id: str = "",
        players_db_id: str = "",
        responses_db_id: str = "",
        proposals_db_id: str = "",
        decisions_db_id: str = "",
    ) -> None:
        self.client = client
        self.sessions_db_id = sessions_db_id
        self.players_db_id = players_db_id
        self.responses_db_id = responses_db_id
        self.proposals_db_id = proposals_db_id
        self.decisions_db_id = decisions_db_id

    def is_ready(self) -> bool:
        return bool(self.client)

    def query(self, database_id: str, **kwargs: Any) -> List[Dict[str, Any]]:
        if not database_id:
            return []
        payload = _cached_query(self.client, database_id, **kwargs)
        return list(payload.get("results", []))

    def get_active_session(self, default_code: str = "MONX26") -> Optional[Dict[str, Any]]:
        if not self.sessions_db_id:
            return {"id": "", "code": default_code, "name": default_code, "status": "local"}
        filters = [
            {"property": "status", "select": {"equals": "active"}},
            {"property": "code", "rich_text": {"equals": default_code}},
        ]
        for filter_payload in filters:
            results = self.query(self.sessions_db_id, filter=filter_payload, page_size=1)
            if results:
                return self._page_summary(results[0])
        return None

    def list_proposals(self, limit: int = 20) -> List[Dict[str, Any]]:
        return [self._page_summary(page) for page in self.query(self.proposals_db_id, page_size=limit)]

    def list_decisions(self, limit: int = 20) -> List[Dict[str, Any]]:
        return [self._page_summary(page) for page in self.query(self.decisions_db_id, page_size=limit)]

    def create_response(
        self,
        session_id: str,
        kind: str,
        content: str,
        actor: str = "",
        payload: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        if not self.responses_db_id:
            return None
        properties = {
            "Name": _title(f"{kind} · {actor or 'anonymous'} · {_now_iso()}"),
            "kind": _select(kind),
            "content": _rich_text(content),
            "actor": _rich_text(actor),
            "payload_json": _rich_text(json.dumps(payload or {}, ensure_ascii=False)),
            "created_at": _date(_now_iso()),
        }
        if session_id:
            properties["session"] = _relation(session_id)
        page = self.client.pages.create(parent={"database_id": self.responses_db_id}, properties=properties)
        clear_notion_cache()
        return str(page.get("id", ""))

    def create_proposal(
        self,
        title: str,
        body: str,
        proposer: str = "",
        session_id: str = "",
    ) -> Optional[str]:
        if not self.proposals_db_id:
            return None
        properties = {
            "Name": _title(title),
            "status": _select("new"),
            "body": _rich_text(body),
            "proposer": _rich_text(proposer),
            "created_at": _date(_now_iso()),
        }
        if session_id:
            properties["session"] = _relation(session_id)
        page = self.client.pages.create(parent={"database_id": self.proposals_db_id}, properties=properties)
        clear_notion_cache()
        return str(page.get("id", ""))

    def create_player(
        self,
        *,
        access_key: str,
        nickname: str = "",
        role: str = "Participant",
        emoji: str = "",
        phrase: str = "",
        emoji_suffix_4: str = "",
        emoji_suffix_6: str = "",
        intent: str = "",
        email: str = "",
        session_id: str = "",
    ) -> Optional[str]:
        if not self.players_db_id:
            return None
        properties: Dict[str, Any] = {
            "Name": _title(nickname or "anonymous"),
            "access_key": _rich_text(access_key),
            "nickname": _rich_text(nickname),
            "role": _select(role),
            "emoji": _rich_text(emoji),
            "phrase": _rich_text(phrase),
            "emoji_suffix_4": _rich_text(emoji_suffix_4),
            "emoji_suffix_6": _rich_text(emoji_suffix_6),
            "intent": _rich_text(intent),
            "created_at": _date(_now_iso()),
        }
        if email:
            properties["email"] = {"email": email}
        if session_id:
            properties["session"] = _relation(session_id)
        page = self.client.pages.create(parent={"database_id": self.players_db_id}, properties=properties)
        clear_notion_cache()
        return str(page.get("id", ""))

    @staticmethod
    def _page_summary(page: Dict[str, Any]) -> Dict[str, Any]:
        props = page.get("properties", {}) if isinstance(page, dict) else {}
        name = ""
        for candidate in ("Name", "title", "name"):
            if candidate in props:
                name = _extract_text(props[candidate])
                break
        return {
            "id": str(page.get("id", "")),
            "name": name or "Untitled",
            "code": _extract_text(props.get("code", {})),
            "status": _extract_select(props.get("status", {})),
            "body": _extract_text(props.get("body", {})),
            "created_at": props.get("created_at", {}).get("date", {}).get("start", ""),
        }


def init_notion_repo(
    token: str,
    sessions_db_id: str = "",
    players_db_id: str = "",
    responses_db_id: str = "",
    proposals_db_id: str = "",
    decisions_db_id: str = "",
) -> Optional[NotionRepo]:
    if not token or not isinstance(Client, type):
        return None
    client = Client(auth=token)
    return NotionRepo(
        client=client,
        sessions_db_id=sessions_db_id,
        players_db_id=players_db_id,
        responses_db_id=responses_db_id,
        proposals_db_id=proposals_db_id,
        decisions_db_id=decisions_db_id,
    )
