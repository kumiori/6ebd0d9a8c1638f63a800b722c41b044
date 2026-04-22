from __future__ import annotations

import streamlit as st

from infra.app_context import actor_name, get_active_session, get_notion_repo
from ui import apply_theme, heading, render_system_status, set_page


set_page("Decisions", "◆")
apply_theme()

repo = get_notion_repo()
session = get_active_session(repo)
render_system_status(bool(repo), bool(session.get("id") or session.get("status") == "local"))

heading(
    "decision backend",
    "Proposals become decisions through visible movement.",
    "Start with lightweight proposals now; voting, amendment, delegation, and consent thresholds can lock onto the same records next.",
)

tab_new, tab_current, tab_done = st.tabs(["New proposal", "Open proposals", "Decisions"])

with tab_new:
    title = st.text_input("Proposal title", placeholder="What should the collective decide?")
    body = st.text_area("Proposal body", placeholder="Context, tradeoffs, concrete ask.", height=180)
    proposer = st.text_input("Proposer", value=actor_name(), placeholder="name or working group")
    if st.button("Create proposal", type="primary", use_container_width=True):
        if not title.strip():
            st.error("A proposal needs a title.")
        elif repo and repo.proposals_db_id:
            repo.create_proposal(
                title=title.strip(),
                body=body.strip(),
                proposer=proposer.strip(),
                session_id=session.get("id", ""),
            )
            st.success("Proposal created in Notion.")
        else:
            st.session_state.setdefault("monx26_local_proposals", []).append(
                {"name": title.strip(), "body": body.strip(), "status": "new", "proposer": proposer.strip()}
            )
            st.success("Proposal saved locally for this session.")

with tab_current:
    proposals = repo.list_proposals() if repo and repo.proposals_db_id else st.session_state.get("monx26_local_proposals", [])
    if not proposals:
        st.info("No proposals found yet.")
    for proposal in proposals:
        with st.container(border=True):
            st.subheader(proposal.get("name", "Untitled"))
            st.caption(proposal.get("status") or "new")
            if proposal.get("body"):
                st.write(proposal.get("body"))

with tab_done:
    decisions = repo.list_decisions() if repo and repo.decisions_db_id else []
    if not decisions:
        st.info("No decisions found yet.")
    for decision in decisions:
        with st.container(border=True):
            st.subheader(decision.get("name", "Untitled"))
            st.caption(decision.get("status") or "recorded")
            if decision.get("body"):
                st.write(decision.get("body"))
