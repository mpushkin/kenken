"""Canonical SVG serialization."""

from __future__ import annotations

from kenken.rendering.scene import Color, FillRect, Scene


def serialize_svg(scene: Scene) -> bytes:
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 '
            f'{scene.width} {scene.height}" width="{_points(scene.width)}pt" '
            f'height="{_points(scene.height)}pt">'
        ),
    ]
    for operation in scene.operations:
        if isinstance(operation, FillRect):
            parts.append(
                f'<rect x="{operation.x}" y="{operation.y}" '
                f'width="{operation.width}" height="{operation.height}" '
                f'fill="{_color(operation.color)}"/>'
            )
            continue
        points = " ".join(f"{x},{y}" for x, y in operation.points)
        element = "polygon" if operation.closed else "polyline"
        parts.append(
            f'<{element} points="{points}" fill="none" '
            f'stroke="{_color(operation.color)}" stroke-width="{operation.width}" '
            'stroke-linecap="round" stroke-linejoin="round"/>'
        )
    parts.append("</svg>")
    return ("\n".join(parts) + "\n").encode()


def _color(color: Color) -> str:
    return f"rgb({color[0]},{color[1]},{color[2]})"


def _points(thousandths: int) -> str:
    whole, remainder = divmod(thousandths, 1_000)
    if remainder == 0:
        return str(whole)
    return f"{whole}.{remainder:03d}".rstrip("0")
