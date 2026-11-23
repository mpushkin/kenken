"""Build the fixed, auditable Volume 12 through 20 release batch."""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from kenken.cli import _atomic_write_many
from kenken.generation import (
    ARITHMETIC_CAGE_POLICY,
    EASY_ARITHMETIC_LIMITS,
    GIVEN_CAGE_POLICY,
    GenerationConfig,
    count_given_cages,
    evaluate_arithmetic_cage_policy,
    evaluate_difficulty,
    generate,
    given_cage_cap,
    serialize_generation_report,
)
from kenken.model import DifficultyBand, SolutionV1, VerifiedPuzzle
from kenken.rendering import compose_page, serialize_pdf, serialize_pdf_pages
from kenken.serialization import (
    parse_puzzle_bytes,
    serialize_puzzle_bytes,
    serialize_solution_bytes,
)
from kenken.solver import verify

ROOT = Path(__file__).resolve().parents[1]
PDF_OUTPUT = ROOT / "output" / "pdf"
MAX_ATTEMPTS = 2_000
MAX_SOLVER_NODES = 1_000_000
HISTORICAL_SIGNATURE = (
    (1, 4, "easy"),
    (2, 4, "medium"),
    (3, 4, "hard"),
    (4, 5, "easy"),
    (5, 5, "medium"),
    (6, 5, "hard"),
)
SEVEN_PAGE_SIGNATURE = (
    (1, 4, "easy"),
    (2, 4, "easy"),
    (3, 4, "medium"),
    (4, 4, "hard"),
    (5, 5, "easy"),
    (6, 5, "medium"),
    (7, 5, "hard"),
)
SUPPORTED_MANIFEST_SCHEMAS = {
    "kenken.collection-manifest/v1",
    "kenken.collection-manifest/v2",
    "kenken.collection-manifest/v3",
}


@dataclass(frozen=True)
class PageSpec:
    number: int
    size: int
    profile: DifficultyBand
    seeds: tuple[int, int, int, int]

    @property
    def stem(self) -> str:
        return f"kenken-page-{self.number:02d}-{self.size}x{self.size}-{self.profile}-a4"


@dataclass(frozen=True)
class PriorCollection:
    volume: int
    manifest_path: Path
    artifact_root: Path


@dataclass(frozen=True)
class CollectionSpec:
    volume: int
    seed_namespace: str
    package_root: Path
    collection_path: Path
    pages: tuple[PageSpec, ...]
    prior_collections: tuple[PriorCollection, ...] = ()


VOLUME_1_PAGES = (
    PageSpec(1, 4, "easy", (2026072501, 2026072502, 2026072503, 2026072504)),
    PageSpec(2, 4, "medium", (2026072501, 2026072502, 2026072503, 2026072504)),
    PageSpec(3, 4, "hard", (2026072504, 2026072508, 2026072509, 2026072512)),
    PageSpec(4, 5, "easy", (2026072501, 2026072502, 2026072503, 2026072504)),
    PageSpec(5, 5, "medium", (2026072501, 2026072502, 2026072503, 2026072504)),
    PageSpec(6, 5, "hard", (2026072501, 2026072502, 2026072503, 2026072504)),
)

VOLUME_2_PAGES = (
    PageSpec(1, 4, "easy", (2026072601, 2026072602, 2026072603, 2026072604)),
    PageSpec(2, 4, "medium", (2026072601, 2026072602, 2026072603, 2026072604)),
    PageSpec(3, 4, "hard", (2026072602, 2026072604, 2026072605, 2026072609)),
    PageSpec(4, 5, "easy", (2026072601, 2026072602, 2026072603, 2026072604)),
    PageSpec(5, 5, "medium", (2026072601, 2026072602, 2026072603, 2026072604)),
    PageSpec(6, 5, "hard", (2026072601, 2026072602, 2026072603, 2026072604)),
)

VOLUME_3_PAGES = (
    PageSpec(1, 4, "easy", (2026072701, 2026072702, 2026072703, 2026072704)),
    PageSpec(2, 4, "medium", (2026072701, 2026072702, 2026072703, 2026072704)),
    PageSpec(3, 4, "hard", (2026072701, 2026072704, 2026072706, 2026072709)),
    PageSpec(4, 5, "easy", (2026072701, 2026072702, 2026072703, 2026072704)),
    PageSpec(5, 5, "medium", (2026072701, 2026072702, 2026072703, 2026072704)),
    PageSpec(6, 5, "hard", (2026072701, 2026072702, 2026072703, 2026072704)),
)

VOLUME_4_PAGES = (
    PageSpec(1, 4, "easy", (2026072801, 2026072802, 2026072803, 2026072804)),
    PageSpec(2, 4, "easy", (2026072805, 2026072806, 2026072807, 2026072808)),
    PageSpec(3, 4, "medium", (2026072801, 2026072802, 2026072803, 2026072804)),
    PageSpec(4, 4, "hard", (2026072801, 2026072807, 2026072819, 2026072823)),
    PageSpec(5, 5, "easy", (2026072801, 2026072802, 2026072803, 2026072804)),
    PageSpec(6, 5, "medium", (2026072801, 2026072802, 2026072803, 2026072804)),
    PageSpec(7, 5, "hard", (2026072801, 2026072802, 2026072803, 2026072804)),
)

VOLUME_5_PAGES = (
    PageSpec(1, 4, "easy", (2026072901, 2026072902, 2026072903, 2026072904)),
    PageSpec(2, 4, "easy", (2026072905, 2026072906, 2026072907, 2026072908)),
    PageSpec(3, 4, "medium", (2026072901, 2026072902, 2026072903, 2026072904)),
    PageSpec(4, 4, "hard", (2026072903, 2026072905, 2026072909, 2026072919)),
    PageSpec(5, 5, "easy", (2026072901, 2026072902, 2026072903, 2026072904)),
    PageSpec(6, 5, "medium", (2026072901, 2026072902, 2026072903, 2026072904)),
    PageSpec(7, 5, "hard", (2026072901, 2026072902, 2026072903, 2026072904)),
)

VOLUME_6_PAGES = (
    PageSpec(1, 4, "easy", (2026073001, 2026073002, 2026073003, 2026073004)),
    PageSpec(2, 4, "easy", (2026073005, 2026073006, 2026073007, 2026073008)),
    PageSpec(3, 4, "medium", (2026073001, 2026073002, 2026073003, 2026073004)),
    PageSpec(4, 4, "hard", (2026073003, 2026073005, 2026073006, 2026073010)),
    PageSpec(5, 5, "easy", (2026073001, 2026073002, 2026073003, 2026073004)),
    PageSpec(6, 5, "medium", (2026073001, 2026073002, 2026073003, 2026073004)),
    PageSpec(7, 5, "hard", (2026073001, 2026073002, 2026073003, 2026073004)),
)

VOLUME_7_PAGES = (
    PageSpec(1, 4, "easy", (2026073101, 2026073102, 2026073103, 2026073104)),
    PageSpec(2, 4, "easy", (2026073105, 2026073106, 2026073107, 2026073108)),
    PageSpec(3, 4, "medium", (2026073101, 2026073102, 2026073103, 2026073104)),
    PageSpec(4, 4, "hard", (2026073103, 2026073107, 2026073112, 2026073115)),
    PageSpec(5, 5, "easy", (2026073101, 2026073102, 2026073103, 2026073104)),
    PageSpec(6, 5, "medium", (2026073101, 2026073102, 2026073103, 2026073104)),
    PageSpec(7, 5, "hard", (2026073101, 2026073102, 2026073103, 2026073104)),
)

VOLUME_8_PAGES = (
    PageSpec(1, 4, "easy", (2026080101, 2026080102, 2026080103, 2026080104)),
    PageSpec(2, 4, "easy", (2026080105, 2026080106, 2026080107, 2026080108)),
    PageSpec(3, 4, "medium", (2026080101, 2026080102, 2026080103, 2026080104)),
    PageSpec(4, 4, "hard", (2026080111, 2026080112, 2026080114, 2026080117)),
    PageSpec(5, 5, "easy", (2026080101, 2026080102, 2026080103, 2026080104)),
    PageSpec(6, 5, "medium", (2026080101, 2026080102, 2026080103, 2026080104)),
    PageSpec(7, 5, "hard", (2026080101, 2026080102, 2026080103, 2026080104)),
)

VOLUME_9_PAGES = (
    PageSpec(1, 4, "easy", (2026080201, 2026080202, 2026080203, 2026080204)),
    PageSpec(2, 4, "easy", (2026080205, 2026080206, 2026080207, 2026080208)),
    PageSpec(3, 4, "medium", (2026080201, 2026080202, 2026080203, 2026080204)),
    PageSpec(4, 4, "hard", (2026080202, 2026080203, 2026080209, 2026080214)),
    PageSpec(5, 5, "easy", (2026080201, 2026080202, 2026080203, 2026080204)),
    PageSpec(6, 5, "medium", (2026080201, 2026080202, 2026080203, 2026080204)),
    PageSpec(7, 5, "hard", (2026080201, 2026080202, 2026080203, 2026080204)),
)

VOLUME_10_PAGES = (
    PageSpec(1, 4, "easy", (2026080301, 2026080302, 2026080303, 2026080304)),
    PageSpec(2, 4, "easy", (2026080305, 2026080306, 2026080307, 2026080308)),
    PageSpec(3, 4, "medium", (2026080301, 2026080302, 2026080303, 2026080304)),
    PageSpec(4, 4, "hard", (2026080305, 2026080306, 2026080307, 2026080309)),
    PageSpec(5, 5, "easy", (2026080301, 2026080302, 2026080303, 2026080304)),
    PageSpec(6, 5, "medium", (2026080301, 2026080302, 2026080303, 2026080304)),
    PageSpec(7, 5, "hard", (2026080301, 2026080302, 2026080303, 2026080304)),
)

VOLUME_11_PAGES = (
    PageSpec(1, 4, "easy", (2026080401, 2026080402, 2026080403, 2026080404)),
    PageSpec(2, 4, "easy", (2026080405, 2026080406, 2026080407, 2026080408)),
    PageSpec(3, 4, "medium", (2026080401, 2026080402, 2026080403, 2026080404)),
    PageSpec(4, 4, "hard", (2026080401, 2026080402, 2026080403, 2026080407)),
    PageSpec(5, 5, "easy", (2026080401, 2026080402, 2026080403, 2026080404)),
    PageSpec(6, 5, "medium", (2026080401, 2026080402, 2026080403, 2026080404)),
    PageSpec(7, 5, "hard", (2026080401, 2026080402, 2026080403, 2026080404)),
)

VOLUME_12_PAGES = (
    PageSpec(1, 4, "easy", (2026080501, 2026080502, 2026080503, 2026080504)),
    PageSpec(2, 4, "easy", (2026080505, 2026080506, 2026080507, 2026080508)),
    PageSpec(3, 4, "medium", (2026080501, 2026080502, 2026080503, 2026080504)),
    PageSpec(4, 4, "hard", (2026080501, 2026080503, 2026080509, 2026080516)),
    PageSpec(5, 5, "easy", (2026080501, 2026080502, 2026080503, 2026080504)),
    PageSpec(6, 5, "medium", (2026080501, 2026080502, 2026080503, 2026080504)),
    PageSpec(7, 5, "hard", (2026080501, 2026080502, 2026080503, 2026080504)),
)

VOLUME_13_PAGES = (
    PageSpec(1, 4, "easy", (2026080601, 2026080602, 2026080603, 2026080604)),
    PageSpec(2, 4, "easy", (2026080605, 2026080606, 2026080607, 2026080608)),
    PageSpec(3, 4, "medium", (2026080601, 2026080602, 2026080603, 2026080604)),
    PageSpec(4, 4, "hard", (2026080601, 2026080605, 2026080606, 2026080608)),
    PageSpec(5, 5, "easy", (2026080601, 2026080602, 2026080603, 2026080604)),
    PageSpec(6, 5, "medium", (2026080601, 2026080602, 2026080603, 2026080604)),
    PageSpec(7, 5, "hard", (2026080601, 2026080602, 2026080603, 2026080604)),
)

VOLUME_14_PAGES = (
    PageSpec(1, 4, "easy", (2026080701, 2026080702, 2026080703, 2026080704)),
    PageSpec(2, 4, "easy", (2026080705, 2026080706, 2026080707, 2026080708)),
    PageSpec(3, 4, "medium", (2026080701, 2026080702, 2026080703, 2026080704)),
    PageSpec(4, 4, "hard", (2026080702, 2026080704, 2026080707, 2026080714)),
    PageSpec(5, 5, "easy", (2026080701, 2026080702, 2026080703, 2026080704)),
    PageSpec(6, 5, "medium", (2026080701, 2026080702, 2026080703, 2026080704)),
    PageSpec(7, 5, "hard", (2026080701, 2026080702, 2026080703, 2026080704)),
)

VOLUME_15_PAGES = (
    PageSpec(1, 4, "easy", (2026080801, 2026080802, 2026080803, 2026080804)),
    PageSpec(2, 4, "easy", (2026080805, 2026080806, 2026080807, 2026080808)),
    PageSpec(3, 4, "medium", (2026080801, 2026080802, 2026080803, 2026080804)),
    PageSpec(4, 4, "hard", (2026080803, 2026080806, 2026080810, 2026080819)),
    PageSpec(5, 5, "easy", (2026080801, 2026080802, 2026080803, 2026080804)),
    PageSpec(6, 5, "medium", (2026080801, 2026080802, 2026080803, 2026080804)),
    PageSpec(7, 5, "hard", (2026080801, 2026080802, 2026080803, 2026080804)),
)

VOLUME_16_PAGES = (
    PageSpec(1, 4, "easy", (2026080901, 2026080902, 2026080903, 2026080904)),
    PageSpec(2, 4, "easy", (2026080905, 2026080906, 2026080907, 2026080908)),
    PageSpec(3, 4, "medium", (2026080901, 2026080902, 2026080903, 2026080904)),
    PageSpec(4, 4, "hard", (2026080908, 2026080909, 2026080910, 2026080913)),
    PageSpec(5, 5, "easy", (2026080901, 2026080902, 2026080903, 2026080904)),
    PageSpec(6, 5, "medium", (2026080901, 2026080902, 2026080903, 2026080904)),
    PageSpec(7, 5, "hard", (2026080901, 2026080902, 2026080903, 2026080904)),
)

VOLUME_17_PAGES = (
    PageSpec(1, 4, "easy", (2026081001, 2026081002, 2026081003, 2026081004)),
    PageSpec(2, 4, "easy", (2026081005, 2026081006, 2026081007, 2026081008)),
    PageSpec(3, 4, "medium", (2026081001, 2026081002, 2026081003, 2026081004)),
    PageSpec(4, 4, "hard", (2026081003, 2026081004, 2026081009, 2026081011)),
    PageSpec(5, 5, "easy", (2026081001, 2026081002, 2026081003, 2026081004)),
    PageSpec(6, 5, "medium", (2026081001, 2026081002, 2026081003, 2026081004)),
    PageSpec(7, 5, "hard", (2026081001, 2026081002, 2026081003, 2026081004)),
)

VOLUME_18_PAGES = (
    PageSpec(1, 4, "easy", (2026081101, 2026081102, 2026081103, 2026081104)),
    PageSpec(2, 4, "easy", (2026081105, 2026081106, 2026081107, 2026081108)),
    PageSpec(3, 4, "medium", (2026081101, 2026081102, 2026081103, 2026081104)),
    PageSpec(4, 4, "hard", (2026081101, 2026081107, 2026081109, 2026081114)),
    PageSpec(5, 5, "easy", (2026081101, 2026081102, 2026081103, 2026081104)),
    PageSpec(6, 5, "medium", (2026081101, 2026081102, 2026081103, 2026081104)),
    PageSpec(7, 5, "hard", (2026081101, 2026081102, 2026081103, 2026081104)),
)

VOLUME_19_PAGES = (
    PageSpec(1, 4, "easy", (2026081201, 2026081202, 2026081203, 2026081204)),
    PageSpec(2, 4, "easy", (2026081205, 2026081206, 2026081207, 2026081208)),
    PageSpec(3, 4, "medium", (2026081201, 2026081202, 2026081203, 2026081204)),
    PageSpec(4, 4, "hard", (2026081204, 2026081208, 2026081213, 2026081214)),
    PageSpec(5, 5, "easy", (2026081201, 2026081202, 2026081203, 2026081204)),
    PageSpec(6, 5, "medium", (2026081201, 2026081202, 2026081203, 2026081204)),
    PageSpec(7, 5, "hard", (2026081201, 2026081202, 2026081203, 2026081204)),
)

VOLUME_20_PAGES = (
    PageSpec(1, 4, "easy", (2026081301, 2026081302, 2026081303, 2026081304)),
    PageSpec(2, 4, "easy", (2026081305, 2026081306, 2026081307, 2026081308)),
    PageSpec(3, 4, "medium", (2026081301, 2026081302, 2026081303, 2026081304)),
    PageSpec(4, 4, "hard", (2026081301, 2026081304, 2026081308, 2026081311)),
    PageSpec(5, 5, "easy", (2026081301, 2026081302, 2026081303, 2026081304)),
    PageSpec(6, 5, "medium", (2026081301, 2026081302, 2026081303, 2026081304)),
    PageSpec(7, 5, "hard", (2026081301, 2026081302, 2026081303, 2026081304)),
)

VOLUME_1 = CollectionSpec(
    volume=1,
    seed_namespace="20260725xx",
    package_root=PDF_OUTPUT,
    collection_path=PDF_OUTPUT / "kenken-24-puzzle-collection-a4.pdf",
    pages=VOLUME_1_PAGES,
)

VOLUME_2 = CollectionSpec(
    volume=2,
    seed_namespace="20260726xx",
    package_root=PDF_OUTPUT / "volume-2",
    collection_path=PDF_OUTPUT / "kenken-24-puzzle-collection-a4-volume-2.pdf",
    pages=VOLUME_2_PAGES,
    prior_collections=(
        PriorCollection(
            volume=1,
            manifest_path=PDF_OUTPUT / "collection-manifest.json",
            artifact_root=PDF_OUTPUT,
        ),
    ),
)

VOLUME_3 = CollectionSpec(
    volume=3,
    seed_namespace="20260727xx",
    package_root=PDF_OUTPUT / "volume-3",
    collection_path=PDF_OUTPUT / "kenken-24-puzzle-collection-a4-volume-3.pdf",
    pages=VOLUME_3_PAGES,
    prior_collections=(
        PriorCollection(
            volume=1,
            manifest_path=PDF_OUTPUT / "collection-manifest.json",
            artifact_root=PDF_OUTPUT,
        ),
        PriorCollection(
            volume=2,
            manifest_path=PDF_OUTPUT / "volume-2" / "collection-manifest.json",
            artifact_root=PDF_OUTPUT / "volume-2",
        ),
    ),
)

VOLUME_4 = CollectionSpec(
    volume=4,
    seed_namespace="20260728xx",
    package_root=PDF_OUTPUT / "volume-4",
    collection_path=PDF_OUTPUT / "kenken-28-puzzle-collection-a4-volume-4.pdf",
    pages=VOLUME_4_PAGES,
    prior_collections=(
        PriorCollection(
            volume=1,
            manifest_path=PDF_OUTPUT / "collection-manifest.json",
            artifact_root=PDF_OUTPUT,
        ),
        PriorCollection(
            volume=2,
            manifest_path=PDF_OUTPUT / "volume-2" / "collection-manifest.json",
            artifact_root=PDF_OUTPUT / "volume-2",
        ),
        PriorCollection(
            volume=3,
            manifest_path=PDF_OUTPUT / "volume-3" / "collection-manifest.json",
            artifact_root=PDF_OUTPUT / "volume-3",
        ),
    ),
)

VOLUME_5 = CollectionSpec(
    volume=5,
    seed_namespace="20260729xx",
    package_root=PDF_OUTPUT / "volume-5",
    collection_path=PDF_OUTPUT / "kenken-28-puzzle-collection-a4-volume-5.pdf",
    pages=VOLUME_5_PAGES,
    prior_collections=(
        *VOLUME_4.prior_collections,
        PriorCollection(
            volume=4,
            manifest_path=PDF_OUTPUT / "volume-4" / "collection-manifest.json",
            artifact_root=PDF_OUTPUT / "volume-4",
        ),
    ),
)

VOLUME_6 = CollectionSpec(
    volume=6,
    seed_namespace="20260730xx",
    package_root=PDF_OUTPUT / "volume-6",
    collection_path=PDF_OUTPUT / "kenken-28-puzzle-collection-a4-volume-6.pdf",
    pages=VOLUME_6_PAGES,
    prior_collections=(
        *VOLUME_5.prior_collections,
        PriorCollection(
            volume=5,
            manifest_path=PDF_OUTPUT / "volume-5" / "collection-manifest.json",
            artifact_root=PDF_OUTPUT / "volume-5",
        ),
    ),
)

VOLUME_7 = CollectionSpec(
    volume=7,
    seed_namespace="20260731xx",
    package_root=PDF_OUTPUT / "volume-7",
    collection_path=PDF_OUTPUT / "kenken-28-puzzle-collection-a4-volume-7.pdf",
    pages=VOLUME_7_PAGES,
    prior_collections=(
        *VOLUME_6.prior_collections,
        PriorCollection(
            volume=6,
            manifest_path=PDF_OUTPUT / "volume-6" / "collection-manifest.json",
            artifact_root=PDF_OUTPUT / "volume-6",
        ),
    ),
)

VOLUME_8 = CollectionSpec(
    volume=8,
    seed_namespace="20260801xx",
    package_root=PDF_OUTPUT / "volume-8",
    collection_path=PDF_OUTPUT / "kenken-28-puzzle-collection-a4-volume-8.pdf",
    pages=VOLUME_8_PAGES,
    prior_collections=(
        *VOLUME_7.prior_collections,
        PriorCollection(
            volume=7,
            manifest_path=PDF_OUTPUT / "volume-7" / "collection-manifest.json",
            artifact_root=PDF_OUTPUT / "volume-7",
        ),
    ),
)

VOLUME_9 = CollectionSpec(
    volume=9,
    seed_namespace="20260802xx",
    package_root=PDF_OUTPUT / "volume-9",
    collection_path=PDF_OUTPUT / "kenken-28-puzzle-collection-a4-volume-9.pdf",
    pages=VOLUME_9_PAGES,
    prior_collections=(
        *VOLUME_8.prior_collections,
        PriorCollection(
            volume=8,
            manifest_path=PDF_OUTPUT / "volume-8" / "collection-manifest.json",
            artifact_root=PDF_OUTPUT / "volume-8",
        ),
    ),
)

VOLUME_10 = CollectionSpec(
    volume=10,
    seed_namespace="20260803xx",
    package_root=PDF_OUTPUT / "volume-10",
    collection_path=PDF_OUTPUT / "kenken-28-puzzle-collection-a4-volume-10.pdf",
    pages=VOLUME_10_PAGES,
    prior_collections=(
        *VOLUME_9.prior_collections,
        PriorCollection(
            volume=9,
            manifest_path=PDF_OUTPUT / "volume-9" / "collection-manifest.json",
            artifact_root=PDF_OUTPUT / "volume-9",
        ),
    ),
)

VOLUME_11 = CollectionSpec(
    volume=11,
    seed_namespace="20260804xx",
    package_root=PDF_OUTPUT / "volume-11",
    collection_path=PDF_OUTPUT / "kenken-28-puzzle-collection-a4-volume-11.pdf",
    pages=VOLUME_11_PAGES,
    prior_collections=(
        *VOLUME_10.prior_collections,
        PriorCollection(
            volume=10,
            manifest_path=PDF_OUTPUT / "volume-10" / "collection-manifest.json",
            artifact_root=PDF_OUTPUT / "volume-10",
        ),
    ),
)


def _next_volume_spec(
    volume: int, namespace: str, pages: tuple[PageSpec, ...], prior: CollectionSpec
) -> CollectionSpec:
    return CollectionSpec(
        volume=volume,
        seed_namespace=namespace,
        package_root=PDF_OUTPUT / f"volume-{volume}",
        collection_path=(
            PDF_OUTPUT / f"kenken-28-puzzle-collection-a4-volume-{volume}.pdf"
        ),
        pages=pages,
        prior_collections=(
            *prior.prior_collections,
            PriorCollection(
                volume=prior.volume,
                manifest_path=prior.package_root / "collection-manifest.json",
                artifact_root=prior.package_root,
            ),
        ),
    )


VOLUME_12 = _next_volume_spec(12, "20260805xx", VOLUME_12_PAGES, VOLUME_11)
VOLUME_13 = _next_volume_spec(13, "20260806xx", VOLUME_13_PAGES, VOLUME_12)
VOLUME_14 = _next_volume_spec(14, "20260807xx", VOLUME_14_PAGES, VOLUME_13)
VOLUME_15 = _next_volume_spec(15, "20260808xx", VOLUME_15_PAGES, VOLUME_14)
VOLUME_16 = _next_volume_spec(16, "20260809xx", VOLUME_16_PAGES, VOLUME_15)
VOLUME_17 = _next_volume_spec(17, "20260810xx", VOLUME_17_PAGES, VOLUME_16)
VOLUME_18 = _next_volume_spec(18, "20260811xx", VOLUME_18_PAGES, VOLUME_17)
VOLUME_19 = _next_volume_spec(19, "20260812xx", VOLUME_19_PAGES, VOLUME_18)
VOLUME_20 = _next_volume_spec(20, "20260813xx", VOLUME_20_PAGES, VOLUME_19)

REVIEWED_RELEASE_BATCH = (
    VOLUME_12,
    VOLUME_13,
    VOLUME_14,
    VOLUME_15,
    VOLUME_16,
    VOLUME_17,
    VOLUME_18,
    VOLUME_19,
    VOLUME_20,
)


def _source_stem(page: PageSpec, ordinal: int, seed: int) -> str:
    return (
        f"page-{page.number:02d}-{page.size}x{page.size}-{page.profile}"
        f"-puzzle-{ordinal:02d}-seed-{seed}"
    )


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _relative_artifact_path(spec: CollectionSpec, path: Path) -> str:
    return Path(os.path.relpath(path, spec.package_root)).as_posix()


def _puzzle_count(spec: CollectionSpec) -> int:
    return sum(len(page.seeds) for page in spec.pages)


def _source_json_count(spec: CollectionSpec) -> int:
    return 3 * _puzzle_count(spec)


def _declared_artifact_count(spec: CollectionSpec) -> int:
    return _source_json_count(spec) + len(spec.pages) + 1


def _compared_byte_set_count(spec: CollectionSpec) -> int:
    return _declared_artifact_count(spec) + 1


def _read_manifest(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text())
    except (OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"malformed prior collection manifest: {path}") from error
    if not isinstance(value, dict):
        raise RuntimeError(f"malformed prior collection manifest: {path}")
    return value


def _manifest_volume(manifest: dict[str, Any], path: Path) -> int:
    if "volume" not in manifest:
        if manifest.get("schema") == "kenken.collection-manifest/v1":
            return 1
        raise RuntimeError(f"only a v1 Volume 1 manifest may omit volume: {path}")
    volume = manifest["volume"]
    if isinstance(volume, bool) or not isinstance(volume, int) or volume < 1:
        raise RuntimeError(f"malformed prior collection manifest: {path}")
    return volume


def _manifest_records(manifest: dict[str, Any], path: Path) -> list[dict[str, Any]]:
    pages = manifest.get("pages")
    if not isinstance(pages, list) or not pages:
        raise RuntimeError(f"malformed prior collection manifest: {path}")
    records: list[dict[str, Any]] = []
    for page in pages:
        if not isinstance(page, dict) or not isinstance(page.get("puzzles"), list):
            raise RuntimeError(f"malformed prior collection manifest: {path}")
        for record in page["puzzles"]:
            if not isinstance(record, dict):
                raise RuntimeError(f"malformed prior collection manifest: {path}")
            records.append(record)
    if not records:
        raise RuntimeError(f"prior collection contains no puzzles: {path}")
    return records


def _safe_owned_path(root: Path, relative: object, label: str) -> Path:
    if not isinstance(relative, (str, Path)):
        raise RuntimeError(f"invalid {label} path: {relative!r}")
    relative_path = Path(relative)
    if not str(relative_path) or relative_path.is_absolute():
        raise RuntimeError(f"invalid {label} path: {relative!r}")
    root_resolved = root.resolve()
    path = (root / relative_path).resolve()
    if not path.is_relative_to(root_resolved):
        raise RuntimeError(f"{label} path escapes its artifact root: {relative}")
    if not path.is_file():
        raise RuntimeError(f"missing {label}: {path}")
    return path


def _validate_recorded_prior_counts(manifest: dict[str, Any], path: Path) -> None:
    if manifest.get("schema") not in {
        "kenken.collection-manifest/v2",
        "kenken.collection-manifest/v3",
    }:
        return
    cross_volume = manifest.get("cross_volume")
    if not isinstance(cross_volume, dict):
        raise RuntimeError(f"malformed prior collection manifest: {path}")
    claims = cross_volume.get("prior_collections")
    if not isinstance(claims, list):
        raise RuntimeError(f"malformed prior collection manifest: {path}")
    total = 0
    for claim in claims:
        if not isinstance(claim, dict):
            raise RuntimeError(f"malformed prior collection manifest: {path}")
        claim_relative = claim.get("manifest")
        if not isinstance(claim_relative, str):
            raise RuntimeError(f"malformed prior collection manifest: {path}")
        claim_path = _safe_owned_path(
            PDF_OUTPUT,
            Path(os.path.relpath(path.parent, PDF_OUTPUT)) / claim_relative,
            "recorded prior manifest",
        )
        claimed_manifest = _read_manifest(claim_path)
        claimed_volume = _manifest_volume(claimed_manifest, claim_path)
        claimed_count = len(_manifest_records(claimed_manifest, claim_path))
        if claim.get("volume") != claimed_volume or claim.get("puzzle_count") != claimed_count:
            raise RuntimeError(f"recorded prior count mismatch: {claim_path}")
        total += claimed_count
    if cross_volume.get("prior_puzzle_count") != total:
        raise RuntimeError(f"recorded prior total mismatch: {path}")


def _prior_collection_ids(prior: PriorCollection) -> set[str]:
    manifest = _read_manifest(prior.manifest_path)
    if (
        manifest.get("schema") not in SUPPORTED_MANIFEST_SCHEMAS
        or _manifest_volume(manifest, prior.manifest_path) != prior.volume
    ):
        raise RuntimeError(f"malformed prior collection manifest: {prior.manifest_path}")
    _validate_recorded_prior_counts(manifest, prior.manifest_path)
    ids: set[str] = set()
    for record in _manifest_records(manifest, prior.manifest_path):
        puzzle_path = _safe_owned_path(
            prior.artifact_root, record.get("puzzle_file"), "prior puzzle"
        )
        try:
            puzzle = parse_puzzle_bytes(puzzle_path.read_bytes())
        except (OSError, ValueError) as error:
            raise RuntimeError(f"malformed prior puzzle: {puzzle_path}") from error
        if puzzle.id != record.get("puzzle_id"):
            raise RuntimeError(f"prior manifest ID mismatch: {puzzle_path}")
        if puzzle.id in ids:
            raise RuntimeError(f"duplicate prior puzzle id: {puzzle.id}")
        ids.add(puzzle.id)
    return ids


def _prior_puzzle_ids(priors: tuple[PriorCollection, ...]) -> set[str]:
    ids: set[str] = set()
    for prior in priors:
        collection_ids = _prior_collection_ids(prior)
        duplicates = ids & collection_ids
        if duplicates:
            raise RuntimeError(
                f"duplicate puzzle ids across prior collections: {sorted(duplicates)}"
            )
        ids.update(collection_ids)
    return ids


def _validate_spec(spec: CollectionSpec) -> None:
    observed = tuple((page.number, page.size, page.profile) for page in spec.pages)
    expected = HISTORICAL_SIGNATURE if spec.volume <= 3 else SEVEN_PAGE_SIGNATURE
    if observed != expected or spec.volume not in set(range(1, 21)):
        raise RuntimeError(f"collection page specification is invalid: {observed}")
    if any(len(page.seeds) != 4 for page in spec.pages):
        raise RuntimeError("every collection page must contain exactly four seeds")
    seeds = [seed for page in spec.pages for seed in page.seeds]
    if re.fullmatch(r"[0-9]{8}xx", spec.seed_namespace) is None or any(
        isinstance(seed, bool)
        or not isinstance(seed, int)
        or seed < 0
        or seed > 2**64 - 1
        or str(seed)[:8] != spec.seed_namespace[:8]
        for seed in seeds
    ):
        raise RuntimeError("collection seeds do not match the fixed namespace")
    if spec.volume >= 4:
        expected_root = PDF_OUTPUT / f"volume-{spec.volume}"
        expected_name = (
            f"kenken-{_puzzle_count(spec)}-puzzle-collection-a4-volume-{spec.volume}.pdf"
        )
        if spec.package_root != expected_root or spec.collection_path != PDF_OUTPUT / expected_name:
            raise RuntimeError("collection output paths do not match the release identity")
        if [prior.volume for prior in spec.prior_collections] != list(range(1, spec.volume)):
            raise RuntimeError("collection prior chain is incomplete or out of order")


def _validate_build_target(spec: CollectionSpec) -> None:
    _validate_spec(spec)
    if spec.volume < 12:
        raise RuntimeError("historical collection specifications are read-only")
    if spec not in REVIEWED_RELEASE_BATCH:
        raise RuntimeError("collection specification is not in the reviewed release batch")
    if spec.package_root.exists() or spec.collection_path.exists():
        raise RuntimeError(f"collection target is already owned: Volume {spec.volume}")


def _new_release_path_allowed(path: Path, specs: tuple[CollectionSpec, ...]) -> bool:
    resolved = path.resolve()
    return any(
        resolved == spec.collection_path.resolve()
        or resolved.is_relative_to(spec.package_root.resolve())
        for spec in specs
    )


def _historical_inventory(specs: tuple[CollectionSpec, ...]) -> dict[Path, str]:
    return {
        path.resolve(): _sha256(path.read_bytes())
        for path in PDF_OUTPUT.rglob("*")
        if path.is_file() and not _new_release_path_allowed(path, specs)
    }


def _assert_historical_inventory(inventory: dict[Path, str]) -> None:
    mismatches = [
        path
        for path, expected in inventory.items()
        if not path.is_file() or _sha256(path.read_bytes()) != expected
    ]
    if mismatches:
        raise RuntimeError(f"historical release byte drift: {mismatches}")


def _preflight_release_batch(specs: tuple[CollectionSpec, ...]) -> dict[Path, str]:
    if specs != REVIEWED_RELEASE_BATCH:
        raise RuntimeError("only the exact reviewed release batch may be published")
    for spec in specs:
        _validate_build_target(spec)
    if len({spec.seed_namespace for spec in specs}) != len(specs):
        raise RuntimeError("new collection seed namespaces overlap")
    if any(
        first.collection_path == second.collection_path or first.package_root == second.package_root
        for index, first in enumerate(specs)
        for second in specs[index + 1 :]
    ):
        raise RuntimeError("new collection targets overlap")

    claimed_volumes: set[int] = set()
    claimed_namespaces: set[str] = set()
    for manifest_path in PDF_OUTPUT.glob("**/collection-manifest.json"):
        manifest = _read_manifest(manifest_path)
        claimed_volumes.add(_manifest_volume(manifest, manifest_path))
        generation = manifest.get("generation")
        if isinstance(generation, dict) and isinstance(generation.get("seed_namespace"), str):
            claimed_namespaces.add(generation["seed_namespace"])
    if claimed_volumes & {spec.volume for spec in specs}:
        raise RuntimeError("new collection volume is already claimed")
    if claimed_namespaces & {spec.seed_namespace for spec in specs}:
        raise RuntimeError("new collection seed namespace is already claimed")

    _prior_puzzle_ids(specs[0].prior_collections)
    return _historical_inventory(specs)


def build_collection(spec: CollectionSpec) -> None:
    """Build and transactionally publish one collection specification."""
    _validate_build_target(spec)
    sources = spec.package_root / "sources"
    spec.package_root.mkdir(parents=True, exist_ok=True)
    sources.mkdir(parents=True, exist_ok=True)
    spec.collection_path.parent.mkdir(parents=True, exist_ok=True)

    outputs: list[tuple[Path, bytes]] = []
    page_scenes = []
    page_records: list[dict[str, object]] = []
    artifact_hashes: dict[str, str] = {}
    puzzle_ids: set[str] = set()
    prior_counts = tuple(len(_prior_collection_ids(prior)) for prior in spec.prior_collections)
    prior_ids = _prior_puzzle_ids(spec.prior_collections)

    for page in spec.pages:
        verified_puzzles: list[VerifiedPuzzle] = []
        puzzle_records: list[dict[str, object]] = []
        for ordinal, seed in enumerate(page.seeds, start=1):
            config = GenerationConfig(
                page.size,
                seed,
                page.profile,
                max_attempts=MAX_ATTEMPTS,
                max_solver_nodes=MAX_SOLVER_NODES,
            )
            generated = generate(config)
            verified, result = verify(generated.puzzle, MAX_SOLVER_NODES)
            if verified is None or result.status != "unique":
                raise RuntimeError(f"{generated.puzzle.id} did not independently verify as unique")
            if verified.solution != generated.solution:
                raise RuntimeError(f"{generated.puzzle.id} solution changed during verification")
            difficulty = evaluate_difficulty(generated.puzzle, MAX_SOLVER_NODES)
            if difficulty is None or difficulty.band != page.profile:
                raise RuntimeError(
                    f"{generated.puzzle.id} does not match requested search-v1 profile"
                )
            if difficulty != generated.report.evaluated_difficulty:
                raise RuntimeError(
                    f"{generated.puzzle.id} report difficulty does not match evaluation"
                )
            if generated.puzzle.id in puzzle_ids:
                raise RuntimeError(f"duplicate puzzle id: {generated.puzzle.id}")
            if generated.puzzle.id in prior_ids:
                raise RuntimeError(f"cross-volume duplicate puzzle id: {generated.puzzle.id}")
            given_cages = count_given_cages(generated.puzzle.cages)
            given_limit = given_cage_cap(page.size, page.profile)
            if given_cages > given_limit:
                raise RuntimeError(
                    f"{generated.puzzle.id} has {given_cages} givens, limit {given_limit}"
                )
            if (
                generated.report.given_cage_policy.policy != GIVEN_CAGE_POLICY
                or generated.report.given_cage_policy.max_given_cages != given_limit
                or generated.report.given_cage_policy.accepted_given_cages != given_cages
            ):
                raise RuntimeError(
                    f"{generated.puzzle.id} report does not match observed given cages"
                )
            arithmetic_policy = evaluate_arithmetic_cage_policy(
                page.size, page.profile, generated.puzzle.cages
            )
            if (
                not arithmetic_policy.qualified
                or generated.report.arithmetic_cage_policy.policy != ARITHMETIC_CAGE_POLICY
                or generated.report.arithmetic_cage_policy.applicable
                != arithmetic_policy.applicable
                or generated.report.arithmetic_cage_policy.limits != arithmetic_policy.limits
                or generated.report.arithmetic_cage_policy.accepted_maxima
                != arithmetic_policy.observed_maxima
            ):
                raise RuntimeError(f"{generated.puzzle.id} report does not match arithmetic policy")
            puzzle_ids.add(generated.puzzle.id)
            verified_puzzles.append(verified)

            stem = _source_stem(page, ordinal, seed)
            puzzle_path = sources / f"{stem}.puzzle.json"
            solution_path = sources / f"{stem}.solution.json"
            report_path = sources / f"{stem}.report.json"
            solution = SolutionV1(
                "kenken.solution/v1",
                generated.puzzle.id,
                generated.solution,
            )
            source_artifacts = (
                (puzzle_path, serialize_puzzle_bytes(generated.puzzle)),
                (
                    solution_path,
                    serialize_solution_bytes(solution, generated.puzzle),
                ),
                (report_path, serialize_generation_report(generated.report)),
            )
            for path, data in source_artifacts:
                outputs.append((path, data))
                artifact_hashes[_relative_artifact_path(spec, path)] = _sha256(data)
            puzzle_records.append(
                {
                    "accepted_attempt": generated.report.accepted_attempt,
                    "given_cages": given_cages,
                    "ordinal": ordinal,
                    "puzzle_file": _relative_artifact_path(spec, puzzle_path),
                    "puzzle_id": generated.puzzle.id,
                    "report_file": _relative_artifact_path(spec, report_path),
                    "seed": str(seed),
                    "solution_file": _relative_artifact_path(spec, solution_path),
                }
            )

        scene = compose_page(verified_puzzles, "4up", "a4")
        page_scenes.append(scene)
        page_path = spec.package_root / f"{page.stem}.pdf"
        page_pdf = serialize_pdf(scene)
        outputs.append((page_path, page_pdf))
        artifact_hashes[_relative_artifact_path(spec, page_path)] = _sha256(page_pdf)
        page_records.append(
            {
                "page_number": page.number,
                "page_pdf": _relative_artifact_path(spec, page_path),
                "profile": page.profile,
                "puzzles": puzzle_records,
                "size": page.size,
            }
        )

    expected_puzzles = _puzzle_count(spec)
    if len(puzzle_ids) != expected_puzzles:
        raise RuntimeError(
            f"expected {expected_puzzles} distinct puzzle ids, found {len(puzzle_ids)}"
        )

    collection_pdf = serialize_pdf_pages(page_scenes)
    outputs.append((spec.collection_path, collection_pdf))
    collection_relative = _relative_artifact_path(spec, spec.collection_path)
    artifact_hashes[collection_relative] = _sha256(collection_pdf)

    cross_volume: dict[str, object] | None = None
    if spec.prior_collections:
        cross_volume = {
            "distinct_from_priors": True,
            "prior_collections": [
                {
                    "manifest": _relative_artifact_path(spec, prior.manifest_path),
                    "puzzle_count": count,
                    "volume": prior.volume,
                }
                for prior, count in zip(spec.prior_collections, prior_counts, strict=True)
            ],
            "prior_puzzle_count": len(prior_ids),
        }
    manifest = {
        "artifact_sha256": artifact_hashes,
        "collection_pdf": collection_relative,
        "cross_volume": cross_volume,
        "generation": {
            "arithmetic_cage_policy": {
                "applies_to_profiles": ["easy"],
                "limits": {
                    "max_add_target": EASY_ARITHMETIC_LIMITS.max_add_target,
                    "max_add_terms": EASY_ARITHMETIC_LIMITS.max_add_terms,
                    "max_cage_cells": EASY_ARITHMETIC_LIMITS.max_cage_cells,
                    "max_multiply_factors": (EASY_ARITHMETIC_LIMITS.max_multiply_factors),
                    "max_multiply_target": (EASY_ARITHMETIC_LIMITS.max_multiply_target),
                },
                "policy": ARITHMETIC_CAGE_POLICY,
            },
            "given_cage_policy": {
                "max_by_profile": {"easy": 4, "hard": 1, "medium": 2},
                "policy": GIVEN_CAGE_POLICY,
            },
            "max_attempts_per_puzzle": MAX_ATTEMPTS,
            "max_solver_nodes": MAX_SOLVER_NODES,
            "seed_namespace": spec.seed_namespace,
        },
        "page_geometry_points": {"height": "841.89", "width": "595.276"},
        "pages": page_records,
        "schema": "kenken.collection-manifest/v3",
        "volume": spec.volume,
    }
    if len(artifact_hashes) != _declared_artifact_count(spec):
        raise RuntimeError("collection artifact membership count is invalid")
    manifest_path = spec.package_root / "collection-manifest.json"
    manifest_bytes = (json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n").encode()
    outputs.append((manifest_path, manifest_bytes))
    _atomic_write_many(outputs)

    print(
        f"published Volume {spec.volume}: {len(page_scenes)} A4 pages and "
        f"{len(puzzle_ids)} distinct puzzles to {spec.collection_path}"
    )


def main() -> None:
    specs = REVIEWED_RELEASE_BATCH
    historical_inventory = _preflight_release_batch(specs)
    published_inventories: list[dict[Path, str]] = []
    for spec in specs:
        build_collection(spec)
        _assert_historical_inventory(historical_inventory)
        for inventory in published_inventories:
            _assert_historical_inventory(inventory)
        published_inventories.append(
            {
                path.resolve(): _sha256(path.read_bytes())
                for path in (*spec.package_root.rglob("*"), spec.collection_path)
                if path.is_file()
            }
        )
    new_paths = {
        path.resolve()
        for path in PDF_OUTPUT.rglob("*")
        if path.is_file() and path.resolve() not in historical_inventory
    }
    unexpected = [path for path in new_paths if not _new_release_path_allowed(path, specs)]
    if unexpected:
        raise RuntimeError(f"unexpected new release paths: {unexpected}")


if __name__ == "__main__":
    main()
