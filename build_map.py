#!/usr/bin/env python3
"""
build_map.py — minimal Folium map of the segments GeoJSON.

Colors each street segment by its `overhead_underground` class and writes a
single self-contained HTML file. Deliberately minimal: two colors, the
segments, a basemap, a small legend. No layer toggles, no per-field popups
beyond the essentials.

Usage:
    python build_map.py [--src data/processed/segments.geojson] [--out data/processed/map.html]
"""

import argparse
import json
import sys
from pathlib import Path

import folium


# overhead/underground -> line color
COLORS = {
    "overhead": "#d62728",     # red
    "underground": "#1f77b4",  # blue
    "mixed": "#9467bd",        # purple
    "unknown": "#7f7f7f",      # gray
}
DEFAULT_COLOR = "#7f7f7f"


def load_segments(path):
    if not path.exists():
        print(f"ERROR: {path} not found. Run build_geojson.py first.", file=sys.stderr)
        sys.exit(1)
    data = json.loads(path.read_text(encoding="utf-8"))
    feats = data.get("features", [])
    if not feats:
        print(f"ERROR: {path} has no features.", file=sys.stderr)
        sys.exit(1)
    return feats


def all_coords(features):
    pts = []
    for f in features:
        geom = f.get("geometry") or {}
        if geom.get("type") == "LineString":
            pts.extend(geom.get("coordinates", []))
    return pts


def center_of(features):
    pts = all_coords(features)
    lons = [p[0] for p in pts]
    lats = [p[1] for p in pts]
    return [sum(lats) / len(lats), sum(lons) / len(lons)]


def add_legend(m):
    present = """
    <div style="position: fixed; bottom: 24px; left: 24px; z-index: 9999;
                background: white; padding: 10px 14px; border: 1px solid #999;
                border-radius: 4px; font: 13px sans-serif; line-height: 1.6;">
      <b>Distribution</b><br>
      <span style="color:#d62728;">&#9644;</span> Overhead<br>
      <span style="color:#1f77b4;">&#9644;</span> Underground<br>
      <span style="color:#9467bd;">&#9644;</span> Mixed<br>
      <span style="color:#7f7f7f;">&#9644;</span> Unknown
    </div>
    """
    m.get_root().html.add_child(folium.Element(present))


def main():
    ap = argparse.ArgumentParser(description="Minimal Folium map of segments.")
    ap.add_argument("--src", default="data/processed/segments.geojson")
    ap.add_argument("--out", default="data/processed/map.html")
    args = ap.parse_args()

    features = load_segments(Path(args.src))

    m = folium.Map(location=center_of(features), zoom_start=16, tiles="CartoDB positron")

    for f in features:
        geom = f.get("geometry") or {}
        if geom.get("type") != "LineString":
            continue
        props = f.get("properties", {})
        cls = (props.get("overhead_underground") or "unknown").strip().lower()
        color = COLORS.get(cls, DEFAULT_COLOR)

        # GeoJSON is [lon, lat]; folium wants [lat, lon]
        latlons = [[c[1], c[0]] for c in geom["coordinates"]]

        tooltip = props.get("segment_id", "")
        popup = folium.Popup(
            f"<b>{props.get('segment_id','')}</b><br>"
            f"class: {props.get('overhead_underground','')}<br>"
            f"primary side: {props.get('primary_side','')}<br>"
            f"poles: {props.get('pole_count','')} &nbsp; "
            f"transformers: {props.get('transformer_count','')}",
            max_width=280,
        )

        folium.PolyLine(
            latlons, color=color, weight=5, opacity=0.85,
            tooltip=tooltip, popup=popup,
        ).add_to(m)

    add_legend(m)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    m.save(str(out))
    print(f"Wrote map with {len(features)} segment(s) -> {out}")


if __name__ == "__main__":
    main()
