# jc-power-infrastructure

An open, ground-truthed dataset classifying overhead vs. underground electrical
infrastructure in Jersey City, NJ — block by block, pole by pole.

## The question

Stand on the Jersey City waterfront and look across the Hudson. You can see two
electrical grids that made fundamentally different choices. Manhattan is served
by Con Edison's secondary network: a meshed, almost entirely underground system
where every customer has multiple electrical paths back to multiple feeders.
Jersey City, three thousand feet away, is served by PSE&G's predominantly
overhead, radial distribution: tree-topology feeders that travel from a
substation outward along utility poles, with every customer hanging off a single
branch.

These are not subtle engineering differences. They produce different reliability
outcomes during storms, different exposures to vegetation conflicts, different
maintenance regimes, and different long-run costs. Yet there is no public,
block-level dataset describing which streets in Jersey City are served overhead
and which are served underground. PSE&G does not publish it. This repository is
an attempt to build that dataset from the ground up, by direct observation.

## How this differs from existing data

A reasonable first question is whether this already exists. After searching, the
answer is that block-level, observation-based classification of distribution
infrastructure for Jersey City does not appear to be publicly available. The
datasets that do exist are either coarser or describe a different layer of the
grid:

- **Modeled estimates at ZIP/utility granularity.** The most comprehensive
  open effort is Stanford's *Grid Underground Distribution Statistics* (GUDS,
  Sun et al., 2024), which assembles each utility's total underground and
  overhead *mileage* from regulatory filings (SEC Form 10-K, USDA Form 7, state
  PUC submissions) and allocates those totals down to ZIP Code Tabulation Areas
  in proportion to population. The result is a useful national picture, but the
  underground "rate" for any given ZIP is an estimate derived from a
  utility-wide ratio — not an observation that a specific street is overhead or
  buried. It cannot distinguish one block from the next.
- **Transmission, not distribution.** Datasets derived from HIFLD (the
  Homeland Infrastructure Foundation-Level Data electric transmission layer,
  repackaged by various GIS platforms) map high-voltage bulk transmission lines
  between substations. That is a different layer of the grid from the
  distribution lines on the poles outside homes and businesses, which is what
  this dataset classifies.
- **OpenStreetMap.** OSM models distribution lines in its schema, but its own
  documentation notes that underground cables "should only be mapped if
  technical knowledge and sources are available" — because they are invisible to
  the aerial imagery most contributors work from. In practice, OSM's overhead
  distribution coverage in dense U.S. cities is patchy and its underground
  coverage is close to absent. A direct query of OSM for the Phase I corridor
  (June 2026) returned no distribution lines, poles, or overhead/underground
  classification, confirming the gap; the query and its date are documented in
  [`METHODOLOGY.md`](METHODOLOGY.md).

In short: where comparable data exists, it is either a population-weighted
estimate at ZIP resolution (GUDS) or a different grid layer entirely (HIFLD).
This dataset is a direct, street-level classification at block-face resolution,
which is new for this area.

## Dataset structure

The dataset is published as GeoJSON, generated from four source CSV files by a
Python conversion script. There are three feature types:

- **Line segments** — block-face centerlines, each classified overhead or
  underground.
- **Pole points** — individual utility poles, with associated equipment fields.
- **Underground feature points** — visible surface evidence of underground
  infrastructure (e.g. pad-mounted transformers, vault lids, risers).

Full field definitions, types, and allowed values are in
[`DATA_DICTIONARY.md`](DATA_DICTIONARY.md).

## Classification methodology

This dataset does not map underground cables — buried conductors are invisible
from imagery. Instead, each block face is classified by the presence or absence
of *overhead* distribution infrastructure, with undergrounding inferred as the
residual. Classification is performed primarily from Google Street View and
Google Earth imagery, with a field-verified validation sample.

The full method — what is observed vs. inferred, the decision rule, known
sources of classification error, and the validation procedure — is documented in
[`METHODOLOGY.md`](METHODOLOGY.md).

## Limitations

- **Single-observer classification.** Every segment in the current release was
  coded by one person. Inter-rater reliability has not been measured.
- **Imagery-based inference, not direct mapping.** Underground segments are
  inferred from the absence of visible overhead infrastructure, not observed
  directly. See [`METHODOLOGY.md`](METHODOLOGY.md) for the known error modes.
- **Snapshot in time.** Street View imagery varies in capture date, recorded
  per segment. Infrastructure changes are not reflected in real time.
- **Not utility-validated.** PSE&G has not reviewed or endorsed this data. It
  represents what is visible from the street, not what appears on utility
  as-built drawings.
- **Symbolic, not surveyed, geometry.** Line segments follow block-face
  centerlines rather than the actual physical path of conductors. Pole locations
  are approximate. The dataset is intended for analysis and planning, not for
  engineering or excavation.

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
variation. A customer on a buried main in a dense corridor and a customer at the
end of a long overhead lateral may share a SAIFI number that means almost
nothing about either of their actual experiences. Block-level infrastructure
data is a precondition for moving beyond utility averages.

**3. The role of overhead infrastructure in canopy and storm vulnerability.**
Overhead distribution lines drive vegetation management practices (tree
trimming, removals, canopy suppression) and concentrate storm-related outages in
places where above-ground exposure is highest. This was the original entry point
to the project and remains a live thread.

A working bibliography of source documents — NY PSC annual reliability reports,
Con Ed network operating documents, PSE&G regulatory filings, and academic work
on urban distribution reliability (including the GUDS dataset referenced above)
— is being assembled in `references.md`.

## Intended audience

This dataset is built with several use cases in mind:

- **Researchers and journalists** examining reliability, environmental justice,
  or infrastructure equity in northern New Jersey, who need block-level
  resolution that isn't available from the utility.
- **Local planners and advocates** working on tree canopy, climate adaptation,
  or undergrounding policy, who need to see where the overhead system is
  concentrated.
- **Tool-builders** — developers and civic technologists who want a starting
  dataset to build atop, whether for outage visualization, public engagement, or
  comparative analysis with Con Edison's service territory.
- **Other cities and neighborhoods** that might want to replicate the
  methodology in their own service areas. The classification scheme and Street
  View workflow are designed to be portable.

## Status and roadmap

This is an early-stage, single-observer dataset.

**Phase I** (current) covers the corridor bounded by Marin Boulevard (west),
Columbus Drive (north), the Hudson River (east), and the Hudson-Bergen Light
Rail tracks (south).

**Phase II** will extend the western boundary to Jersey Avenue.

Deferred to later phases (noted here so they are not pursued prematurely):
mirroring the dataset into OpenStreetMap, per-customer cost translation,
deeper PSE&G reliability decomposition, city-wide expansion, storm-event
reconstruction, and submission to Jersey City's open data portal.

## License

Code is released under the MIT License. Data is released under
Creative Commons Attribution 4.0 (CC-BY 4.0).
