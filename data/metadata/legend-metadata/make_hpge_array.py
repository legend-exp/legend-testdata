"""Write the channel map, the detector records and the geometry of the mock HPGe array.

Every germanium channel is an identical copy of the test detector `V99999Z`, named after the string
slot it sits in. The array is LEGEND-200-like: string positions, SiPM channels and hardware
dimensions come from _legend-pygeom-l200_, which is where a real geometry reads them from.

The array is small on purpose, two strings of four detectors: it exists to be simulated in tests,
not to reproduce LEGEND-200.

`V99999Z` is 88.8 mm wide and 90 mm tall, more than any detector operated in LEGEND-200, so it
needs room: every string gets the widest nylon mini-shroud and support-rod radius in use (54.0 mm
and 49.5 mm, the values of string 5) and the largest PEN plate, which needs the rods that far out.
The two strings are 129.8 mm apart, enough for two 108 mm wide mini-shrouds. Every detector unit is
103.5 mm long, more than the detector is tall.

Run from this directory.
"""

from __future__ import annotations

import json
import shutil
from collections import Counter
from importlib import resources
from pathlib import Path

from dbetto import utils

here = Path(__file__).parent
hardware = here / "hardware"
pygeoml200 = resources.files("pygeoml200") / "configs"

# the channel map: real string slots, invented detector names, two slices per crystal
layout = json.loads((pygeoml200 / "dummy_geom/channelmap.json").read_text())
slots = sorted(
    (ch for ch in layout.values() if ch["system"] == "geds"),
    key=lambda ch: (ch["location"]["string"], ch["location"]["position"]),
)
slots = [
    ch
    for ch in slots
    if ch["location"]["string"] in (4, 5) and ch["location"]["position"] <= 4
]

chmap_file = hardware / "configuration/channelmaps/l200-p03-r%-T%-all-config.yaml"
chmap = {"PULS01": utils.load_dict(chmap_file)["PULS01"]}
for i, ch in enumerate(slots):
    name = f"V{i // 2 + 1:05d}{'AB'[i % 2]}"
    chmap[name] = {
        "name": name,
        "system": "geds",
        "location": ch["location"],
        "daq": {"rawid": 1104000 + i},
    }
for i, ch in enumerate(ch for ch in layout.values() if ch["system"] == "spms"):
    chmap[ch["name"]] = dict(ch, daq={"rawid": 1052800 + i})

utils.write_dict(chmap, chmap_file)

# one germanium record per channel. They keep the production fields of `V99999Z`, so all of them
# point at its crystal record, and only the name says which slot the detector sits in.
diode = utils.load_dict(hardware / "detectors/germanium/diodes/V99999Z.yaml")
diodes = hardware / "detectors/germanium/diodes"
for path in diodes.glob("V0*.yaml"):
    path.unlink()

for name in (ch for ch, meta in chmap.items() if meta["system"] == "geds"):
    utils.write_dict(dict(diode, name=name), diodes / f"{name}.yaml")

# one record per fiber module, shared by the two SiPM channels reading it out
fibers = hardware / "detectors/lar/fibers"
shutil.rmtree(fibers, ignore_errors=True)
fibers.mkdir(parents=True)
for module in {
    ch["location"]["fiber"] for ch in chmap.values() if ch["system"] == "spms"
}:
    utils.write_dict(
        {
            "name": module,
            "type": "inner" if module.startswith("IB") else "outer",
            "geometry": {"tpb": {"thickness_in_nm": 1000}},
        },
        fibers / f"{module}.yaml",
    )

# the string and calibration-tube geometry, widened around the detector. The nylon mini-shroud is
# also shortened to the length of the four detector units it has to cover: the default 1000 mm one
# would stick out above the copper top plate.
rod_length = 103.5
per_string = Counter(
    ch["location"]["string"] for ch in chmap.values() if ch["system"] == "geds"
)

special = utils.load_dict(pygeoml200 / "extra_meta/l200-p03-r%-T%-all-config.yaml")
for number, string in special["hpge_string"].items():
    if string["minishroud_radius_in_mm"] is not None:
        string["minishroud_radius_in_mm"] = 54.0
        string["rod_radius_in_mm"] = 49.5
        length = per_string.get(number, 0) * rod_length * 0.997 + 10
        string["minishroud_delta_length_in_mm"] = round(length - 1000)

special["hpges"] = {
    name: {"rodlength_in_mm": rod_length, "baseplate": "xlarge"}
    for name, meta in chmap.items()
    if meta["system"] == "geds"
}

utils.write_dict(special, here / "simprod/config/geom/special_metadata.yaml")

print(f"{len(special['hpges'])} detectors")
