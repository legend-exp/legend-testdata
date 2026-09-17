# _remage_ output files

- `tutorial/`: geometry, macro and output of the simulation used by the
  _reboost_ tutorial (see `tutorial/README.md`).
- `th228-full-optional-v0_13.lh5`: output of the
  `output/hdf5-ntuple-optionals.mac` _remage_ unit test.
- `l200cfg01-optmap-dummy.lh5`: dummy LEGEND-200 optical map.
- `V99999Z-3500V-hpge-drift-time-map.lh5`: drift time over the `(r, z)` plane
  of the test ICPC detector `V99999Z` (see `../metadata/legend-metadata`) at
  3500 V.
- `V99999Z-3500V-hpge-pulse-shape-lib.lh5`: charge pulses over the same
  grid, without electronics response, every 8 ns (625 samples, `float32`).

The last two hold the `<100>` and `<110>` crystal axes, on a 0.5 mm grid with
the p+ contact at `(0, 0)` and three rings of grid points outside the detector
(`padding: 3`), and are gzip-compressed inside the file.

## Reproducing the two maps

Needs a _legend-simflow_ checkout with its Julia environment
(`pixi run -e test init-julia-env`), this repository for the detector
metadata, and a settings file `ssd.yaml`:

```yaml
grid_size_in_mm: 0.5
ssd_refinement_limits: [0.2, 0.1, 0.05, 0.02]
padding: 3
```

Then, from the _legend-simflow_ directory, about 7 minutes each on one thread:

```console
$ julia --project=workflow/src/LegendSimflow.jl \
    workflow/src/legendsimflow/scripts/make_hpge_drift_time_maps.jl \
    --detector V99999Z --metadata <legend-testdata>/data/metadata/legend-metadata \
    --opv 3500 --ssd-settings ssd.yaml --output-file drift-time-map.lh5
$ julia --project=workflow/src/LegendSimflow.jl \
    workflow/src/legendsimflow/scripts/make_hpge_ideal_pulse_shape_lib.jl \
    --detector V99999Z --metadata <legend-testdata>/data/metadata/legend-metadata \
    --opv 3500 --ssd-settings ssd.yaml --output-file pulse-shape-lib.lh5
```

The library comes out sampled every 1 ns. It is compressed with GZip.
