"""Minimal deterministic vector PDF backend."""

from __future__ import annotations

from collections.abc import Sequence

from kenken.rendering.scene import Color, FillRect, Scene


def serialize_pdf(scene: Scene) -> bytes:
    return serialize_pdf_pages((scene,))


def serialize_pdf_pages(scenes: Sequence[Scene]) -> bytes:
    """Serialize one or more scenes as a deterministic vector PDF."""
    if not scenes:
        raise ValueError("a PDF requires at least one page")
    page_numbers = tuple(3 + 2 * index for index in range(len(scenes)))
    kids = " ".join(f"{number} 0 R" for number in page_numbers)
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        f"<< /Type /Pages /Kids [{kids}] /Count {len(scenes)} >>".encode(),
    ]
    for scene, page_number in zip(scenes, page_numbers, strict=True):
        stream = _content_stream(scene)
        width = _number(scene.width)
        height = _number(scene.height)
        objects.extend(
            (
                (
                    f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {width} {height}] "
                    f"/Contents {page_number + 1} 0 R /Resources << >> >>"
                ).encode(),
                b"<< /Length "
                + str(len(stream)).encode()
                + b" >>\nstream\n"
                + stream
                + b"endstream",
            )
        )
    return _serialize_objects(objects)


def _content_stream(scene: Scene) -> bytes:
    commands = ["1 J", "1 j"]
    for operation in scene.operations:
        if isinstance(operation, FillRect):
            commands.extend(
                (
                    f"{_pdf_color(operation.color)} rg",
                    (
                        f"{_number(operation.x)} "
                        f"{_number(scene.height - operation.y - operation.height)} "
                        f"{_number(operation.width)} {_number(operation.height)} re f"
                    ),
                )
            )
            continue
        commands.extend(
            (
                f"{_pdf_color(operation.color)} RG",
                f"{_number(operation.width)} w",
                (
                    f"{_number(operation.points[0][0])} "
                    f"{_number(scene.height - operation.points[0][1])} m"
                ),
            )
        )
        commands.extend(
            f"{_number(x)} {_number(scene.height - y)} l" for x, y in operation.points[1:]
        )
        if operation.closed:
            commands.append("h")
        commands.append("S")
    return ("\n".join(commands) + "\n").encode()


def _serialize_objects(objects: list[bytes]) -> bytes:
    result = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for index, item in enumerate(objects, start=1):
        offsets.append(len(result))
        result.extend(f"{index} 0 obj\n".encode())
        result.extend(item)
        result.extend(b"\nendobj\n")
    xref = len(result)
    result.extend(f"xref\n0 {len(objects) + 1}\n".encode())
    result.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        result.extend(f"{offset:010d} 00000 n \n".encode())
    result.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n"
        ).encode()
    )
    return bytes(result)


def _pdf_color(color: Color) -> str:
    return " ".join(_component(component) for component in color)


def _component(component: int) -> str:
    if component == 0:
        return "0"
    if component == 255:
        return "1"
    return f"{component / 255:.5f}".rstrip("0").rstrip(".")


def _number(thousandths: int) -> str:
    whole, remainder = divmod(thousandths, 1_000)
    if remainder == 0:
        return str(whole)
    return f"{whole}.{remainder:03d}".rstrip("0")
