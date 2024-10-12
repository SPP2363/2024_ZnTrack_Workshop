import pathlib

import ase.io
import zntrack
from rdkit2ase import smiles2conformers


class Smiles2Conformers(zntrack.Node):
    smiles: str = zntrack.params()
    num_confs: int = zntrack.params()
    random_seed: int = zntrack.params(42)
    max_attempts: int = zntrack.params(1000)

    frames_path: pathlib.Path = zntrack.outs_path(zntrack.nwd / "frames.xyz")

    def run(self):
        frames = smiles2conformers(
            smiles=self.smiles,
            numConfs=self.num_confs,
            randomSeed=self.random_seed,
            maxAttempts=self.max_attempts,
        )
        ase.io.write(self.frames_path, frames, format="xyz")

    @property
    def frames(self) -> list[ase.Atoms]:
        with self.state.fs.open(self.frames_path, "r") as f:
            return list(ase.io.iread(f, index=":", format="extxyz"))
