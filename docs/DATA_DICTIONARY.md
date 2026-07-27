# Data Dictionary

Field definitions for the `jc-power-infrastructure` dataset. The dataset is
published as GeoJSON, generated from three source CSV files (intersections,
segments, underground features) by a Python conversion script.

Geometry is **symbolic, not surveyed**: line segments follow street centerlines
between intersections, and point coordinates are captured via Google Maps
right-click, so all coordinates are approximate. See
[`METHODOLOGY.md`](METHODOLOGY.md) for how the classification fields are
determined.

## Why pole attributes live on the segment

An earlier design modeled each utility pole as its own point feature. That was
dropped: individual poles cannot be reliably geolocated from available imagery —
matching a pole seen in Street View to a satellite pixel is unreliable, worsened
by tree canopy. Because the dataset's resolution claim is block-face level, not
survey level, precise pole coordinates were never part of what it promises.

Pole information is therefore **rolled up onto the segment**: counts of physical
structures (poles, transformers, streetlights) and properties of the conductors
(primary phase count and side, secondary presence, joint use) are recorded per
street segment rather than per pole. This matches what is actually observable,
removes the slowest and least reliable part of collection, and keeps every
classification field. What is lost is per-pole identity (e.g. *which* of a
block's poles carries the transformer) — deliberately, since that was not
recoverable anyway.

## Identifier conventions

**Intersections** (`intersection_id`):
- `<street1>_x_<street2>` for a crossing — e.g. `grove_x_newark`.
- `<street>_terminus_<direction>_of_<cross_street>` for a dead-end or street
  discontinuity — e.g. `sussex_terminus_east_of_warren`.
- Simpler `<street>_terminus_<direction>` where context is unambiguous, e.g.
  waterfront termini.

**Segments** (`segment_id`): `<traveled_street>__<from_cross>_to_<to_cross>`,
lowercase, where the two cross-streets are the bounding intersections' streets
and their order follows the segment's drawn direction (from→to). The ID encodes
the geometry: `grove__newark_to_1st` is Grove Street from Newark to 1st, drawn
in that direction. Termini reuse the intersection convention, e.g.
`grove__1st_to_terminus_north`.

## Line segments (`segments`)

One row per street segment — a single centerline between two intersections,
representing the whole street (both sides) for that block. Pole and conductor
information is rolled up onto this row.

| Field | Type | Values / format | Description |
|---|---|---|---|
| `segment_id` | string | e.g. `grove__newark_to_1st` | Unique segment identifier; encodes traveled street, bounding crosses, and draw direction (see *Identifier conventions*). |
| `from_intersection` | string | `intersection_id` | Start intersection (the "from" end that sets draw direction). |
| `to_intersection` | string | `intersection_id` | End intersection (the "to" end). |
| `overhead_underground` | categorical | `overhead` \| `underground` \| `mixed` \| `unknown` | Segment classification, keyed on the overhead primary/distribution conductor (see *Decision rule* in METHODOLOGY.md). `mixed` = genuinely split along the segment (explain in `notes`); `unknown` = imagery insufficient. |
| `primary_side` | categorical | `north` \| `south` \| `east` \| `west` \| `both` \| `none` | Which side of the street the overhead primary runs along, by the street's dominant compass bearing. `both` where primary runs both sides; `none` for underground segments or segments with no primary. Genuinely diagonal streets: name the side in `notes`. |
| `primary_conductors` | integer | `0`–`3` | Phase count of the primary line along the segment (a line property, not a per-pole sum). `1` = single-phase, `3` = three-phase, `0` = no primary. |
| `pole_count` | integer | ≥ 0 | Count of all physical poles on the segment, including comms-only poles. A count of structures. |
| `transformer_count` | integer | ≥ 0 | Count of transformers observed on the segment. |
| `secondary_present` | boolean | `true` \| `false` | Whether electrical secondary (low-voltage, below the clearance gap) is present anywhere on the segment. |
| `joint_use` | boolean | `true` \| `false` | Whether telecom (below the clearance gap) is present anywhere on the segment. |
| `streetlight_count` | integer | ≥ 0 | Count of streetlight fixtures on or near poles along the segment. |
| `imagery_date` | string | `YYYY-MM` | Capture date of the Street View imagery used, as displayed in Street View. Records evidence vintage. |
| `notes` | string | free text | Ambiguities the fields cannot capture: mid-block side switches, service/crossing poles, comms-only poles, diagonal-street side naming, hybrid configurations. |

### Reading the tally fields on underground segments

The overhead-tally fields — `primary_conductors`, `pole_count`,
`transformer_count`, `secondary_present`, `joint_use`, and `streetlight_count` —
record **visible overhead infrastructure**. On an `underground` segment they are
therefore `0`/`false`, because nothing overhead is present to count. This does
*not* mean the segment has no primary, transformers, or secondary — that
equipment exists below grade — only that it is not visible from the street and
is out of scope for a street-observation dataset.

As a result, `0`/`false` means something different depending on
`overhead_underground`: on an `overhead` segment it is an observation of absence
(looked, found none); on an `underground` segment it is structural (nothing
overhead to observe). **The tally fields must always be read conditional on
`overhead_underground`.** Aggregations (e.g. summing `transformer_count` across
the corridor) count *visible overhead* equipment only, not the total installed
grid.

## Underground feature points (`underground_features`)

Discrete, locatable surface evidence of underground infrastructure. Unlike
poles, these are individually findable in satellite view (pad-mounted
transformers, vault lids, etc.), so they remain point features.

| Field | Type | Values / format | Description |
|---|---|---|---|
| `feature_id` | string | — | Unique identifier. |
| `segment_id` | string | `segment_id` | Segment the feature is associated with. |
| `subtype` | categorical | `pad_transformer` \| `manhole` \| `handhole` \| `switchgear` \| `marker` | Type of visible surface evidence. If unsure, pick the closest and describe in `notes` — do not add new subtypes. |
| `imagery_date` | string | `YYYY-MM` | Capture date of imagery used. |
| `notes` | string | free text | — |

## Intersections (`intersections`)

Reference points that anchor segment endpoints. Primarily a collection aid.

| Field | Type | Values / format | Description |
|---|---|---|---|
| `intersection_id` | string | e.g. `grove_x_newark` | Unique identifier (see *Identifier conventions*). |
| `notes` | string | free text | — |
