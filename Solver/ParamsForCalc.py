from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class CellParameters:
    dia_outer: float
    dia_eff: float
    ln_prod: float
    thk_wall: float
    thk_c2s: float
    offset_x: bool
    offset_y: bool
    shape_incell: str
    dia_incell: float
    thk_top: float
    thk_mid: float
    shape_outcell: str
    num_oc: int
    thk_outcell: float
    thk_wall_outcell: float
    thk_slit: float
    ratio_slit: int
    num_ic_lim: int

    @property
    def pitch_x(self) -> float:
        return self.dia_incell + self.thk_wall

    @property
    def pitch_y(self) -> float:
        return self.pitch_x * np.sin(np.pi / 3)

    @property
    def pitch_slit(self) -> float:
        ds1 = 2 * self.thk_i2o
        ds2 = (self.ratio_slit - 1) * self.pitch_y
        return ds1 + ds2

    @property
    def thk_i2o(self) -> float:
        ds1 = 0.5 * self.thk_outcell + self.thk_c2s
        if self.shape_incell == "circle":
            return ds1 + 0.5 * self.dia_incell
        elif self.shape_incell == "hexagon":
            # heptagon
            return ds1 + 0.5 * self.dia_incell * np.cos(np.pi / 6)

    @property
    def lim_slit(self) -> float:
        ds1 = 0.5 * self.dia_eff
        if self.num_ic_lim == 0:
            return ds1 - 0.5 * self.thk_slit
        else:
            ds2 = (self.num_ic_lim - 1) * self.pitch_y
            if self.shape_incell == "circle":
                return ds1 - ds2 - self.thk_i2o - 0.5 * self.dia_incell
            elif self.shape_incell == "hexagon":
                # heptagon
                return ds1 - ds2 - self.thk_i2o - 0.5 * self.dia_incell / np.cos(np.pi / 6)
