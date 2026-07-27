# jc-power-infrastructure

An open dataset of Jersey City's electrical infrastructure — overhead vs.
underground, classified block by block and verified via direct street-level observation.

## The question

Separated by the Hudson River, Jersey City, NJ and Manhattan are served by electrical grids that made fundamentally different choices nearly a century ago. Manhattan is served
by Con Edison's secondary network: a meshed, almost entirely underground system
where every customer has multiple electrical paths back to multiple feeders.
Jersey City sits across the Hudson in a different state, under a different regulator, served by a different utility — but with similar density, similar weather, and similar exposure to coastal storms. It is served by PSE&G's predominantly overhead, radial distribution: tree-topology feeders that travel from a substation outward along utility poles, with every customer hanging off a single branch.

These are not subtle engineering differences. They produce different reliability
outcomes during storms, different exposures to vegetation conflicts, different
maintenance regimes, and different long-run costs. They are also not, strictly
speaking, technical choices — they are the accumulated result of a century of
regulatory environments, rate cases, density assumptions, and path-dependent
capital investment.

The interesting question isn't *which is better* (the answer is well-known: networked
underground systems are dramatically more reliable, at much higher capital cost).
The interesting question is **what the actual infrastructure looks like, where, at
what density** — and what that implies for who experiences outages, who pays for
hardening, and where targeted undergrounding could deliver the best
reliability-per-dollar.

You cannot answer that question from public data. PSE&G does not publish
block-level infrastructure information. The New Jersey Board of Public
Utilities receives utility-aggregated reliability metrics, but not the spatial
granularity that would let a planner or researcher correlate outages to
infrastructure type at the neighborhood scale. The New York Public Service
Commission requires more detailed reporting from Con Edison, but that data
covers the other side of the river.

This repository is a small attempt to close that gap — starting in one
neighborhood, with the intent to expand.

## How this differs from existing data

A reasonable first question is whether this already exists. For this utility and
service territory, it does not. The datasets that come closest are either
coarser, cover a different region, or describe a different layer of the grid:

- **Modeled estimates at ZIP/utility granularity.** The most comprehensive open
  effort is Stanford's *Grid Underground Distribution Statistics* (GUDS, Sun et
  al., 2024), which assembles each utility's total underground and overhead
  *mileage* from regulatory filings and allocates those totals down to ZIP Code
  Tabulation Areas in proportion to population. The underground "rate" for any
  given ZIP is therefore an estimate derived from a utility-wide ratio — not an
  observation that a specific street is overhead or buried. It cannot
  distinguish one block from the next.
- **Machine-learning classification, in a different region.** The closest
  methodological neighbor is a Stanford framework (Wang et al., *Nature
  Communications*, 2023) that uses machine learning to classify overhead
  distribution from Google Street View imagery and predict underground extent
  from road-network and building data. It was developed and benchmarked in
  California against utility-owned grid maps. This dataset shares its data source
  (Street View) and target (overhead/underground classification) but covers a
  different region and utility — PSE&G's New Jersey territory — by direct human
  observation rather than model inference, in an area where no utility-owned
  benchmark map is publicly available. See [`references.md`](references.md) for
  detail.
- **Transmission, not distribution.** Datasets derived from HIFLD (the Homeland
  Infrastructure Foundation-Level Data electric transmission layer) map
  high-voltage bulk transmission lines between substations — a different layer
  of the grid from the distribution lines on the poles outside homes and
  businesses, which is what this dataset classifies.
- **OpenStreetMap.** OSM models distribution lines in its schema, but its own
  documentation notes that underground cables should only be mapped where
  technical knowledge and sources are available — because they are invisible to
  the aerial imagery most contributors work from. A direct query of OSM for the
  Phase I corridor (June 2026) returned no distribution lines, poles, or
  overhead/underground classification, confirming the gap for the area covered
  so far; the check is corridor-specific and is re-run as coverage expands. The
  query and its date are documented in [`METHODOLOGY.md`](METHODOLOGY.md).

In short: the existing data is either a modeled estimate at ZIP resolution
(GUDS), a machine-learning classification of a different region (Wang et al.,
California), or a different grid layer entirely (HIFLD). What this dataset
contributes is a direct, street-level classification of PSE&G's distribution
infrastructure in Jersey City — a specific utility and service territory, in a
dense Northeastern coastal-storm context, that the existing efforts do not
cover.

## What's in the dataset

The dataset is organized around two feature types. **Line segments** represent
street centerlines between intersections, each classified overhead, underground,
or mixed, and each carrying rolled-up counts of the poles, transformers, and
streetlights along it, along with the primary line's phase count and which side
of the street it runs on. **Underground feature points** mark the visible
above-ground manifestations of buried systems, such as vaults, pad-mount
transformers, and service heads.

Pole information is recorded per segment rather than as individual pole points:
poles cannot be reliably located from available imagery, and the dataset's
resolution is block-face level by design. The reasoning is documented in
[`DATA_DICTIONARY.md`](DATA_DICTIONARY.md).

Classification is performed by direct observation of Google Street View
imagery, with each block-face inspected and coded by hand. The initial
release covers a bounded area of downtown Jersey City, with later phases
extending coverage westward.

The full classification method — what is observed versus inferred, the
decision rule, known sources of error, and the validation procedure — is
documented in [`METHODOLOGY.md`](METHODOLOGY.md), and field definitions are in
[`DATA_DICTIONARY.md`](DATA_DICTIONARY.md).

## Background research

Three lines of work motivated the framing of this dataset:

**1. Network vs. radial architecture.** The Manhattan secondary network is one
of the most-studied examples of high-reliability urban distribution. Con
Edison's networked system was built out across the early 20th century and is
both meshed (multiple primary feeders supply each network transformer) and
redundant at the secondary level (customers draw from a grid rather than a
single line). Radial systems like PSE&G's, which dominate most of suburban and
urban America, are simpler and cheaper but vulnerable to single-point failures
and storm damage — a downed line interrupts everyone downstream of it.

**2. Reliability metrics and what they obscure.** Utility reliability is
typically reported as SAIFI (System Average Interruption Frequency Index — how
often the average customer loses power per year) and CAIDI (Customer Average
Interruption Duration Index — how long an outage lasts when it happens). These
metrics are useful at the utility-wide level but mask enormous within-utility
variation. A customer on a buried main in a dense corridor and a customer at
the end of a long overhead lateral may share a SAIFI number that means almost
nothing about either of their actual experiences. Block-level infrastructure
data is a precondition for moving beyond utility averages.

**3. The role of overhead infrastructure in canopy and storm vulnerability.**
Overhead distribution lines drive vegetation management practices (tree
trimming, removals, canopy suppression) and concentrate storm-related outages
in places where above-ground exposure is highest. This was the original entry
point to the project and remains a live thread.

A working bibliography of source documents — NY PSC annual reliability reports,
Con Ed network operating documents, PSE&G regulatory filings, and academic work
on urban distribution reliability — is being assembled and will accompany the
dataset.

## Intended audience

This dataset is built with several use cases in mind:

- **Researchers and journalists** examining reliability, environmental justice,
  or infrastructure equity in northern New Jersey, who need block-level
  resolution that isn't available from the utility.
- **Local planners and advocates** working on tree canopy, climate adaptation,
  or undergrounding policy, who need to see where the overhead system is
  concentrated.
- **Tool-builders** — developers and civic technologists who want a starting
  dataset to build atop, whether for outage visualization, public engagement,
  or comparative analysis with Con Edison's service territory.
- **Other cities and neighborhoods** that might want to replicate the
  methodology in their own service areas. The classification scheme and Street
  View workflow are designed to be portable.

## Status and roadmap

This is an early-stage, single-observer dataset. It is not a substitute for
authoritative utility records, and it should not be treated as one.

- **Phase I (in progress):** Complete classification of the downtown bounding
  box described above. Publish initial GeoJSON release and Folium-based
  interactive visualization.
- **Phase II (planned):** Extend the western boundary to Jersey Avenue,
  adding coverage of additional downtown blocks.
- **Future:** Replication methodology documentation, expansion to additional
  Jersey City neighborhoods, integration with publicly available outage
  snapshots, and — eventually — comparison layers against Con Edison's
  publicly reported reliability data for adjacent Manhattan service areas.

The project is being developed under a fixed time budget. Scope expansion is
deliberate rather than opportunistic.

## Using the data

The dataset is published in GeoJSON, which can be loaded directly into any
standard GIS tool — QGIS, ArcGIS, GeoPandas, Folium, Leaflet, or Mapbox.

If you use this data in research or reporting, citation is requested but not
required (see License below). I'd also be interested to hear how you used it.

## Limitations

- **Single-observer classification.** Every segment in the current release was
  coded by one person. Inter-rater reliability has not been measured.
- **Imagery-based inference, not direct mapping.** Underground segments are
  inferred from the absence of visible overhead infrastructure, not observed
  directly. See [`METHODOLOGY.md`](METHODOLOGY.md) for the known error modes
  (rear-lot feeds, hybrid blocks, stale imagery).
- **Snapshot in time.** Google Street View imagery for the Phase I area varies
  in capture date. Infrastructure changes — new construction, undergrounding
  projects, pole replacements — are not reflected in real time.
- **Not utility-validated.** PSE&G has not reviewed or endorsed this data. It
  represents what is visible from the street, not what appears on utility
  as-built drawings.
- **Symbolic, not surveyed, geometry.** Line segments follow street centerlines
  rather than the actual physical path of conductors, and underground-feature
  points are approximate. The dataset is intended for analysis and planning, not
  for engineering or excavation.

## License

- **Code** in this repository is released under the MIT License.
- **Data** in this repository is released under the
  [Creative Commons Attribution 4.0 International License (CC-BY 4.0)](https://creativecommons.org/licenses/by/4.0/).

Attribution suggestion:
> Jersey City Power Infrastructure Dataset, [author], [year]. Available at
> [repository URL]. Licensed CC-BY 4.0.

## Contact and contributions

Issues and pull requests welcome. For larger questions, methodological
suggestions, or collaboration inquiries, open an issue on this repository.
