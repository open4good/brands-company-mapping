#!/usr/bin/env python3
"""One-shot migration of the brands-company-mapping referential from v2 to v3.

Changes:
  - brands-company-mapping.json: version 2 -> 3, drop the legacy top-level
    `companyNameSource` key.
  - company/*.json: drop the legacy flat `factoryLocations` / `scorings` fields,
    introduce the structured v3 slots (manufacturing / scores / xmetas / hq /
    identifiers / aliases / provenance), all initialised empty so the
    brands-maintenance agent can fill them in, sourced, batch by batch.

Idempotent: re-running on already-migrated files is a no-op.
"""
import json
import pathlib
import sys

REPO = pathlib.Path(__file__).resolve().parent.parent
TODAY = "2026-06-12"


def migrate_root() -> None:
    path = REPO / "brands-company-mapping.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["version"] = 3
    data.pop("companyNameSource", None)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"migrated {path.name}")


def migrate_company(path: pathlib.Path) -> None:
    data = json.loads(path.read_text(encoding="utf-8"))
    migrated = {
        "schemaVersion": 3,
        "id": data.get("id", path.stem),
        "name": data.get("name", ""),
        "aliases": data.get("aliases", []),
        "parentCompanyId": data.get("parentCompanyId"),
        "identifiers": data.get("identifiers", {}),
        "hq": data.get("hq"),
        "manufacturing": data.get("manufacturing", []),
        "scores": data.get("scores", {}),
        "xmetas": data.get("xmetas", []),
        "provenance": data.get("provenance"),
    }
    path.write_text(json.dumps(migrated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    migrate_root()
    company_dir = REPO / "company"
    count = 0
    for path in sorted(company_dir.glob("*.json")):
        migrate_company(path)
        count += 1
    print(f"migrated {count} company files")
    return 0


if __name__ == "__main__":
    sys.exit(main())
