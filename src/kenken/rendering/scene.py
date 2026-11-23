"""Backend-independent ordered integer geometry."""

from __future__ import annotations

from dataclasses import dataclass, field

type Color = tuple[int, int, int]
type Point = tuple[int, int]

WHITE: Color = (255, 255, 255)


@dataclass(frozen=True)
class FillRect:
    x: int
    y: int
    width: int
    height: int
    color: Color


@dataclass(frozen=True)
class StrokePath:
    points: tuple[Point, ...]
    width: int
    color: Color
    closed: bool = False

    def __post_init__(self) -> None:
        if len(self.points) < 2:
            raise ValueError("a stroke path requires at least two points")


type DrawOperation = FillRect | StrokePath


@dataclass
class Scene:
    width: int
    height: int
    operations: list[DrawOperation] = field(default_factory=list)


def place_scene(source: Scene, target: Scene, x: int, y: int, width: int, height: int) -> None:
    """Center and uniformly scale source into the target rectangle."""
    numerator = min(width * source.height, height * source.width)
    denominator = source.width * source.height
    scaled_width = source.width * numerator // denominator
    scaled_height = source.height * numerator // denominator
    offset_x = x + (width - scaled_width) // 2
    offset_y = y + (height - scaled_height) // 2

    def scaled(value: int) -> int:
        return value * numerator // denominator

    for operation in source.operations:
        if isinstance(operation, FillRect):
            target.operations.append(
                FillRect(
                    offset_x + scaled(operation.x),
                    offset_y + scaled(operation.y),
                    max(1, scaled(operation.width)),
                    max(1, scaled(operation.height)),
                    operation.color,
                )
            )
        else:
            target.operations.append(
                StrokePath(
                    tuple(
                        (offset_x + scaled(point_x), offset_y + scaled(point_y))
                        for point_x, point_y in operation.points
                    ),
                    max(1, scaled(operation.width)),
                    operation.color,
                    operation.closed,
                )
            )
