#!/usr/bin/env python3
"""Validate the brands-company-mapping referential and every company file
against the v3 JSON schemas. Exits non-zero on the first violation.

Usage: python3 scripts/validate.py
Requires: pip install jsonschema
"""
import json
import pathlib
import sys

try:
    from jsonschema import Draft202012Validator
except ImportError:
    print("Missing dependency: pip install jsonschema", file=sys.stderr)
    sys.exit(2)

REPO = pathlib.Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO / "schema"


def load(path: pathlib.Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(path: pathlib.Path, validator: "Draft202012Validator") -> int:
    errors = sorted(validator.iter_errors(load(path)), key=lambda e: e.path)
    for err in errors:
        location = "/".join(str(p) for p in err.path) or "<root>"
        print(f"  {path.relative_to(REPO)} :: {location}: {err.message}", file=sys.stderr)
    return len(errors)


def main() -> int:
    root_validator = Draft202012Validator(load(SCHEMA_DIR / "brands-company-mapping.schema.json"))
    company_validator = Draft202012Validator(load(SCHEMA_DIR / "company.schema.json"))

    total = validate(REPO / "brands-company-mapping.json", root_validator)
    companies = 0
    for path in sorted((REPO / "company").glob("*.json")):
        total += validate(path, company_validator)
        companies += 1

    if total:
        print(f"FAILED: {total} schema violation(s)", file=sys.stderr)
        return 1
    print(f"OK: referential + {companies} company files valid against v3 schema")
    return 0


if __name__ == "__main__":
    sys.exit(main())
