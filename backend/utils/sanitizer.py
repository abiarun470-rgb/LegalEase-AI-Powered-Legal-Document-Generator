import html
import re


REPLACEMENTS = {
    "\u2018": "'",
    "\u2019": "'",
    "\u201c": '"',
    "\u201d": '"',
    "\u2013": "-",
    "\u2014": "-",
    "\u2022": "-",
    "\u00a0": " ",
    "\u2026": "..."
}


def sanitize_text(text: str) -> str:
    """
    Normalize common typographic characters
    and remove control characters.
    """

    for old, new in REPLACEMENTS.items():
        text = text.replace(old, new)

    text = re.sub(
        r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]",
        "",
        text
    )

    return text.strip()


def html_preview(text: str) -> str:
    """
    Safely display generated document text
    as HTML.
    """

    escaped = html.escape(text)

    return (
        '<div '
        'style="'
        'background:#111827;'
        'color:#f3f4f6;'
        'padding:24px;'
        'border-radius:12px;'
        'max-height:650px;'
        'overflow-y:auto;'
        'white-space:pre-wrap;'
        'font-family:Georgia,serif;'
        'line-height:1.65;'
        '">'
        f"{escaped}"
        "</div>"
    )