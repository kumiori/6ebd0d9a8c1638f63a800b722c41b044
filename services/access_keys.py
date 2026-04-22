from __future__ import annotations

from datetime import datetime
from typing import Any, Dict

from infra.credentials_pdf import build_credentials_pdf
from infra.key_codec import generate_hex_key, hex_to_emoji, hex_to_phrase, split_emoji_symbols


def mint_access_key(nickname: str = "", role: str = "Participant") -> Dict[str, Any]:
    access_key = generate_hex_key()
    emoji = hex_to_emoji(access_key)
    phrase = hex_to_phrase(access_key)
    symbols = split_emoji_symbols(emoji)
    suffix4 = "".join(symbols[-4:]) if len(symbols) >= 4 else emoji
    suffix6 = "".join(symbols[-6:]) if len(symbols) >= 6 else emoji
    pdf_bytes = build_credentials_pdf(
        access_key=access_key,
        emoji=emoji,
        phrase=phrase,
        nickname=nickname,
        role=role,
        title="Collective Access Card",
    )
    return {
        "access_key": access_key,
        "emoji": emoji,
        "phrase": phrase,
        "emoji4": suffix4,
        "emoji6": suffix6,
        "pdf_bytes": pdf_bytes,
        "filename": f"monx26-key-{datetime.now().strftime('%Y%m%d-%H%M%S')}.pdf",
    }
