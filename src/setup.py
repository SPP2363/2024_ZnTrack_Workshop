import pathlib

import ase.io
import zntrack
from rdkit2ase import smiles2conformers


class Smiles2Conformers(zntrack.Node):
    """Create multiple conformers from a SMILES string.

    Attributes
    ----------
    smiles : str
        The SMILES string to generate conformers for.
    num_confs : int
        The number of conformers to generate.
    random_seed : int
        The random seed for conformer generation.
    max_attempts : int
        The maximum number of attempts for conformer generation.
    """

    smiles: str = zntrack.params()
    num_confs: int = zntrack.params()
    random_seed: int = zntrack.params(42)
    max_attempts: int = zntrack.params(1000)

    frames_path: pathlib.Path = zntrack.outs_path(zntrack.nwd / "frames.xyz")

    def run(self):
        """Primary Node run method."""
        frames = smiles2conformers(
            smiles=self.smiles,
            numConfs=self.num_confs,
            randomSeed=self.random_seed,
            maxAttempts=self.max_attempts,
        )
        ase.io.write(self.frames_path, frames, format="xyz")

    @property
    def frames(self) -> list[ase.Atoms]:
        """List of generated conformers."""
        with self.state.fs.open(self.frames_path, "r") as f:
            return list(ase.io.iread(f, index=":", format="extxyz"))
