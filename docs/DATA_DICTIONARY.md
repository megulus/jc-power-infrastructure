# Data Dictionary

Field definitions for the `jc-power-infrastructure` dataset. The dataset is
published as GeoJSON, generated from four source CSV files (intersections,
segments, poles, underground features) by a Python conversion script.

Geometry is **symbolic, not surveyed**: line segments follow block-face
centerlines and point coordinates are captured via Google Maps right-click, so
all coordinates are approximate. See [`METHODOLOGY.md`](METHODOLOGY.md) for how
the classification fields are determined.

## Segment identifiers

Segment and endpoint IDs follow a fixed naming convention:

- `_x_` denotes a street crossing — e.g. `grove_x_newark` is the intersection of
  Grove Street and Newark Avenue.
- `_terminus_<direction>_of_<cross_street>` denotes a dead-end or street
  discontinuity — e.g. `sussex_terminus_east_of_warren`.
- A simpler `_terminus_<direction>` is acceptable where context is unambiguous,
  e.g. waterfront termini.

## Line segments (`segments`)

Block-face centerlines, each classified overhead or underground.

| Field | Type | Values / format | Description |
|---|---|---|---|
| `segment_id` | string | e.g. `grove_x_newark__to__grove_x_bay` | Unique segment identifier (see *Segment identifiers* above). |
| `overhead_underground` | categorical | `overhead` \| `underground` \| `unknown` | Classification of the block face, keyed on the overhead primary/distribution conductor (see *Decision rule* in METHODOLOGY.md). `unknown` where imagery is insufficient. |
| `pole_present` | boolean | `true` \| `false` | Whether one or more utility poles are present along the segment. |
| `transformer_present` | boolean | `true` \| `false` | Whether a pole-mounted or pad-mounted transformer is visible. |
| `tree_clearance_status` | categorical | `low` \| `medium` \| `high` | Degree of conflict between overhead conductors and tree canopy. `low` = little to no canopy contact or pressure; `high` = significant canopy intrusion or heavy trimming evident. Recorded only where overhead infrastructure is present. |
| `segment_length` | number | meters | Approximate length of the block-face centerline. |
| `imagery_date` | string | `YYYY-MM` | Capture date of the Google Street View imagery used to classify the segment, as displayed in Street View. Records evidence vintage for auditability. |
| `notes` | string | free text | Ambiguities, hybrid configurations, or anything the categorical fields cannot capture. |

## Pole points (`poles`)

Individual utility poles with associated equipment fields.

| Field | Type | Values / format | Description |
|---|---|---|---|
| `pole_id` | string | — | Unique pole identifier. |
| `segment_id` | string | — | Segment the pole is associated with. |
| `transformer` | boolean | `true` \| `false` | Pole-mounted transformer present. |
| `imagery_date` | string | `YYYY-MM` | Capture date of imagery used. |
| `notes` | string | free text | Other equipment or observations. |

> **Note:** the pole feature type has roughly eight equipment fields in total.
> The remaining ones (e.g. riser, streetlight, multiple attachments) are
> currently documented inline in the source CSV header and will be formalized in
> this table as the schema stabilizes.

## Underground feature points (`underground_features`)

Visible surface evidence of underground infrastructure.

| Field | Type | Values / format | Description |
|---|---|---|---|
| `feature_id` | string | — | Unique identifier. |
| `segment_id` | string | — | Associated segment. |
| `feature_type` | categorical | e.g. `pad_transformer` \| `vault_lid` \| `riser` | Type of visible surface evidence of underground infrastructure. |
| `imagery_date` | string | `YYYY-MM` | Capture date of imagery used. |
| `notes` | string | free text | — |

## Intersections (`intersections`)

Reference points used during collection to anchor segment endpoints.

| Field | Type | Values / format | Description |
|---|---|---|---|
| `intersection_id` | string | e.g. `grove_x_newark` | Unique identifier (see *Segment identifiers*). |
| `notes` | string | free text | — |

> The intersections file is primarily a collection aid; its fields will be
> formalized here against the actual CSV header.
