#!/usr/bin/env python3
"""Round-trip check a STEP file with CadQuery/OpenCascade.

This verifies file readability, solid count, units when detectable from the STEP
text, and the overall bounding box. It does not validate design correctness,
fit, strength, safety, manufacturability, or compliance.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="STEP file to verify")
    parser.add_argument("--expected-solids", type=int, help="Expected imported solid count")
    parser.add_argument("--output", type=Path, help="Optional JSON output path")
    parser.add_argument(
        "--cadquery-path",
        type=Path,
        help="Optional directory containing a workspace-local CadQuery installation",
    )
    return parser.parse_args()


def detect_units(step_text: str) -> str:
    upper = step_text.upper()
    if "SI_UNIT(.MILLI.,.METRE.)" in upper:
        return "millimetres"
    if "SI_UNIT($,.METRE.)" in upper or "SI_UNIT(.NONE.,.METRE.)" in upper:
        return "metres"
    if "CONVERSION_BASED_UNIT('INCH'" in upper:
        return "inches"
    return "unknown"


def detect_schema(step_text: str) -> str:
    upper = step_text.upper()
    marker = "FILE_SCHEMA(("
    start = upper.find(marker)
    if start < 0:
        return "unknown"
    end = upper.find("));", start)
    if end < 0:
        return "unknown"
    return step_text[start + len(marker) : end].strip()


def main() -> int:
    args = parse_args()
    if args.cadquery_path:
        sys.path.insert(0, str(args.cadquery_path.resolve()))

    try:
        import cadquery as cq
        from cadquery import importers
    except ImportError as exc:
        print(
            "Error: CadQuery is required for round-trip verification. "
            "Use --cadquery-path for a workspace-local installation.",
            file=sys.stderr,
        )
        print(str(exc), file=sys.stderr)
        return 2

    input_path = args.input.resolve()
    if not input_path.is_file():
        print(f"Error: STEP file not found: {input_path}", file=sys.stderr)
        return 2

    raw = input_path.read_text(encoding="utf-8", errors="ignore")
    valid_header = raw.lstrip().startswith("ISO-10303-21;")

    try:
        imported = importers.importStep(str(input_path))
        solids = imported.solids().vals()
    except Exception as exc:  # OpenCascade raises several backend-specific types.
        print(f"Error: STEP import failed: {exc}", file=sys.stderr)
        return 2

    if solids:
        boxes = [solid.BoundingBox() for solid in solids]
        xmin = min(box.xmin for box in boxes)
        xmax = max(box.xmax for box in boxes)
        ymin = min(box.ymin for box in boxes)
        ymax = max(box.ymax for box in boxes)
        zmin = min(box.zmin for box in boxes)
        zmax = max(box.zmax for box in boxes)
        bounding_box = {
            "x_length": round(xmax - xmin, 3),
            "y_length": round(ymax - ymin, 3),
            "z_length": round(zmax - zmin, 3),
            "x_min": round(xmin, 3),
            "x_max": round(xmax, 3),
            "y_min": round(ymin, 3),
            "y_max": round(ymax, 3),
            "z_min": round(zmin, 3),
            "z_max": round(zmax, 3),
        }
    else:
        bounding_box = None

    count_pass = args.expected_solids is None or len(solids) == args.expected_solids
    result = {
        "file": str(input_path),
        "size_bytes": input_path.stat().st_size,
        "valid_iso_10303_header": valid_header,
        "schema": detect_schema(raw),
        "units_detected": detect_units(raw),
        "imported_solid_count": len(solids),
        "expected_solid_count": args.expected_solids,
        "solid_count_pass": count_pass,
        "round_trip_import_pass": bool(solids),
        "bounding_box": bounding_box,
        "overall_pass": valid_header and bool(solids) and count_pass,
        "limitations": [
            "File integrity does not validate geometry correctness or interface fit.",
            "This check does not validate strength, safety, manufacturability, regulatory compliance, or production readiness.",
        ],
    }

    rendered = json.dumps(result, indent=2)
    if args.output:
        args.output.write_text(rendered + "\n", encoding="utf-8")
    print(rendered)
    return 0 if result["overall_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

