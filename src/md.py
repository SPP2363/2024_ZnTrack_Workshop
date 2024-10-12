import pathlib

import ase.io
import pandas as pd
import zntrack
from ase import units
from ase.md.langevin import Langevin
from tqdm import tqdm

from .models import MACE_MP_0


class MolecularDynamics(zntrack.Node):
    data: list[ase.Atoms] = zntrack.deps()
    model: MACE_MP_0 = zntrack.deps()

    data_id: int = zntrack.params(-1)
    temperature: float = zntrack.params(300)
    thermo_interval: int = zntrack.params(50)
    steps: int = zntrack.params(1000)

    trajectory: pathlib.Path = zntrack.outs_path(zntrack.nwd / "trajectory.traj")
    thermo: pd.DataFrame = zntrack.plots(
        x="step", y=["temp", "epot", "ekin", "etot"], autosave=True
    )

    def run(self):
        atoms = self.data[self.data_id]
        step = 0
        atoms.calc = self.model.get_model()

        self.thermo = pd.DataFrame(
            {"step": [], "epot": [], "ekin": [], "etot": [], "temp": []}
        )

        dyn = Langevin(
            atoms,
            0.5 * units.fs,
            self.temperature * units.kB,
            0.002,
            trajectory=self.trajectory.as_posix(),
        )

        def printenergy():
            """Function to print the potential, kinetic and total energy."""
            nonlocal step
            nonlocal atoms

            epot = atoms.get_potential_energy() / len(atoms)
            ekin = atoms.get_kinetic_energy() / len(atoms)
            self.thermo = pd.concat(
                [
                    self.thermo,
                    pd.DataFrame(
                        {
                            "step": [step],
                            "epot": [epot],
                            "ekin": [ekin],
                            "etot": [epot + ekin],
                            "temp": [ekin / (1.5 * units.kB)],
                        }
                    ),
                ]
            )

        dyn.attach(printenergy, interval=self.thermo_interval)

        for _ in tqdm(dyn.irun(self.steps), total=self.steps):
            step += 1

    @property
    def frames(self):
        with self.state.fs.open(self.trajectory, "rb") as f:
            return list(ase.io.iread(f, index=":", format="traj"))
