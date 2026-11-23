"""Deterministic puzzle and page renderers."""

from kenken.rendering.page import compose_page, standalone_page
from kenken.rendering.pdf import serialize_pdf, serialize_pdf_pages
from kenken.rendering.png import serialize_png
from kenken.rendering.puzzle import puzzle_scene
from kenken.rendering.svg import serialize_svg

__all__ = [
    "compose_page",
    "puzzle_scene",
    "serialize_pdf",
    "serialize_pdf_pages",
    "serialize_png",
    "serialize_svg",
    "standalone_page",
]
