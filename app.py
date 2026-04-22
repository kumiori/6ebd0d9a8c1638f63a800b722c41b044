from __future__ import annotations

from typing import Any, Dict

import streamlit as st

from infra.app_context import (
    actor_name,
    get_active_session,
    get_Database_repo,
    set_actor_name,
)
from infra.key_codec import split_emoji_symbols
from services.access_keys import mint_access_key
from ui import apply_theme, heading, render_system_status, set_page

MINT_RESULT_KEY = "monx26_splash_mint_result"
SHOW_MINT_DIALOG_KEY = "monx26_splash_show_mint_dialog"
SHOW_MINT_FORM_KEY = "monx26_splash_show_mint_form"
MINT_JUST_COMPLETED_KEY = "monx26_splash_mint_just_completed"


@st.dialog("Create your access key")
def _render_mint_info_dialog() -> None:
    st.markdown(
        """
This platform is designed for transparent collective work with lightweight anonymity.

You will create a unique access key. It lets the system connect your signals, proposals, and decisions across sessions without forcing a public identity.

Optional details can make the experience easier:

- Name or nickname, so the room can greet you when you return.
- Intention, so facilitators understand why you are entering.
- Email, only if you want a credential reminder later.
"""
    )
    if st.button(
        "Understood, create the key", type="primary", use_container_width=True
    ):
        st.session_state[SHOW_MINT_FORM_KEY] = True
        st.session_state[SHOW_MINT_DIALOG_KEY] = False
        st.rerun()


def _persist_player(
    repo: Any,
    session: Dict[str, Any],
    mint_result: Dict[str, Any],
    nickname: str,
    intent: str,
    email: str,
) -> None:
    if not repo or not repo.players_db_id:
        return
    symbols = split_emoji_symbols(str(mint_result.get("emoji", "")))
    repo.create_player(
        access_key=str(mint_result.get("access_key", "")),
        nickname=nickname,
        role="Participant",
        emoji=str(mint_result.get("emoji", "")),
        phrase=str(mint_result.get("phrase", "")),
        emoji_suffix_4="".join(symbols[-4:]) if len(symbols) >= 4 else "",
        emoji_suffix_6="".join(symbols[-6:]) if len(symbols) >= 6 else "",
        intent=intent,
        email=email,
        session_id=str(session.get("id", "")),
    )


def _render_mint_panel(repo: Any, session: Dict[str, Any]) -> None:
    if not bool(st.session_state.get(SHOW_MINT_FORM_KEY)):
        return

    with st.container(border=True):
        st.markdown("### Add optional details to your key")
        with st.form("monx26-splash-mint-token-form"):
            mint_name = st.text_input("Name or nickname", key="monx26-splash-mint-name")
            mint_intent = st.text_input(
                "Why are you joining this collective space?",
                key="monx26-splash-mint-intent",
                max_chars=160,
            )
            mint_email = st.text_input(
                "Email (optional, only for credential reminder)",
                key="monx26-splash-mint-email",
            )
            mint_submit = st.form_submit_button(
                "Generate Access Key",
                type="primary",
                use_container_width=True,
            )

        if not mint_submit:
            return

        with st.status("Minting access key...", expanded=True) as status:
            status.update(label="Generating anonymous credential", state="running")
            mint_result = mint_access_key(nickname=mint_name, role="Participant")
            status.update(label="Building access card", state="running")
            try:
                _persist_player(
                    repo, session, mint_result, mint_name, mint_intent, mint_email
                )
                if repo and repo.players_db_id:
                    status.update(label="Saved to Database", state="running")
            except Exception as exc:
                status.update(label="Key created, Database save failed", state="error")
                st.warning(
                    f"Key created locally, but Database persistence failed: {exc}"
                )
            st.session_state[MINT_RESULT_KEY] = mint_result
            st.session_state["monx26_access_key"] = mint_result["access_key"]
            set_actor_name(mint_name)
            status.update(label="Minting complete", state="complete")
        st.session_state[SHOW_MINT_FORM_KEY] = False
        st.session_state[SHOW_MINT_DIALOG_KEY] = False
        st.session_state[MINT_JUST_COMPLETED_KEY] = True
        st.rerun()


def _render_mint_result() -> None:
    mint_result = st.session_state.get(MINT_RESULT_KEY)
    if not mint_result:
        return

    st.success(
        "Your access key is ready. You can now continue to the collective space."
    )
    st.markdown("### Your key shortcut")
    st.markdown(
        f"<div style='font-size:4.1rem;line-height:1.2;text-align:center'>{mint_result.get('emoji4', '-')}</div>",
        unsafe_allow_html=True,
    )
    st.caption(
        "A unique 22-emoji access key has been generated. The last four emojis are the handy shortcut. "
        "Download the full card and keep it somewhere safe."
    )
    st.download_button(
        "Download Access Card",
        data=mint_result.get("pdf_bytes", b""),
        file_name=mint_result.get("filename", "monx26-key.pdf"),
        mime="application/pdf",
        use_container_width=True,
        key="monx26-splash-mint-download-pdf",
    )
    st.page_link(
        "pages/01_Participate.py", label="Continue to audience interaction", icon="🗣️"
    )


set_page("Home", "◼")
apply_theme()

repo = get_Database_repo()
session = get_active_session(repo)
render_system_status(
    bool(repo), bool(session.get("id") or session.get("status") == "local")
)
st.session_state.setdefault(MINT_RESULT_KEY, None)
st.session_state.setdefault(SHOW_MINT_FORM_KEY, False)
st.session_state.setdefault(SHOW_MINT_DIALOG_KEY, False)
st.session_state.setdefault(MINT_JUST_COMPLETED_KEY, False)

heading(
    "monx26 backbone",
    "Collective decisions need a living instrument.",
    "This is the operational surface for audience interaction, coordination, proposals, and decisions.",
)

if (
    not st.session_state.get(SHOW_MINT_FORM_KEY)
    and not st.session_state.get(MINT_RESULT_KEY)
    and not st.session_state.get(SHOW_MINT_DIALOG_KEY)
):
    st.session_state[SHOW_MINT_DIALOG_KEY] = True

if bool(st.session_state.get(SHOW_MINT_DIALOG_KEY)):
    _render_mint_info_dialog()
_render_mint_panel(repo, session)
_render_mint_result()
if st.session_state.pop(MINT_JUST_COMPLETED_KEY, False):
    st.balloons()

st.markdown(
    """
<section class="monx-manifesto">
  <div class="monx-manifesto__label">COLLETTIVO MONX26</div>
  <p>
    <strong>Monx26</strong> est un collectif né du partage des arts. MONX,
    Monasteriolum, d’orchestration de nœuds et concepts expérimentaux, est une
    base temporelle, une discipline légère de liberté commune d’introspection et
    de recherche. C’est avant tout un retour aux origines de Montreuil.
  </p>
  <p>
    L’objectif est d’offrir une orchestration et une coordination sans
    hiérarchie. Le leitmotiv ? Les nœuds, qui se mélangent, s’entrechoquent et se
    complètent.
  </p>
  <p>
    MONX, c’est la volonté de créer et de promouvoir des arts expérimentaux
    accessibles à tous et partagés par tous. 26 est également un nombre clé :
    l’année de notre création et, en même temps, l’allégorie des vingt-six
    lettres de l’alphabet, témoignant de notre volonté d’ouverture et de
    production pluridisciplinaire.
  </p>
  <p class="monx-manifesto__closing">
    L’autonomie, la communauté et l’orchestration sont nos impulsions.
  </p>
</section>
""",
    unsafe_allow_html=True,
)

left, right = st.columns([1.15, 0.85], gap="large")

with left:
    st.subheader("Enter the room")
    st.write(
        "Use this app to register presence, send signals, make proposals, and follow collective decisions as they evolve."
    )
    name = st.text_input(
        "Name or handle", value=actor_name(), placeholder="anonymous is allowed"
    )
    if st.button("Remember me", use_container_width=True):
        set_actor_name(name)
        st.success("Presence remembered for this browser session.")

    st.divider()
    st.page_link("pages/01_Participate.py", label="Audience interaction", icon="🗣️")
    st.page_link("pages/02_Decisions.py", label="Decision room", icon="⚖️")
    st.page_link("pages/03_Backbone.py", label="Backbone overview", icon="🧭")

with right:
    st.markdown("<div class='monx-panel'>", unsafe_allow_html=True)
    st.subheader("Current session")
    st.metric("Code", session.get("code") or "MONX26")
    st.write(f"Status: `{session.get('status') or 'unknown'}`")
    if not repo:
        st.info("Database is not configured yet. The app is running in local mode.")
    elif not session.get("id"):
        st.warning("Database is connected, but no active/default session was found.")
    else:
        st.success("Database session is connected.")
    st.markdown("</div>", unsafe_allow_html=True)

st.caption(
    "Built from the proven Streamlit + Database architecture used in app_affranchis and app_iceicebaby."
)
