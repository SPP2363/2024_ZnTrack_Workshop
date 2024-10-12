import dataclasses


@dataclasses.dataclass
class MACE_MP_0:
    def get_model(self):
        from mace.calculators import mace_mp

        return mace_mp()
