# Mock _legend-metadata_

Small, public stand-in for the private
[legend-metadata](https://github.com/legend-exp/legend-metadata) repository,
with the same folder layout, holding the hardware and the datasets. Values are
invented but physically consistent.

It configures a small LEGEND-200-like germanium array, two strings of four
detectors, in which every detector is a copy of the test ICPC `V99999Z` (see
`../../legend/metadata`), the detector the drift time map and pulse shape
library in `../../remage` were computed for. _legend-simflow_ builds and
simulates it, adding its own `simprod` configuration to this folder at runtime.

- `hardware/configuration/channelmaps`: 8 germanium channels named `V00001A`,
  `V00001B` and so on, 58 SiPM channels and a pulser channel. String slots and
  channel identifiers come from a real LEGEND-200 channel map, the names do not.
- `hardware/detectors`: one germanium record per channel, all of them copies of
  `V99999Z` that differ only in the name, so they share its crystal record. Plus
  the fiber modules.
- `datasets`: run information, run lists and detector statuses for `p03`
  runs `r000` and `r001`.
