import zntrack

from src import MACE_MP_0, MolecularDynamics, Smiles2Conformers, StructureOptimization

project = zntrack.Project()
model = MACE_MP_0()

with project:
    data = Smiles2Conformers(smiles="N1=PN=PN=P1", num_confs=10)
    geom_opt = StructureOptimization(data=data.frames, model=model)
    md = MolecularDynamics(
        data=geom_opt.frames, model=model, thermo_interval=10, always_changed=True
    )

project.repro()
