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
    """Optimize the structure of a molecule.

    Attributes
    ----------
    data : list[ase.Atoms]
        Input data as a list of ASE Atoms objects.
    data_id : int
        Index of the ase.Atoms to optimize.
        Default to the last element in the data list.
    model : MACE_MP_0
        Model to use for optimization.
    fmax : float
        Maximum force as stopping criterion.
    trajectory : pathlib.Path
        Path to the trajectory file.
    optimizer : Optimizer
        Optimizer to use for structure optimization.
        Default to LBFGS.
    """

    data: list[ase.Atoms] = zntrack.deps()
    model: MACE_MP_0 = zntrack.deps()

    data_id: int = zntrack.params(-1)
    fmax: float = zntrack.params(0.05)
    trajectory: pathlib.Path = zntrack.outs_path(zntrack.nwd / "trajectory.traj")

    optimizer: Optimizer = zntrack.params(str(Optimizer.LBFGS))

    def run(self):
        """Primary Node run method."""
        atoms = self.data[self.data_id]
        atoms.calc = self.model.get_model()
        optim = getattr(ase.optimize, self.optimizer)
        dyn = optim(atoms, trajectory=self.trajectory.as_posix())
        dyn.run(fmax=self.fmax)

    @property
    def frames(self):
        """List of generated conformers."""
        with self.state.fs.open(self.trajectory, "rb") as f:
            return list(ase.io.iread(f, index=":", format="traj"))
