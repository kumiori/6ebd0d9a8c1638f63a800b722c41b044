from __future__ import annotations

from io import BytesIO
from typing import List

from PIL import Image, ImageDraw, ImageFont

from infra.key_codec import split_emoji_symbols


def _load_font(
    candidates: List[str], size: int
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    for path in candidates:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            continue
    return ImageFont.load_default()


def _pick_emoji_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    return _load_font(
        [
            "/System/Library/Fonts/Apple Color Emoji.ttc",
            "/System/Library/Fonts/Supplemental/Apple Symbols.ttf",
            "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ],
        size,
    )


def _wrap_text(
    draw: ImageDraw.ImageDraw, text: str, font: ImageFont.ImageFont, max_width: int
) -> List[str]:
    if not text:
        return [""]
    lines: List[str] = []
    current = ""
    for word in text.split(" "):
        trial = word if not current else f"{current} {word}"
        if draw.textlength(trial, font=font) <= max_width:
            current = trial
            continue
        if current:
            lines.append(current)
        current = word
    if current:
        lines.append(current)
    return lines or [""]


def build_credentials_pdf(
    *,
    access_key: str,
    emoji: str,
    phrase: str,
    nickname: str,
    role: str,
    title: str = "Access Card",
) -> bytes:
    symbols = split_emoji_symbols(emoji)
    suffix4 = symbols[-4:] if len(symbols) >= 4 else []
    suffix6 = symbols[-6:] if len(symbols) >= 6 else []

    text_font = _load_font(
        [
            "/System/Library/Fonts/Supplemental/Helvetica.ttc",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ],
        18,
    )
    title_font = _load_font(
        [
            "/System/Library/Fonts/Supplemental/Helvetica.ttc",
            "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        ],
        30,
    )
    emoji_font = _pick_emoji_font(26)

    width = 680
    height = 640
    margin = 28
    label_x = margin
    value_x = margin + 150
    max_text_width = width - value_x - margin

    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)
    draw.rectangle([(0, 0), (width, 110)], fill=(238, 242, 236))
    draw.text((margin, 28), "MONX26", fill=(23, 23, 23), font=title_font)
    draw.text((margin, 66), title, fill=(23, 23, 23), font=text_font)

    y = 138
    details = [
        ("Name", nickname or "anonymous"),
        ("Role", role),
        ("Passphrase", phrase.replace("-", " - ")),
        ("Full hash", access_key),
    ]
    for label, value in details:
        draw.text((label_x, y), f"{label}:", fill=(40, 40, 40), font=text_font)
        for line in _wrap_text(draw, value, text_font, max_text_width):
            draw.text((value_x, y), line, fill=(10, 10, 10), font=text_font)
            y += 28
        y += 8

    def draw_tokens(label: str, token_symbols: List[str]) -> None:
        nonlocal y
        if not token_symbols:
            return
        draw.text((label_x, y), label, fill=(40, 40, 40), font=text_font)
        x = value_x
        total = len(token_symbols)
        for idx, symbol in enumerate(token_symbols):
            if x + 72 > width - margin:
                x = value_x
                y += 44
            draw.rounded_rectangle(
                [(x, y), (x + 64, y + 34)],
                radius=8,
                fill=(248, 248, 248),
                outline=(170, 170, 170),
            )
            draw.text((x + 8, y + 3), symbol, fill=(20, 20, 20), font=emoji_font, embedded_color=True)
            draw.text((x + 44, y + 9), str(total - idx), fill=(70, 70, 70), font=text_font)
            x += 72
        y += 48

    draw_tokens("Emoji-4:", suffix4)
    draw_tokens("Emoji-6:", suffix6)
    draw_tokens("Emoji:", symbols)

    draw.line([(margin, height - 58), (width - margin, height - 58)], fill=(23, 23, 23))
    draw.text((margin, height - 42), "Keep this document somewhere safe.", fill=(23, 23, 23), font=text_font)

    buffer = BytesIO()
    image.save(buffer, format="PDF", resolution=150.0)
    return buffer.getvalue()
