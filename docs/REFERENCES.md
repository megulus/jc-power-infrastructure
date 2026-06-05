# References

A working bibliography for the `jc-power-infrastructure` project: prior datasets
and academic work on distribution-grid mapping, plus the reliability and
architecture sources that motivate the dataset's framing. Entries marked
*Relation to this project* note how the work compares to this dataset.

## Prior datasets and grid-mapping work

**Wang, Z., et al. (2023). "Geospatial mapping of distribution grid with machine
learning and publicly-accessible multi-modal data."** *Nature Communications*,
17 August 2023 (open access). https://www.nature.com/articles/s41467-023-39647-3
The closest methodological neighbor to this project. A Stanford framework
(Rajagopal lab) uses machine learning to identify overhead distribution lines
from Google Street View imagery, then predicts the underground grid on top of
the predicted overhead map by incorporating road-network and building-location
data. Developed and benchmarked in California against utility-owned distribution
grid maps, and shown to transfer to three Sub-Saharan African cities without
retraining.
*Relation to this project:* Same data source (Street View) and same target
(overhead/underground distribution classification), but a different method,
geography, and verification basis. Their classification is model-inferred and
gap-filled at scale; the underground class in particular is a prediction layered
on a prediction, benchmarked where utility maps exist. This dataset is
hand-classified by direct observation, with a field-verified validation sample,
in PSE&G's New Jersey territory — a service area their work does not cover, and
one where no utility-owned benchmark map is publicly available.

**Wang, Z., Wara, M., Majumdar, A. & Rajagopal, R. (2023). "Local and
utility-wide cost allocations for a more equitable wildfire-resilient
distribution grid."** *Nature Energy* 8(10), 1097–1108.
https://doi.org/10.1038/s41560-023-01306-8
An applied follow-on from the same lab that uses the Street-View grid-mapping
method above to study the equity of undergrounding costs in California: it finds
lower-income communities have fewer lines undergrounded and more
wildfire-vulnerable overhead lines and poles, and proposes an income-thresholded
cost-allocation scheme.
*Relation to this project:* Demonstrates a policy use case for block-level
overhead/underground data — cost and equity analysis of undergrounding — of the
kind this dataset is meant to enable for Jersey City, though in a wildfire rather
than coastal-storm context.

**Sun, T., Zanocco, C., Flora, J., & Rajagopal, R. (2024). "Mapping the Depths:
A Stocktake of Underground Power Distribution in the United States."** arXiv
preprint 2402.06668; also published via IEEE.
https://arxiv.org/abs/2402.06668
Introduces Grid Underground Distribution Statistics (GUDS), described as the
first nationwide assessment of underground distribution at high spatial
granularity, reported at the Zip Code Tabulation Area (ZCTA) and state levels.
The study examines relationships between underground rates and household income,
urbanization, and natural-hazard vulnerability. Underground-distribution data is
published via Stanford's Data Commons for Sustainability.
*Relation to this project:* A useful national picture, but at ZCTA resolution —
far coarser than block-face. The underground rate for a given ZIP is a
modeled/aggregated figure, not an observation that a specific street is overhead
or buried, and so cannot distinguish one block from the next. (Note: confirm the
exact ZCTA allocation method against the paper's methodology section before
citing the mechanism in detail.)

**Homeland Infrastructure Foundation-Level Data (HIFLD) — Electric Power
Transmission Lines.**
A federal open-data layer of high-voltage bulk transmission lines between
substations, repackaged by various GIS platforms.
*Relation to this project:* A different layer of the grid. HIFLD maps
transmission, not the distribution lines on the poles outside homes and
businesses that this dataset classifies. Not comparable coverage.

**OpenStreetMap — `power=*` features.** Queried via the Overpass API.
https://www.openstreetmap.org
OSM models distribution lines in its schema but, per its own documentation,
underground cables should only be mapped where technical knowledge and sources
are available, since they are invisible to the aerial imagery most contributors
use.
*Relation to this project:* A direct Overpass query of the Phase I corridor
(June 2026) returned no distribution lines, poles, or overhead/underground
classification — confirming the gap for the area covered so far. See
[`METHODOLOGY.md`](METHODOLOGY.md) for the query, date, and re-run procedure.

## Reliability and grid architecture

**City of New York, Office of Long-Term Planning and Sustainability (2013).
"Utilization of Underground and Overhead Power Lines in the City of New York."**
December 2013. Prepared pursuant to Local Law 13.
https://www.nyc.gov/html/planyc2030/downloads/pdf/power_lines_study_2013.pdf
A study commissioned after Hurricane Sandy to evaluate the feasibility of
converting New York City's overhead distribution to underground. Drawing on Con
Edison data and an engineering feasibility report by CHA Consulting, it finds
that 86% of the city's electric load is already served by underground networks
(Manhattan being entirely underground), that underground systems experience
fewer interruptions but longer restoration times when faults occur, and that
wholesale undergrounding would be cost-prohibitive — on the order of $18.5
billion for the City alone — with no U.S. state utility commission having
recommended wholesale conversion. Its recommended approach is *selective*,
targeted undergrounding of the highest-benefit segments combined with overhead
hardening and circuit sectionalizing.
*Relation to this project:* Foundational to this project's framing. This study
reframed the initial question away from a simple overhead-vs-underground
reliability comparison — which it shows is already a settled tradeoff (each has
characteristic strengths; cost is the binding constraint) — toward the question
this dataset addresses: *where* the overhead segments are, at a granularity that
would let a planner target undergrounding cost-effectively. The study performs
this analysis for New York's Con Edison territory; no equivalent block-level
inventory exists for PSE&G's New Jersey territory across the Hudson.

**Regional Plan Association (Mason, K. & Freudenberg, R.) (2025). "The State of
the Grid in New Jersey."** RPA Lab, 22 December 2025.
https://rpa.org/news/lab/the-state-of-the-grid-in-new-jersey
Background overview of New Jersey's electrical grid: governance (PJM, BPU), the
four major distribution utilities, generation mix, and statewide reliability.
Reports that New Jersey has among the highest reliability indices in the country
(2023 statewide SAIDI 108.3 min, SAIFI 0.881, CAIDI 123 min), with PSE&G the
most reliable utility in the state (SAIFI 0.53, CAIDI 62 min), and notes a
north-south reliability gradient tied to historical development density. Gives
system-scale figures including roughly 57,000 miles of distribution line
statewide and 14,200 miles of power lines in PSE&G's system.
*Relation to this project:* Background reading on New Jersey grid reliability and
scale. Provides the utility-aggregated reliability metrics that this dataset is
intended to complement with sub-utility, block-level infrastructure detail —
the granularity that statewide and utility-level figures cannot resolve.

## Reliability sources (to be expanded)

*(Specific report years and citations to be filled in as the bibliography is
built out.)*

**New York Public Service Commission — annual electric reliability reports.**
Source for Con Edison SAIFI/CAIDI reliability metrics and network-system
performance. (Note: the NYC 2013 study above draws on the NYS DPS 2012 Electric
Reliability Performance Report; that report is a concrete starting citation.)
*To add:* specific report year(s) and URLs used.

**New Jersey Board of Public Utilities — reliability reporting.**
Source for PSE&G service-territory reliability metrics (utility-aggregated).
*To add:* specific filings/years and URLs used.

**Con Edison secondary-network documentation.**
Background on meshed, redundant underground network distribution architecture.
*To add:* specific operating documents or engineering references.

**PSE&G regulatory filings.**
Background on radial distribution architecture and undergrounding activity in
the service territory.
*To add:* specific docket numbers or filings.

## Notes

- This file is a living document; reliability-section entries are placeholders
  to be filled with exact citations as sources are consulted.
- Citations should be verified at the source before being relied on in the
  README or any external-facing writeup.
