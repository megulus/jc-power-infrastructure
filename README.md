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

## What's in the dataset

The dataset is organized around three feature types: line segments
representing block-face centerlines classified as overhead, underground, or
mixed; pole points capturing utility poles and the equipment attached to them
(transformers, primary and secondary conductors, communications,
streetlights); and underground feature points marking the visible
above-ground manifestations of buried systems, such as vaults, pad-mount
transformers, and service heads.

Classification is performed by direct observation of Google Street View
imagery, with each block-face inspected and coded by hand. The initial
release covers a bounded area of downtown Jersey City, with later phases
extending coverage westward.

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
- **Snapshot in time.** Google Street View imagery for the Phase I area varies
  in capture date. Infrastructure changes — new construction, undergrounding
  projects, pole replacements — are not reflected in real time.
- **Not utility-validated.** PSE&G has not reviewed or endorsed this data. It
  represents what is visible from the street, not what appears on utility
  as-built drawings.
- **Symbolic, not surveyed, geometry.** Line segments follow block-face
  centerlines rather than the actual physical path of conductors. Pole
  locations are approximate. The dataset is intended for analysis and planning,
  not for engineering or excavation.

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
