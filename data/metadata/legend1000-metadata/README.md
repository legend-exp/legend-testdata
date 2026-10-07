# Mock _legend1000-metadata_

Small stand-in for the
[legend1000-metadata](https://github.com/legend-exp/legend1000-metadata)
repository, with the same folder layout, holding the hardware and the datasets.
Values are invented but physically consistent.

Like the real repository, it holds one default record per channel kind:
`V99999Z` (germanium), `S9999Z` (SiPM) and `PMT9999` (PMT). _pylegendmeta_
copies and adjusts them for any channel name that has no record of its own.

Only the default records are on disk: the channel names come from
_legend-pygeom-l1000_, and _pylegendmeta_ derives their records, statuses and 
operational voltages from the default records. _legend-simflow_ writes the 
germanium records the pulse-shape simulation needs, builds and simulates the 
array, adding its own `simprod` configuration to this folder at runtime. 
The default germanium record is the test ICPC `V99999Z` (see 
`../../legend/metadata`).

- `hardware/configuration/channelmaps`: the three default records only. The
  channels of the array, and their identifiers, are derived from them.
- `hardware/configuration/opvs`: operational voltage of the default germanium
  detector.
- `hardware/detectors`: the default germanium record and its crystal (links to
  `../../legend/metadata`).
- `datasets`: run information, run lists and the statuses of the three default
  records for `p01` run `r000`.
