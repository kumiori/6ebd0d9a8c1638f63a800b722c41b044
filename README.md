# monx26 collective backbone

Streamlit application for the monx26 collective.

The app is designed as two connected surfaces:

- an audience-facing interface for presence, interaction, proposals, and coordination;
- a backend surface for collective decision making, moderation, and operational overview.

Notion is the primary database layer. The implementation reuses the architecture proven in sibling apps: thin repositories, explicit session context, and Streamlit pages organized by flow.

The home page also reuses the tested splash pattern:

- automatic access-key explanation dialog;
- optional nickname, intention, and email fields;
- 128-bit access key projected as emoji and passphrase;
- downloadable PDF access card;
- Notion player persistence when `monx26_players_db_id` is configured.

## Run locally

```bash
streamlit run app.py
```

## Streamlit secrets

Create `.streamlit/secrets.toml` locally with:

```toml
[notion]
token = "secret_xxx"
monx26_sessions_db_id = ""
monx26_players_db_id = ""
monx26_responses_db_id = ""
monx26_proposals_db_id = ""
monx26_decisions_db_id = ""
default_session_code = "MONX26"

[cookie]
name = "monx26"
key = "replace-with-a-long-random-string"
expiry_days = 30
```

The repository also accepts environment variables with the same names in uppercase:

- `NOTION_TOKEN`
- `MONX26_SESSIONS_DB_ID`
- `MONX26_PLAYERS_DB_ID`
- `MONX26_RESPONSES_DB_ID`
- `MONX26_PROPOSALS_DB_ID`
- `MONX26_DECISIONS_DB_ID`
- `MONX26_DEFAULT_SESSION_CODE`

## Notion entities

Initial contract:

- `sessions`: collective gatherings, assemblies, public activations, or working sessions.
- `players`: people, members, guests, organizers, and recurring audience identities.
- `responses`: raw interaction events and form submissions.
- `proposals`: things that can be discussed, amended, voted on, or coordinated around.
- `decisions`: accepted, rejected, delegated, or pending decisions.

The schema helpers are intentionally tolerant: they use common property names when present and degrade gracefully while the Notion databases are still being shaped.
