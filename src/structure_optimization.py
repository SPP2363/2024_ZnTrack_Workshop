import pathlib
from enum import StrEnum

import ase.io
import ase.optimize
import zntrack

from .models import MACE_MP_0


class Optimizer(StrEnum):
    BFGS = "BFGS"
    LBFGS = "LBFGS"
    FIRE = "FIRE"


class StructureOptimization(zntrack.Node):
    data: list[ase.Atoms] = zntrack.deps()
    model: MACE_MP_0 = zntrack.deps()

    data_id: int = zntrack.params(-1)
    fmax: float = zntrack.params(0.05)
    trajectory: pathlib.Path = zntrack.outs_path(zntrack.nwd / "trajectory.traj")

    optimizer: Optimizer = zntrack.params(str(Optimizer.BFGS))

    def run(self):
        atoms = self.data[self.data_id]
        atoms.calc = self.model.get_model()
        optim = getattr(ase.optimize, self.optimizer)
        dyn = optim(atoms, trajectory=self.trajectory.as_posix())
        dyn.run(fmax=self.fmax)

    @property
    def frames(self):
        with self.state.fs.open(self.trajectory, "rb") as f:
            return list(ase.io.iread(f, index=":", format="traj"))
