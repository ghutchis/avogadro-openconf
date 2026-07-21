# avogadro-openconf

An Avogadro 2 plugin that generates conformer ensembles using
[OpenConf](https://github.com/rowansci/openconf).

It adds the following items under **Extensions → OpenConf**, each running a
tuned OpenConf preset on the current molecule and returning the conformers as
an energy-ranked ensemble:

- **Rapid** — fast, diverse set for virtual screening
- **Ensemble** — balanced ensemble for property prediction
- **Spectroscopic** — exhaustive Boltzmann ensemble for NMR/IR/VCD
- **Docking** — maximize bioactive-pose recall
- **Macrocycle** — macrocyclic ring systems (ring size ≥ 10)

Each conformer is tagged with a relative ``<energy>`` (kJ/mol) so Avogadro can
plot the conformer energies.

An **Inorganic** item (OpenConf's ``transition_metal`` preset) is planned once
that preset appears in an OpenConf PyPI release — it currently exists only on
the project's unreleased git ``main`` branch.

## Suggestions

Please submit suggestions, bugs, etc. on GitHub: https://github.com/ghutchis/avogadro-openconf/issues
