# _remage_ tutorial simulation

Input for the _reboost_ tutorial: a BEGe and the ICPC `V99999Z` in liquid
argon, with a Th-228 source between them.

- `make_geometry.py` → `geometry.gdml`
- `th228.mac`: 500 000 Th-228 decays, events with ≥ 1 MeV in germanium
- `th228-stp.lh5`: _remage_ output

Reproduce with `pixi run simulate` (random seed not fixed).
