"""Small project-owned deterministic vector stroke face.

The normalized geometry below is original to this project and distributed
under the terms recorded in ``VECTOR_FONT_LICENSE.txt``. It deliberately uses
only straight strokes so every output backend consumes identical geometry.
"""

from __future__ import annotations

from collections.abc import Iterable

from kenken.rendering.scene import Color, Scene, StrokePath

type GlyphPath = tuple[tuple[int, int], ...]
type Glyph = tuple[GlyphPath, ...]

MINUS = "\N{MINUS SIGN}"
MULTIPLICATION = "\N{MULTIPLICATION SIGN}"
DIVISION = "\N{DIVISION SIGN}"

_W = 500
_H = 700
_ADVANCE = 600
_PROPORTIONAL_ADVANCES: dict[str, int] = {
    " ": 330,
    "I": 360,
    "i": 280,
    "j": 340,
    "l": 330,
    "m": 700,
    "r": 450,
    "t": 450,
    "w": 680,
}


def _paths(*paths: Iterable[tuple[int, int]]) -> Glyph:
    return tuple(tuple(path) for path in paths)


# Coordinates use a 500 by 700 cap-height box. Lowercase input intentionally
# shares this clean single-stroke construction; ascenders and x-height remain
# visually distinct through the supplied paths.
_GLYPHS: dict[str, Glyph] = {
    "0": _paths(
        (
            (100, 0),
            (400, 0),
            (500, 100),
            (500, 600),
            (400, 700),
            (100, 700),
            (0, 600),
            (0, 100),
            (100, 0),
        ),
        ((80, 620), (420, 80)),
    ),
    "1": _paths(((100, 150), (250, 0), (250, 700)), ((80, 700), (430, 700))),
    "2": _paths(((0, 120), (100, 0), (400, 0), (500, 120), (500, 260), (0, 700), (500, 700))),
    "3": _paths(
        ((0, 80), (100, 0), (400, 0), (500, 100), (500, 250), (400, 350), (200, 350)),
        ((400, 350), (500, 450), (500, 600), (400, 700), (100, 700), (0, 620)),
    ),
    "4": _paths(((400, 700), (400, 0), (0, 470), (500, 470))),
    "5": _paths(
        (
            (500, 0),
            (0, 0),
            (0, 330),
            (400, 330),
            (500, 430),
            (500, 600),
            (400, 700),
            (100, 700),
            (0, 620),
        )
    ),
    "6": _paths(
        (
            (500, 80),
            (400, 0),
            (120, 0),
            (0, 150),
            (0, 580),
            (120, 700),
            (400, 700),
            (500, 580),
            (500, 430),
            (400, 330),
            (0, 330),
        )
    ),
    "7": _paths(((0, 0), (500, 0), (160, 700))),
    "8": _paths(
        (
            (100, 350),
            (0, 250),
            (0, 100),
            (100, 0),
            (400, 0),
            (500, 100),
            (500, 250),
            (400, 350),
            (100, 350),
            (0, 450),
            (0, 600),
            (100, 700),
            (400, 700),
            (500, 600),
            (500, 450),
            (400, 350),
        )
    ),
    "9": _paths(
        (
            (500, 370),
            (100, 370),
            (0, 270),
            (0, 100),
            (100, 0),
            (400, 0),
            (500, 120),
            (500, 550),
            (380, 700),
            (100, 700),
            (0, 620),
        )
    ),
    "A": _paths(((0, 700), (0, 220), (250, 0), (500, 220), (500, 700)), ((0, 390), (500, 390))),
    "B": _paths(
        ((0, 700), (0, 0), (350, 0), (500, 100), (500, 250), (350, 350), (0, 350)),
        ((350, 350), (500, 450), (500, 600), (350, 700), (0, 700)),
    ),
    "C": _paths(
        ((500, 100), (400, 0), (100, 0), (0, 100), (0, 600), (100, 700), (400, 700), (500, 600))
    ),
    "D": _paths(((0, 700), (0, 0), (320, 0), (500, 150), (500, 550), (320, 700), (0, 700))),
    "E": _paths(((500, 0), (0, 0), (0, 700), (500, 700)), ((0, 350), (400, 350))),
    "F": _paths(((0, 700), (0, 0), (500, 0)), ((0, 350), (400, 350))),
    "G": _paths(
        (
            (500, 120),
            (400, 0),
            (100, 0),
            (0, 100),
            (0, 600),
            (100, 700),
            (400, 700),
            (500, 600),
            (500, 390),
            (300, 390),
        )
    ),
    "H": _paths(((0, 0), (0, 700)), ((500, 0), (500, 700)), ((0, 350), (500, 350))),
    "I": _paths(((80, 0), (420, 0)), ((250, 0), (250, 700)), ((80, 700), (420, 700))),
    "J": _paths(((0, 0), (500, 0), (500, 560), (380, 700), (120, 700), (0, 580))),
    "K": _paths(((0, 0), (0, 700)), ((500, 0), (0, 390), (500, 700))),
    "L": _paths(((0, 0), (0, 700), (500, 700))),
    "M": _paths(((0, 700), (0, 0), (250, 300), (500, 0), (500, 700))),
    "N": _paths(((0, 700), (0, 0), (500, 700), (500, 0))),
    "O": _paths(
        (
            (100, 0),
            (400, 0),
            (500, 100),
            (500, 600),
            (400, 700),
            (100, 700),
            (0, 600),
            (0, 100),
            (100, 0),
        )
    ),
    "P": _paths(((0, 700), (0, 0), (380, 0), (500, 120), (500, 280), (380, 400), (0, 400))),
    "Q": _paths(
        (
            (100, 0),
            (400, 0),
            (500, 100),
            (500, 600),
            (400, 700),
            (100, 700),
            (0, 600),
            (0, 100),
            (100, 0),
        ),
        ((300, 500), (520, 720)),
    ),
    "R": _paths(
        ((0, 700), (0, 0), (380, 0), (500, 120), (500, 280), (380, 400), (0, 400)),
        ((280, 400), (520, 700)),
    ),
    "S": _paths(
        (
            (500, 100),
            (400, 0),
            (100, 0),
            (0, 100),
            (0, 280),
            (100, 350),
            (400, 350),
            (500, 430),
            (500, 600),
            (400, 700),
            (100, 700),
            (0, 600),
        )
    ),
    "T": _paths(((0, 0), (500, 0)), ((250, 0), (250, 700))),
    "U": _paths(((0, 0), (0, 580), (120, 700), (380, 700), (500, 580), (500, 0))),
    "V": _paths(((0, 0), (250, 700), (500, 0))),
    "W": _paths(((0, 0), (100, 700), (250, 420), (400, 700), (500, 0))),
    "X": _paths(((0, 0), (500, 700)), ((500, 0), (0, 700))),
    "Y": _paths(((0, 0), (250, 350), (500, 0)), ((250, 350), (250, 700))),
    "Z": _paths(((0, 0), (500, 0), (0, 700), (500, 700))),
    ":": _paths(((250, 210), (250, 230)), ((250, 500), (250, 520))),
    ".": _paths(((250, 660), (250, 700))),
    ",": _paths(((280, 630), (210, 760))),
    "-": _paths(((50, 350), (450, 350))),
    MINUS: _paths(((50, 350), (450, 350))),
    "+": _paths(((50, 350), (450, 350)), ((250, 150), (250, 550))),
    MULTIPLICATION: _paths(((70, 150), (430, 550)), ((430, 150), (70, 550))),
    DIVISION: _paths(
        ((50, 350), (450, 350)),
        ((250, 110), (250, 130)),
        ((250, 570), (250, 590)),
    ),
    "/": _paths(((450, 0), (50, 700))),
    "(": _paths(((350, 0), (180, 160), (150, 350), (180, 540), (350, 700))),
    ")": _paths(((150, 0), (320, 160), (350, 350), (320, 540), (150, 700))),
}

_LOWERCASE: dict[str, Glyph] = {
    "a": _paths(
        ((40, 350), (120, 250), (390, 250), (480, 350), (480, 700)),
        (
            (480, 380),
            (360, 300),
            (120, 300),
            (20, 420),
            (20, 590),
            (120, 680),
            (360, 680),
            (480, 590),
        ),
    ),
    "b": _paths(
        ((20, 0), (20, 700)),
        (
            (20, 340),
            (120, 250),
            (370, 250),
            (480, 360),
            (480, 590),
            (370, 700),
            (120, 700),
            (20, 610),
        ),
    ),
    "c": _paths(
        (
            (480, 340),
            (390, 250),
            (120, 250),
            (20, 350),
            (20, 600),
            (120, 700),
            (390, 700),
            (480, 610),
        )
    ),
    "d": _paths(
        ((480, 0), (480, 700)),
        (
            (480, 340),
            (380, 250),
            (130, 250),
            (20, 360),
            (20, 590),
            (130, 700),
            (380, 700),
            (480, 610),
        ),
    ),
    "e": _paths(
        (
            (20, 470),
            (480, 470),
            (480, 360),
            (370, 250),
            (130, 250),
            (20, 360),
            (20, 590),
            (130, 700),
            (390, 700),
            (480, 620),
        )
    ),
    "f": _paths(((130, 700), (130, 130), (240, 0), (430, 0)), ((20, 270), (360, 270))),
    "g": _paths(
        ((480, 260), (480, 750), (380, 850), (120, 850), (30, 770)),
        (
            (480, 340),
            (380, 250),
            (130, 250),
            (20, 360),
            (20, 590),
            (130, 700),
            (380, 700),
            (480, 610),
        ),
    ),
    "h": _paths(((20, 0), (20, 700)), ((20, 380), (140, 250), (360, 250), (480, 370), (480, 700))),
    "i": _paths(((250, 260), (250, 700)), ((250, 80), (250, 100))),
    "j": _paths(
        ((330, 260), (330, 740), (240, 840), (80, 840), (20, 780)), ((330, 80), (330, 100))
    ),
    "k": _paths(((20, 0), (20, 700)), ((460, 250), (20, 520), (480, 700))),
    "l": _paths(((200, 0), (200, 590), (300, 700), (430, 700))),
    "m": _paths(((20, 700), (20, 260), (180, 260), (250, 360), (320, 260), (480, 260), (480, 700))),
    "n": _paths(
        ((20, 700), (20, 260)), ((20, 380), (140, 250), (360, 250), (480, 370), (480, 700))
    ),
    "o": _paths(
        (
            (130, 250),
            (370, 250),
            (480, 360),
            (480, 590),
            (370, 700),
            (130, 700),
            (20, 590),
            (20, 360),
            (130, 250),
        )
    ),
    "p": _paths(
        ((20, 850), (20, 260)),
        (
            (20, 340),
            (120, 250),
            (370, 250),
            (480, 360),
            (480, 590),
            (370, 700),
            (120, 700),
            (20, 610),
        ),
    ),
    "q": _paths(
        ((480, 850), (480, 260)),
        (
            (480, 340),
            (380, 250),
            (130, 250),
            (20, 360),
            (20, 590),
            (130, 700),
            (380, 700),
            (480, 610),
        ),
    ),
    "r": _paths(((20, 700), (20, 260)), ((20, 390), (150, 260), (350, 260), (470, 350))),
    "s": _paths(
        (
            (470, 330),
            (390, 250),
            (120, 250),
            (20, 340),
            (120, 470),
            (380, 470),
            (480, 600),
            (390, 700),
            (100, 700),
            (20, 620),
        )
    ),
    "t": _paths(((220, 80), (220, 580), (320, 700), (460, 700)), ((50, 270), (400, 270))),
    "u": _paths(((20, 260), (20, 580), (140, 700), (360, 700), (480, 580), (480, 260), (480, 700))),
    "v": _paths(((20, 260), (250, 700), (480, 260))),
    "w": _paths(((20, 260), (100, 700), (250, 460), (400, 700), (480, 260))),
    "x": _paths(((30, 260), (470, 700)), ((470, 260), (30, 700))),
    "y": _paths(((20, 260), (250, 700), (480, 260)), ((250, 700), (160, 850), (40, 850))),
    "z": _paths(((20, 260), (480, 260), (20, 700), (480, 700))),
}
_GLYPHS.update(_LOWERCASE)


_FRIENDLY_TITLE_GLYPHS: dict[str, Glyph] = {
    "K": _paths(
        ((50, 20), (50, 680)),
        (
            (470, 30),
            (405, 70),
            (310, 155),
            (205, 260),
            (95, 350),
            (205, 435),
            (315, 545),
            (405, 635),
            (470, 675),
        ),
    ),
    "P": _paths(
        ((45, 690), (45, 20), (285, 20), (395, 50), (470, 140), (470, 260)),
        ((470, 260), (395, 350), (285, 380), (45, 380)),
    ),
    "e": _paths(
        (
            (35, 470),
            (470, 470),
            (455, 375),
            (390, 305),
            (290, 270),
            (165, 270),
            (75, 320),
            (30, 405),
            (30, 560),
            (80, 640),
            (175, 685),
            (315, 685),
            (415, 650),
            (475, 600),
        )
    ),
    "n": _paths(
        ((35, 690), (35, 280)),
        ((35, 410), (90, 330), (175, 280), (300, 270), (405, 315), (470, 405), (470, 690)),
    ),
    "u": _paths(
        (
            (30, 280),
            (30, 535),
            (65, 625),
            (150, 680),
            (275, 690),
            (390, 650),
            (470, 555),
            (470, 280),
            (470, 690),
        )
    ),
    "z": _paths(
        (
            (35, 290),
            (465, 290),
            (430, 340),
            (335, 430),
            (205, 540),
            (95, 635),
            (35, 680),
            (465, 680),
        )
    ),
    "l": _paths(((180, 25), (180, 560), (205, 635), (275, 680), (400, 680))),
    "s": _paths(
        (
            (455, 345),
            (395, 295),
            (300, 270),
            (165, 270),
            (75, 310),
            (35, 375),
            (65, 440),
            (150, 475),
            (335, 490),
            (425, 535),
            (465, 600),
            (405, 655),
            (310, 685),
            (160, 685),
            (65, 650),
            (30, 610),
        )
    ),
}


def text_width(text: str, height: int) -> int:
    if not text:
        return 0
    return ((len(text) - 1) * _ADVANCE + _W) * height // _H


def proportional_text_width(text: str, height: int) -> int:
    if not text:
        return 0
    advances = sum(_proportional_advance(character) for character in text[:-1])
    return (advances + _W) * height // _H


def _proportional_advance(character: str) -> int:
    return _PROPORTIONAL_ADVANCES.get(character, 560)


def _add_glyph_run(
    scene: Scene,
    text: str,
    x: int,
    y: int,
    height: int,
    color: Color,
    width: int,
    *,
    proportional: bool,
    glyph_overrides: dict[str, Glyph] | None = None,
) -> None:
    cursor = x
    for character in text:
        advance = _proportional_advance(character) if proportional else _ADVANCE
        if character == " ":
            cursor += advance * height // _H
            continue
        glyph = None if glyph_overrides is None else glyph_overrides.get(character)
        if glyph is None:
            try:
                glyph = _GLYPHS[character]
            except KeyError as error:
                raise ValueError(f"unsupported vector glyph: {character!r}") from error
        for path in glyph:
            scene.operations.append(
                StrokePath(
                    tuple(
                        (
                            cursor + point_x * height // _H,
                            y + point_y * height // _H,
                        )
                        for point_x, point_y in path
                    ),
                    width,
                    color,
                )
            )
        cursor += advance * height // _H


def add_text(
    scene: Scene,
    text: str,
    x: int,
    y: int,
    height: int,
    color: Color,
    *,
    stroke_width: int | None = None,
) -> None:
    """Expand a glyph run into ordered vector paths."""
    width = stroke_width if stroke_width is not None else max(1, height // 15)
    _add_glyph_run(
        scene,
        text,
        x,
        y,
        height,
        color,
        width,
        proportional=False,
    )


def add_proportional_text(
    scene: Scene,
    text: str,
    x: int,
    y: int,
    height: int,
    color: Color,
    *,
    stroke_width: int | None = None,
) -> None:
    """Expand a proportionally spaced glyph run into ordered vector paths."""
    width = stroke_width if stroke_width is not None else max(1, height // 15)
    _add_glyph_run(
        scene,
        text,
        x,
        y,
        height,
        color,
        width,
        proportional=True,
    )


def add_centered_proportional_text(
    scene: Scene,
    text: str,
    center_x: int,
    y: int,
    height: int,
    color: Color,
    *,
    stroke_width: int | None = None,
) -> None:
    add_proportional_text(
        scene,
        text,
        center_x - proportional_text_width(text, height) // 2,
        y,
        height,
        color,
        stroke_width=stroke_width,
    )


def add_centered_friendly_title(
    scene: Scene,
    text: str,
    center_x: int,
    y: int,
    height: int,
    color: Color,
    *,
    stroke_width: int | None = None,
) -> None:
    """Render the fixed page title with softer, proportionally spaced glyphs."""
    width = stroke_width if stroke_width is not None else max(1, height // 12)
    _add_glyph_run(
        scene,
        text,
        center_x - proportional_text_width(text, height) // 2,
        y,
        height,
        color,
        width,
        proportional=True,
        glyph_overrides=_FRIENDLY_TITLE_GLYPHS,
    )


def add_centered_text(
    scene: Scene,
    text: str,
    center_x: int,
    y: int,
    height: int,
    color: Color,
    *,
    stroke_width: int | None = None,
) -> None:
    add_text(
        scene,
        text,
        center_x - text_width(text, height) // 2,
        y,
        height,
        color,
        stroke_width=stroke_width,
    )
