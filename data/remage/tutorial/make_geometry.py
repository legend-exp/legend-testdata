import pygeomhpges as hpges
import pyg4ometry as pg4
from numpy import pi
import pygeomtools


reg = pg4.geant4.Registry()

bege_meta = {
    "name": "B00000B",
    "type": "bege",
    "production": {
        "enrichment": {"val": 0.874, "unc": 0.003},
        "mass_in_g": 697.0,
    },
    "geometry": {
        "height_in_mm": 29.46,
        "radius_in_mm": 36.98,
        "groove": {"depth_in_mm": 2.0, "radius_in_mm": {"outer": 10.5, "inner": 7.5}},
        "pp_contact": {"radius_in_mm": 7.5, "depth_in_mm": 0},
        "taper": {
            "top": {"angle_in_deg": 0.0, "height_in_mm": 0.0},
            "bottom": {"angle_in_deg": 0.0, "height_in_mm": 0.0},
        },
    },
}

# test detector V99999Z, copied from
# ../../legend/metadata/hardware/detectors/germanium/diodes/V99999Z.yaml
icpc_meta = {
    "name": "V99999Z",
    "type": "icpc",
    "production": {
        "enrichment": {"val": 0.9, "unc": 0.01},
        "mass_in_g": 3045,
    },
    "geometry": {
        "height_in_mm": 90,
        "radius_in_mm": 44.4,
        "borehole": {"radius_in_mm": 4, "depth_in_mm": 53},
        "groove": {"depth_in_mm": 2, "radius_in_mm": {"outer": 15, "inner": 12}},
        "pp_contact": {"radius_in_mm": 12, "depth_in_mm": 0},
        "taper": {
            "top": {"angle_in_deg": 45, "height_in_mm": 3},
            "bottom": {"angle_in_deg": 45, "height_in_mm": 3},
            "borehole": {"angle_in_deg": 5, "height_in_mm": 45},
        },
    },
}
# create logical volumes for the two HPGe detectors
bege_l = hpges.make_hpge(bege_meta, name="BEGe_L", registry=reg)
icpc_l = hpges.make_hpge(icpc_meta, name="ICPC_L", registry=reg)

# create a world volume
world_s = pg4.geant4.solid.Orb("World_s", 20, registry=reg, lunit="cm")
world_l = pg4.geant4.LogicalVolume(world_s, "G4_Galactic", "World", registry=reg)
reg.setWorld(world_l)

# let's make a liquid argon balloon
lar_s = pg4.geant4.solid.Orb("LAr_s", 15, registry=reg, lunit="cm")
lar_l = pg4.geant4.LogicalVolume(lar_s, "G4_lAr", "LAr_l", registry=reg)
pg4.geant4.PhysicalVolume([0, 0, 0], [0, 0, 0], lar_l, "LAr", world_l, registry=reg)

# now place the two HPGe detectors in the argon
bege_pv = pg4.geant4.PhysicalVolume(
    [0, 0, 0], [5, 0, -3, "cm"], bege_l, "BEGe", lar_l, registry=reg
)
icpc_pv = pg4.geant4.PhysicalVolume(
    [0, 0, 0], [-5, 0, -3, "cm"], icpc_l, "ICPC", lar_l, registry=reg
)

# register them as detectors in remage
# this also saves the metadata into the files for later use
bege_pv.set_pygeom_active_detector(
    pygeomtools.RemageDetectorInfo("germanium", 1, bege_meta)
)
icpc_pv.set_pygeom_active_detector(
    pygeomtools.RemageDetectorInfo("germanium", 2, icpc_meta)
)

# finally create a small radioactive source
source_s = pg4.geant4.solid.Tubs("Source_s", 0, 1, 1, 0, 2 * pi, registry=reg)
source_l = pg4.geant4.LogicalVolume(source_s, "G4_BRAIN_ICRP", "Source_L", registry=reg)
pg4.geant4.PhysicalVolume(
    [0, 0, 0], [0, 5, 0, "cm"], source_l, "Source", lar_l, registry=reg
)

pygeomtools.write_pygeom(reg, "geometry.gdml")
