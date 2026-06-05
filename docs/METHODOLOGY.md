# Methodology

How segments in this dataset are classified, what is observed versus inferred,
where classification can go wrong, and how the method is validated.

## What is actually being observed

This dataset does not map underground cables. Buried conductors are invisible
from the street, from aerial imagery, and from any source available without
utility as-built drawings. Mapping them directly is not possible here.

Instead, each block-face segment is classified by the **presence or absence of
overhead distribution infrastructure** — utility poles, overhead primary
conductors, and the associated hardware (transformers, risers, service drops).
This is reliably observable from street-level imagery. Undergrounding is then
the inferred complement: a block face with no poles and no overhead distribution
conductor is classified as underground, because the customers on it are
necessarily served from below.

This reframing matters. The dataset measures the thing that can be seen
(overhead presence) and treats the underground class as the residual, rather
than claiming to locate something that cannot be seen. A segment coded
`underground` is a statement that no overhead distribution was visible along
that block face — not a claim about the cable's path, depth, or existence in any
specific location.

## Data sources

Classification is performed primarily from **Google Street View and Google
Earth imagery**. For blocks within walking distance of the author's residence,
imagery-based classification is cross-checked against direct field observation
(see *Validation* below). The remainder of the corridor is classified from
imagery alone.

## Decision rule

A segment's `overhead_underground` value keys on the **overhead primary or
distribution conductor**, not on service drops to individual buildings. A block
with overhead primary on poles is `overhead` even where some buildings receive
buried service connections; a block with no poles and no overhead distribution
conductor is `underground` even if streetlight or telecom wiring is present.
Where this rule is ambiguous (see below), the ambiguity is recorded in the
segment's `notes` field rather than silently resolved.

## Known sources of classification error

Three failure modes are inherent to imagery-based classification and are not
fully eliminated in this release:

- **Rear-lot and alley feeds.** Some block faces are served by distribution
  lines running behind the buildings rather than along the street frontage.
  Street View down the street frontage can miss these, causing an overhead block
  to be misclassified as underground. Jersey City's denser blocks have few
  service alleys, but they exist.
- **Hybrid configurations.** Overhead primary with underground service drops, or
  underground low-voltage with overhead medium-voltage, do not fit a clean
  binary. The decision rule above keys on the overhead primary to make these
  cases deterministic, but the binary necessarily flattens real variation.
- **Imagery vintage.** Street View capture dates within the Phase I area range
  across multiple years. A block undergrounded after its imagery was captured
  will be classified from stale evidence. The capture date visible in Street
  View is recorded per observation (`imagery_date`) so that staleness is
  auditable rather than hidden.

## Validation

The blocks within direct field-verification range serve as a validation sample.
Each was classified blind from imagery first, then checked against ground-truth
field observation. The agreement rate between imagery-based and field-verified
classification is reported in the repository as a measured accuracy figure for
the method, rather than asserted. This converts the dataset from a set of
individual judgments into a method with a known error rate on its validation
sample.

Note: the validation sample is small and geographically clustered; the reported
agreement rate characterizes the method on these blocks, not a guaranteed
accuracy across the full corridor.

## OpenStreetMap coverage check

The README claims that no comparable block-level classification exists for this
area. The OpenStreetMap portion of that claim is verifiable, so it was checked
directly rather than asserted.

On 2026-06-05, OSM was queried via the Overpass API for all `power=*` features
within the Phase I corridor bounding box, covering power lines
(`line`/`minor_line`/`cable`), poles and towers, and any other power-tagged
nodes, ways, or relations. The query returned a single feature: a rooftop solar
array (`power=generator`, `generator:source=solar`, `location=roof`). It
returned no distribution lines, no poles, and nothing carrying an
overhead/underground `location` tag.

The rooftop generator is unrelated to distribution infrastructure and is
expected noise from the catch-all `power=*` match; anyone re-running the query
should disregard it. The substantive result is that OSM provides no distribution
classification for the corridor. Because OSM is live data, the query date is
recorded so the finding can be re-verified; the gap may close if contributors
add features later.

The exact Overpass query used, runnable at overpass-turbo.eu, was:

```
[out:json][timeout:60];
// Phase I corridor bounding box: (south, west, north, east)
(
  way["power"~"^(line|minor_line|cable)$"](40.7112, -74.0435, 40.7190, -74.0331);
  node["power"~"^(pole|tower)$"](40.7112, -74.0435, 40.7190, -74.0331);
  nwr["power"](40.7112, -74.0435, 40.7190, -74.0331);
);
out geom;
```

The bounding box approximates the Phase I corridor (Marin Boulevard west,
Columbus Drive north, the Hudson River east, the Hudson-Bergen Light Rail
tracks south); adjust the four coordinates to re-run against a different extent.

## Workflow summary

Data is collected into four CSV files (intersections, segments, poles,
underground features), edited in VS Code with the Rainbow CSV extension, with
coordinates captured via Google Maps right-click. A Python script converts the
CSVs to GeoJSON. A calibration block and a pipeline smoke-test are run before
the bulk classification pass, to lock the decision rule and confirm the
conversion pipeline before scaling.

Field definitions for all four files are in
[`DATA_DICTIONARY.md`](DATA_DICTIONARY.md).
