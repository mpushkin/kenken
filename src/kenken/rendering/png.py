"""Dependency-free deterministic RGB PNG backend."""

from __future__ import annotations

import struct
import zlib
from itertools import pairwise

from kenken.rendering.scene import Color, FillRect, Scene


def serialize_png(scene: Scene, width: int, height: int) -> bytes:
    if width <= 0 or height <= 0:
        raise ValueError("PNG dimensions must be positive")
    pixels = bytearray(b"\xff" * (width * height * 3))

    def sx(value: int) -> int:
        return value * width // scene.width

    def sy(value: int) -> int:
        return value * height // scene.height

    def fill(
        x: int,
        y: int,
        rectangle_width: int,
        rectangle_height: int,
        color: Color,
    ) -> None:
        left = max(0, x)
        top = max(0, y)
        right = min(width, x + max(1, rectangle_width))
        bottom = min(height, y + max(1, rectangle_height))
        if right <= left or bottom <= top:
            return
        scanline = bytes(color) * (right - left)
        for row in range(top, bottom):
            start = (row * width + left) * 3
            pixels[start : start + len(scanline)] = scanline

    def paint_disc(center_x: int, center_y: int, radius: int, color: Color) -> None:
        radius_squared = radius * radius
        for paint_y in range(center_y - radius, center_y + radius + 1):
            distance_y = paint_y - center_y
            for paint_x in range(center_x - radius, center_x + radius + 1):
                distance_x = paint_x - center_x
                if distance_x * distance_x + distance_y * distance_y <= radius_squared:
                    fill(paint_x, paint_y, 1, 1, color)

    def stroke_segment(
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        stroke_width: int,
        color: Color,
    ) -> None:
        radius = max(0, (stroke_width - 1) // 2)
        delta_x = abs(x2 - x1)
        step_x = 1 if x1 < x2 else -1
        delta_y = -abs(y2 - y1)
        step_y = 1 if y1 < y2 else -1
        error = delta_x + delta_y
        while True:
            if radius:
                paint_disc(x1, y1, radius, color)
            else:
                fill(x1, y1, 1, 1, color)
            if x1 == x2 and y1 == y2:
                break
            doubled = 2 * error
            if doubled >= delta_y:
                error += delta_y
                x1 += step_x
            if doubled <= delta_x:
                error += delta_x
                y1 += step_y

    for operation in scene.operations:
        if isinstance(operation, FillRect):
            fill(
                sx(operation.x),
                sy(operation.y),
                max(1, sx(operation.x + operation.width) - sx(operation.x)),
                max(1, sy(operation.y + operation.height) - sy(operation.y)),
                operation.color,
            )
            continue
        points = tuple((sx(x), sy(y)) for x, y in operation.points)
        stroke_width = max(
            1,
            min(
                operation.width * width // scene.width,
                operation.width * height // scene.height,
            ),
        )
        segments = tuple(pairwise(points))
        if operation.closed:
            segments += ((points[-1], points[0]),)
        for (x1, y1), (x2, y2) in segments:
            stroke_segment(x1, y1, x2, y2, stroke_width, operation.color)

    rows = b"".join(
        b"\x00" + pixels[row * width * 3 : (row + 1) * width * 3] for row in range(height)
    )
    return (
        b"\x89PNG\r\n\x1a\n"
        + _chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
        + _chunk(b"IDAT", _stored_zlib(rows))
        + _chunk(b"IEND", b"")
    )


def _chunk(kind: bytes, data: bytes) -> bytes:
    body = kind + data
    return struct.pack(">I", len(data)) + body + struct.pack(">I", zlib.crc32(body))


def _stored_zlib(data: bytes) -> bytes:
    """Return a byte-stable zlib stream using uncompressed DEFLATE blocks."""
    result = bytearray(b"\x78\x01")
    for offset in range(0, max(1, len(data)), 65_535):
        block = data[offset : offset + 65_535]
        final = offset + len(block) >= len(data)
        result.append(1 if final else 0)
        result.extend(struct.pack("<HH", len(block), len(block) ^ 0xFFFF))
        result.extend(block)
    result.extend(struct.pack(">I", zlib.adler32(data)))
    return bytes(result)
