import dataclasses


@dataclasses.dataclass
class MACE_MP_0:
    """MACE MP-0 model."""

    def get_model(self):
        from mace.calculators import mace_mp

        return mace_mp()
