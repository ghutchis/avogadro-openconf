#  This source file is part of the Avogadro project
#  This source code is released under the 3-Clause BSD License, (see "LICENSE").
#  https://github.com/ghutchis/avogadro-openconf/

"""Conformer ensemble generation using OpenConf presets."""

from io import StringIO

from openconf import generate_conformers
from rdkit import Chem

# OpenConf force field energies are in kcal/mol; Avogadro works in kJ/mol.
KCAL_TO_KJ = 4.184

# Map each menu identifier to an OpenConf preset name.
PRESETS = {
    "rapid": "rapid",
    "ensemble": "ensemble",
    "spectroscopic": "spectroscopic",
    "docking": "docking",
    "macrocycle": "macrocycle",
    "inorganic": "transition_metal",
}


def generate(avo_input: dict, feature: str) -> dict:
    """Generate a conformer ensemble for the current molecule.

    Returns every conformer (lowest energy first) as a multi-conformer SDF,
    each block tagged with an ``<energy>`` data field so Avogadro can plot the
    relative conformer energies.
    """
    preset = PRESETS.get(feature)
    if preset is None:
        return {"error": f"Unknown conformer preset: {feature}"}

    mol = Chem.MolFromMolBlock(avo_input.get("sdf", ""))
    if mol is None:
        return {"error": "Could not interpret the molecule."}

    # Preserve the stereochemistry implied by the input 3D geometry so the
    # generated conformers keep the same configuration.
    Chem.AssignStereochemistryFrom3D(mol)

    try:
        ensemble = generate_conformers(mol, preset=preset)
    except Exception as exc:  # OpenConf raises for unsupported inputs
        return {"error": f"Conformer generation failed:\n{exc}"}

    if ensemble.n_conformers == 0:
        return {"error": "No conformers were generated."}

    m = ensemble.mol
    conf_ids = ensemble.conf_ids
    energies = ensemble.energies

    # Order conformers lowest energy first (unknown energies sort last).
    order = sorted(range(ensemble.n_conformers), key=lambda i: energies[i])

    sio = StringIO()
    writer = Chem.SDWriter(sio)
    for i in order:
        energy = energies[i]
        if energy != float("inf"):
            m.SetDoubleProp("energy", energy * KCAL_TO_KJ)
        elif m.HasProp("energy"):
            m.ClearProp("energy")
        writer.write(m, confId=conf_ids[i])
    writer.close()

    return {"moleculeFormat": "sdf", "sdf": sio.getvalue()}
