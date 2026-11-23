from __future__ import annotations

import importlib.util
import json
import sys
from dataclasses import replace
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

ROOT = Path(__file__).parents[2]


def _builder(root: Path = ROOT) -> ModuleType:
    path = root / "scripts" / "build_collection.py"
    spec = importlib.util.spec_from_file_location("build_collection", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _signature(spec: Any) -> tuple[tuple[int, int, str], ...]:
    return tuple((page.number, page.size, page.profile) for page in spec.pages)


def _source_puzzles(root: Path) -> list[Path]:
    paths = sorted((root / "output" / "pdf").glob("**/*.puzzle.json"))
    unique: dict[str, Path] = {}
    for path in paths:
        payload = json.loads(path.read_text())
        unique.setdefault(payload["id"], path)
    return list(unique.values())


def _write_prior(
    builder: ModuleType,
    manifest_path: Path,
    artifact_root: Path,
    volume: int,
    sources: list[Path],
    *,
    schema: str = "kenken.collection-manifest/v1",
    cross_volume: dict[str, object] | None = None,
) -> Any:
    records = []
    source_root = artifact_root / "sources"
    source_root.mkdir(parents=True, exist_ok=True)
    for index, source in enumerate(sources, start=1):
        destination = source_root / f"puzzle-{index:02d}.json"
        destination.write_bytes(source.read_bytes())
        records.append(
            {
                "puzzle_file": f"sources/{destination.name}",
                "puzzle_id": json.loads(source.read_text())["id"],
            }
        )
    manifest: dict[str, object] = {
        "schema": schema,
        "volume": volume,
        "pages": [{"puzzles": records}],
    }
    if cross_volume is not None:
        manifest["cross_volume"] = cross_volume
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.write_text(json.dumps(manifest))
    return builder.PriorCollection(volume, manifest_path, artifact_root)


def test_collection_specs_keep_historical_contract_and_add_seven_page_releases() -> None:
    builder = _builder()

    for spec in (builder.VOLUME_1, builder.VOLUME_2, builder.VOLUME_3):
        assert _signature(spec) == builder.HISTORICAL_SIGNATURE
        builder._validate_spec(spec)
    seven_page_specs = tuple(
        getattr(builder, f"VOLUME_{volume}") for volume in range(4, 21)
    )
    for spec in seven_page_specs:
        assert _signature(spec) == builder.SEVEN_PAGE_SIGNATURE
        assert all(len(page.seeds) == 4 for page in spec.pages)
        assert {str(seed)[:8] for page in spec.pages for seed in page.seeds} == {
            spec.seed_namespace[:8]
        }
        builder._validate_spec(spec)

    assert [prior.volume for prior in builder.VOLUME_4.prior_collections] == [1, 2, 3]
    assert [prior.volume for prior in builder.VOLUME_5.prior_collections] == [1, 2, 3, 4]
    assert [prior.volume for prior in builder.VOLUME_6.prior_collections] == [
        1,
        2,
        3,
        4,
        5,
    ]
    assert [prior.volume for prior in builder.VOLUME_7.prior_collections] == [
        1,
        2,
        3,
        4,
        5,
        6,
    ]
    for volume in range(8, 21):
        spec = getattr(builder, f"VOLUME_{volume}")
        assert [prior.volume for prior in spec.prior_collections] == list(range(1, volume))
    all_specs = tuple(getattr(builder, f"VOLUME_{volume}") for volume in range(1, 21))
    assert len({spec.collection_path for spec in all_specs}) == 20
    assert all_specs[11:] == builder.REVIEWED_RELEASE_BATCH
    for spec in seven_page_specs:
        assert spec.collection_path.name.startswith("kenken-28-puzzle-")


def test_composition_counts_are_derived_from_pages() -> None:
    builder = _builder()

    for volume in range(4, 21):
        spec = getattr(builder, f"VOLUME_{volume}")
        assert builder._puzzle_count(spec) == 28
        assert builder._source_json_count(spec) == 84
        assert builder._declared_artifact_count(spec) == 92
        assert builder._compared_byte_set_count(spec) == 93
    assert builder._puzzle_count(builder.VOLUME_3) == 24
    assert builder._declared_artifact_count(builder.VOLUME_3) == 79
    assert builder._compared_byte_set_count(builder.VOLUME_3) == 80


@pytest.mark.parametrize(
    "mutator, message",
    [
        (lambda b, s: replace(s, pages=s.pages[:-1]), "page specification"),
        (
            lambda b, s: replace(s, pages=(*s.pages, s.pages[-1])),
            "page specification",
        ),
        (
            lambda b, s: replace(
                s,
                pages=(
                    s.pages[1],
                    s.pages[0],
                    *s.pages[2:],
                ),
            ),
            "page specification",
        ),
        (
            lambda b, s: replace(
                s,
                pages=(
                    replace(s.pages[0], seeds=s.pages[0].seeds[:3]),
                    *s.pages[1:],
                ),
            ),
            "exactly four",
        ),
        (
            lambda b, s: replace(s, seed_namespace="99999999xx"),
            "fixed namespace",
        ),
        (
            lambda b, s: replace(s, collection_path=s.collection_path.with_name("wrong.pdf")),
            "output paths",
        ),
        (
            lambda b, s: replace(s, prior_collections=s.prior_collections[:-1]),
            "prior chain",
        ),
    ],
)
def test_invalid_seven_page_specs_stop_before_output(mutator: Any, message: str) -> None:
    builder = _builder()

    with pytest.raises(RuntimeError, match=message):
        builder._validate_spec(mutator(builder, builder.VOLUME_4))


def test_historical_build_targets_are_read_only() -> None:
    builder = _builder()

    with pytest.raises(RuntimeError, match="historical"):
        builder._validate_build_target(builder.VOLUME_5)


def test_only_exact_reviewed_batch_specs_are_buildable() -> None:
    builder = _builder()
    changed_page = replace(
        builder.VOLUME_12.pages[0],
        seeds=(2026080599, *builder.VOLUME_12.pages[0].seeds[1:]),
    )
    changed_spec = replace(
        builder.VOLUME_12,
        pages=(changed_page, *builder.VOLUME_12.pages[1:]),
    )

    with pytest.raises(RuntimeError, match="reviewed release batch"):
        builder._validate_build_target(changed_spec)


def test_volume_12_through_20_preflight_and_path_allowlist_are_exact(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    builder = _builder()
    builder.PDF_OUTPUT = tmp_path
    reviewed = tuple(
        replace(
            spec,
            package_root=tmp_path / f"volume-{spec.volume}",
            collection_path=(
                tmp_path
                / f"kenken-28-puzzle-collection-a4-volume-{spec.volume}.pdf"
            ),
        )
        for spec in builder.REVIEWED_RELEASE_BATCH
    )
    builder.REVIEWED_RELEASE_BATCH = reviewed
    monkeypatch.setattr(builder, "_prior_puzzle_ids", lambda _priors: set())
    monkeypatch.setattr(builder, "_historical_inventory", lambda _specs: {})

    assert builder._preflight_release_batch(reviewed) == {}
    with pytest.raises(RuntimeError, match="exact reviewed release batch"):
        builder._preflight_release_batch(())
    with pytest.raises(RuntimeError, match="exact reviewed release batch"):
        builder._preflight_release_batch(tuple(reversed(reviewed)))

    assert builder._new_release_path_allowed(reviewed[0].collection_path, reviewed)
    assert builder._new_release_path_allowed(
        reviewed[-1].package_root / "sources" / "puzzle.json", reviewed
    )
    assert not builder._new_release_path_allowed(tmp_path / "outside.json", reviewed)


def test_plural_prior_reader_requires_72_distinct_canonical_ids(collection_project: Path) -> None:
    builder = _builder(collection_project)

    prior_ids = builder._prior_puzzle_ids(builder.VOLUME_4.prior_collections)
    assert len(prior_ids) == 72

    volume_1 = builder.VOLUME_4.prior_collections[0]
    with pytest.raises(RuntimeError, match="across prior collections"):
        builder._prior_puzzle_ids((volume_1, volume_1))


def test_volume_6_rejects_all_128_prior_ids(collection_project: Path) -> None:
    builder = _builder(collection_project)

    prior_ids = builder._prior_puzzle_ids(builder.VOLUME_6.prior_collections)

    assert len(prior_ids) == 128


@pytest.mark.parametrize(
    ("spec_name", "expected_prior_count"),
    [
        ("VOLUME_8", 184),
        ("VOLUME_9", 212),
        ("VOLUME_10", 240),
        ("VOLUME_11", 268),
        ("VOLUME_12", 296),
        ("VOLUME_13", 324),
        ("VOLUME_14", 352),
        ("VOLUME_15", 380),
        ("VOLUME_16", 408),
        ("VOLUME_17", 436),
        ("VOLUME_18", 464),
        ("VOLUME_19", 492),
        ("VOLUME_20", 520),
    ],
)
def test_volume_8_through_20_reject_complete_prior_chain(
    spec_name: str, expected_prior_count: int, collection_project: Path
) -> None:
    builder = _builder(collection_project)
    spec = getattr(builder, spec_name)

    prior_ids = builder._prior_puzzle_ids(spec.prior_collections)

    assert len(prior_ids) == expected_prior_count
    assert expected_prior_count + builder._puzzle_count(spec) == 28 * spec.volume - 12


def test_prior_reader_accepts_28_puzzle_v3_and_checks_recorded_counts(
    tmp_path: Path, collection_project: Path,
) -> None:
    builder = _builder()
    builder.PDF_OUTPUT = tmp_path
    sources = _source_puzzles(collection_project)
    assert len(sources) >= 72

    _write_prior(
        builder,
        tmp_path / "collection-manifest.json",
        tmp_path / "volume-1-owned",
        1,
        sources[:24],
    )
    _write_prior(
        builder,
        tmp_path / "volume-2" / "collection-manifest.json",
        tmp_path / "volume-2",
        2,
        sources[24:48],
    )
    prior = _write_prior(
        builder,
        tmp_path / "volume-4" / "collection-manifest.json",
        tmp_path / "volume-4",
        4,
        sources[:28],
        schema="kenken.collection-manifest/v3",
        cross_volume={
            "distinct_from_priors": True,
            "prior_collections": [
                {
                    "manifest": "../collection-manifest.json",
                    "puzzle_count": 24,
                    "volume": 1,
                },
                {
                    "manifest": "../volume-2/collection-manifest.json",
                    "puzzle_count": 24,
                    "volume": 2,
                },
            ],
            "prior_puzzle_count": 48,
        },
    )
    assert len(builder._prior_collection_ids(prior)) == 28

    manifest = json.loads(prior.manifest_path.read_text())
    manifest["cross_volume"]["prior_collections"][1]["puzzle_count"] = 23
    prior.manifest_path.write_text(json.dumps(manifest))
    with pytest.raises(RuntimeError, match="recorded prior count mismatch"):
        builder._prior_collection_ids(prior)


@pytest.mark.parametrize(
    ("schema", "volume", "puzzle_file", "message"),
    [
        ("kenken.collection-manifest/v99", 4, "sources/puzzle.json", "malformed"),
        (
            "kenken.collection-manifest/v2",
            None,
            "sources/puzzle.json",
            "only a v1 Volume 1",
        ),
        (
            "kenken.collection-manifest/v1",
            4,
            "../escape.json",
            "escapes its artifact root",
        ),
    ],
)
def test_prior_reader_rejects_unknown_versions_illegal_omission_and_path_escape(
    tmp_path: Path,
    schema: str,
    volume: int | None,
    puzzle_file: str,
    message: str,
) -> None:
    builder = _builder()
    artifact_root = tmp_path / "owned"
    artifact_root.mkdir()
    manifest = {
        "schema": schema,
        "pages": [{"puzzles": [{"puzzle_file": puzzle_file, "puzzle_id": "x"}]}],
    }
    if volume is not None:
        manifest["volume"] = volume
    manifest_path = tmp_path / "manifest.json"
    manifest_path.write_text(json.dumps(manifest))
    prior = builder.PriorCollection(4, manifest_path, artifact_root)

    with pytest.raises(RuntimeError, match=message):
        builder._prior_collection_ids(prior)
