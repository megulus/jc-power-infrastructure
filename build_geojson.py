#!/usr/bin/env python3
"""
build_geojson.py — convert the jc-power-infrastructure CSVs to GeoJSON.

Reads three source files:
  - intersections.csv       (intersection_id, latitude, longitude, notes)
  - segments.csv            (Option A schema; see DATA_DICTIONARY.md)
  - underground_features.csv (feature_id, segment_id, subtype, latitude,
                              longitude, imagery_date, notes)

Writes two GeoJSON FeatureCollections:
  - segments.geojson              (LineString per segment)
  - underground_features.geojson  (Point per feature)

Segment geometry is a straight line between the coordinates of its
from_intersection and to_intersection. This is symbolic block-face geometry,
not a surveyed conductor path (see DATA_DICTIONARY.md).

Usage:
    python build_geojson.py [--src DIR] [--out DIR]

Designed to fail loudly: if a segment references an intersection that isn't in
intersections.csv, or a coordinate is missing/unparseable, it reports the
offending row rather than emitting silently-broken geometry. Good for the
calibration smoke test.
"""

import argparse
import csv
import json
import sys
from pathlib import Path


# ---- field typing -----------------------------------------------------------
# Which segment columns are integers / booleans, so the GeoJSON carries real
# numbers and true/false rather than strings. Anything not listed stays a string.

SEGMENT_INT_FIELDS = {
    "primary_conductors",
    "pole_count",
    "transformer_count",
    "streetlight_count",
}
SEGMENT_BOOL_FIELDS = {
    "secondary_present",
    "joint_use",
}

TRUE_STRINGS = {"true", "t", "yes", "y", "1"}
FALSE_STRINGS = {"false", "f", "no", "n", "0", ""}


def parse_bool(value, row_id, field):
    v = (value or "").strip().lower()
    if v in TRUE_STRINGS:
        return True
    if v in FALSE_STRINGS:
        return False
    raise ValueError(
        f"segment '{row_id}': field '{field}' = {value!r} is not a boolean"
    )


def parse_int(value, row_id, field):
    v = (value or "").strip()
    if v == "":
        return 0  # empty tally cell = 0 (see underground convention in the dict)
    try:
        return int(v)
    except ValueError:
        raise ValueError(
            f"segment '{row_id}': field '{field}' = {value!r} is not an integer"
        )


def parse_coord(value, row_id, which):
    v = (value or "").strip()
    if v == "":
        raise ValueError(f"'{row_id}': missing {which}")
    try:
        return float(v)
    except ValueError:
        raise ValueError(f"'{row_id}': {which} = {value!r} is not a number")


# ---- readers ----------------------------------------------------------------

def read_csv(path):
    if not path.exists():
        raise FileNotFoundError(f"expected file not found: {path}")
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_intersections(path):
    """Return {intersection_id: (lon, lat)}. GeoJSON is (lon, lat) order."""
    coords = {}
    for row in read_csv(path):
        iid = (row.get("intersection_id") or "").strip()
        if not iid:
            continue
        lat = parse_coord(row.get("latitude"), iid, "latitude")
        lon = parse_coord(row.get("longitude"), iid, "longitude")
        coords[iid] = (lon, lat)
    if not coords:
        raise ValueError("no intersections loaded — is intersections.csv empty?")
    return coords


# ---- feature builders -------------------------------------------------------

def build_segment_features(rows, intersections):
    features = []
    errors = []
    for row in rows:
        sid = (row.get("segment_id") or "").strip()
        if not sid:
            continue
        frm = (row.get("from_intersection") or "").strip()
        to = (row.get("to_intersection") or "").strip()

        # geometry lookup — the most likely smoke-test failure, so be explicit
        missing = [i for i in (frm, to) if i not in intersections]
        if missing:
            errors.append(
                f"segment '{sid}': intersection(s) not found in "
                f"intersections.csv: {', '.join(missing)}"
            )
            continue

        try:
            props = {}
            for k, v in row.items():
                if k in ("from_intersection", "to_intersection"):
                    props[k] = v
                elif k in SEGMENT_INT_FIELDS:
                    props[k] = parse_int(v, sid, k)
                elif k in SEGMENT_BOOL_FIELDS:
                    props[k] = parse_bool(v, sid, k)
                else:
                    props[k] = v
        except ValueError as e:
            errors.append(str(e))
            continue

        features.append({
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    list(intersections[frm]),
                    list(intersections[to]),
                ],
            },
            "properties": props,
        })
    return features, errors


def build_underground_features(rows):
    features = []
    errors = []
    for row in rows:
        fid = (row.get("feature_id") or "").strip()
        if not fid:
            continue
        try:
            lat = parse_coord(row.get("latitude"), fid, "latitude")
            lon = parse_coord(row.get("longitude"), fid, "longitude")
        except ValueError as e:
            errors.append(str(e))
            continue
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {k: v for k, v in row.items()
                           if k not in ("latitude", "longitude")},
        })
    return features, errors


def collection(features):
    return {"type": "FeatureCollection", "features": features}


# ---- main -------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(description="Build GeoJSON from the project CSVs.")
    ap.add_argument("--src", default=".", help="directory holding the CSVs")
    ap.add_argument("--out", default=".", help="directory to write GeoJSON into")
    args = ap.parse_args()

    src = Path(args.src)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    try:
        intersections = load_intersections(src / "intersections.csv")
        seg_rows = read_csv(src / "segments.csv")
        seg_features, seg_errors = build_segment_features(seg_rows, intersections)

        uf_path = src / "underground_features.csv"
        if uf_path.exists():
            uf_rows = read_csv(uf_path)
            uf_features, uf_errors = build_underground_features(uf_rows)
        else:
            uf_features, uf_errors = [], []
            print("note: underground_features.csv not found — skipping", file=sys.stderr)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

    all_errors = seg_errors + uf_errors
    if all_errors:
        print(f"Completed with {len(all_errors)} row error(s):", file=sys.stderr)
        for e in all_errors:
            print(f"  - {e}", file=sys.stderr)

    (out / "segments.geojson").write_text(
        json.dumps(collection(seg_features), indent=2), encoding="utf-8")
    (out / "underground_features.geojson").write_text(
        json.dumps(collection(uf_features), indent=2), encoding="utf-8")

    print(f"Wrote {len(seg_features)} segment feature(s) -> {out/'segments.geojson'}")
    print(f"Wrote {len(uf_features)} underground feature(s) -> "
          f"{out/'underground_features.geojson'}")
    if all_errors:
        print("Some rows were skipped — see errors above.", file=sys.stderr)
        sys.exit(2)


if __name__ == "__main__":
    main()
