# Mock _legend-metadata_

Small, public stand-in for the private
[legend-metadata](https://github.com/legend-exp/legend-metadata) repository,
with the same folder layout. Values are invented but physically consistent.

It configures a small LEGEND-200-like germanium array, two strings of four
detectors, in which every detector is a copy of the test ICPC `V99999Z` (see
`../../legend/metadata`), the detector the drift time map and pulse shape
library in `../../remage` were computed for. Point `LEGEND_METADATA` here to
build it:

```console
$ LEGEND_METADATA=$PWD legend-pygeom-l200 \
    --config simprod/config/geom/l200cfg01-geom-config.yaml l200.gdml
```

- `hardware/configuration/channelmaps`: 8 germanium channels named `V00001A`,
  `V00001B` and so on, 58 SiPM channels and a pulser channel. String slots and
  channel identifiers come from a real LEGEND-200 channel map, the names do not.
- `simprod/config`: the _legend-simflow_ production configuration of the
  `l200cfg01` experiment. `geom/l200cfg01-special-geom-metadata.yaml` holds the
  string and calibration-tube geometry: `V99999Z` is wider and taller than any
  detector operated in LEGEND-200, so the strings are widened around it.
- `hardware/detectors`: one germanium record per channel, all of them copies of
  `V99999Z` that differ only in the name, so they share its crystal record. Plus
  the fiber modules.
- `datasets`: run information, run lists and detector statuses for `p03`
  runs `r000` and `r001`.
