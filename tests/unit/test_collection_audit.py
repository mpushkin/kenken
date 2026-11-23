from __future__ import annotations

import hashlib
import importlib.util
import json
import shutil
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest

ROOT = Path(__file__).parents[2]


def _audit_module() -> ModuleType:
    path = ROOT / "scripts" / "audit_collection.py"
    spec = importlib.util.spec_from_file_location("collection_audit_under_test", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)


def _prior_paths(volume: int, pdf_root: Path) -> tuple[Path, Path]:
    root = pdf_root if volume == 1 else pdf_root / f"volume-{volume}"
    return root, root / "collection-manifest.json"


def _materialize_audit_root(destination: Path, pdf_root: Path) -> dict[str, Any]:
    schemas = destination / "schemas"
    _copy(
        ROOT / "schemas" / "kenken-collection-manifest-v3.schema.json",
        schemas / "kenken-collection-manifest-v3.schema.json",
    )
    _copy(
        ROOT / "schemas" / "kenken-generation-report-v3.schema.json",
        schemas / "kenken-generation-report-v3.schema.json",
    )

    destination_pdf = destination / "output" / "pdf"
    for volume in (1, 2, 3):
        artifact_root, manifest_path = _prior_paths(volume, pdf_root)
        manifest = json.loads(manifest_path.read_text())
        destination_root = (
            destination_pdf if volume == 1 else destination_pdf / f"volume-{volume}"
        )
        _copy(manifest_path, destination_root / "collection-manifest.json")
        for page in manifest["pages"]:
            for record in page["puzzles"]:
                _copy(
                    artifact_root / record["puzzle_file"],
                    destination_root / record["puzzle_file"],
                )

    source_package = pdf_root / "volume-4"
    destination_package = destination_pdf / "volume-4"
    (destination_package / "qa").mkdir(parents=True)
    manifest_path = source_package / "collection-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    for relative in manifest["artifact_sha256"]:
        _copy(
            (source_package / relative).resolve(),
            (destination_package / relative).resolve(),
        )
    _copy(manifest_path, destination_package / "collection-manifest.json")
    return manifest


def _audit_spec(module: ModuleType, manifest: dict[str, Any]) -> Any:
    return module.AuditSpec(
        volume=4,
        seed_namespace=manifest["generation"]["seed_namespace"],
        pages=tuple(
            (
                page["page_number"],
                page["size"],
                page["profile"],
                tuple(int(record["seed"]) for record in page["puzzles"]),
            )
            for page in manifest["pages"]
        ),
        attempts=tuple(
            tuple(record["accepted_attempt"] for record in page["puzzles"])
            for page in manifest["pages"]
        ),
        prior_counts=(24, 24, 24),
    )


def test_historical_collection_passes_audit_before_mutation(
    tmp_path: Path, collection_project: Path
) -> None:
    module = _audit_module()
    manifest = _materialize_audit_root(tmp_path, collection_project / "output" / "pdf")
    module.audit_collection(tmp_path, _audit_spec(module, manifest))
    results = tmp_path / "output" / "pdf" / "volume-4" / "qa" / "audit-results.json"
    report = json.loads(results.read_bytes())
    assert report["puzzles_checked"] == 28
    assert report["prior_puzzle_ids"] == 72
    assert report["manifest_hashes_checked"] == 92


@pytest.mark.parametrize(
    ("field", "message"),
    [
        ("attempts", "report attempts"),
        ("difficulty_band", "report difficulty"),
    ],
)
def test_audit_rejects_hashed_report_semantic_mutations(
    tmp_path: Path, field: str, message: str, collection_project: Path
) -> None:
    module = _audit_module()
    manifest = _materialize_audit_root(tmp_path, collection_project / "output" / "pdf")
    package = tmp_path / "output" / "pdf" / "volume-4"
    report_relative = manifest["pages"][0]["puzzles"][0]["report_file"]
    report_path = package / report_relative
    report = json.loads(report_path.read_text())
    if field == "attempts":
        report["attempts"] += 1
    else:
        report["evaluated_difficulty"]["band"] = "medium"
    report_bytes = (
        json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode()
    report_path.write_bytes(report_bytes)
    manifest["artifact_sha256"][report_relative] = hashlib.sha256(
        report_bytes
    ).hexdigest()
    (package / "collection-manifest.json").write_text(
        json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n"
    )

    with pytest.raises(AssertionError, match=message):
        module.audit_collection(tmp_path, _audit_spec(module, manifest))
