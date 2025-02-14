from dataclasses import dataclass

import numpy as np


class Parameters:
    def __init__(self, data: dict) -> None:
        self.shrinkage_rate = data["shrinkage_rate"]
        self.product = Product(**data["product"])
        self.incell = Incell(**data["incell"])
        self.outcell = Outcell(**data["outcell"])
        self.slit = Slit(**data["slit"])

    @property
    def eff_dia_incell(self) -> float:
        return self.incell.info.dia_incell - 2 * (self.incell.thk_top + self.incell.thk_mid)

    @property
    def thk_outcell_x(self) -> float:
        value = self.pitch_x - self.outcell.num_oc * self.outcell.info.thk_wall_outcell
        value /= self.outcell.num_oc
        return value

    @property
    def ratio_outcell(self) -> float:
        return self.outcell.info.thk_outcell / self.thk_outcell_x

    @property
    def chamfer_x(self) -> float:
        if self.ratio_outcell >= 1:
            return 0.25 * self.thk_outcell_x
        else:
            return self.chamfer_y * np.tan(np.pi / 3)

    @property
    def chamfer_y(self) -> float:
        if self.ratio_outcell >= 1:
            return self.chamfer_x * np.tan(np.pi / 6)
        else:
            return 0.25 * self.outcell.info.thk_wall_outcell

    @property
    def pitch_x(self) -> float:
        return self.incell.info.dia_incell + self.product.thk_wall

    @property
    def pitch_y(self) -> float:
        return self.pitch_x * np.sin(np.pi / 3)

    @property
    def pitch_slit(self) -> float:
        ds1 = 2 * self.thk_i2o
        ds2 = (self.slit.ratio_slit - 1) * self.pitch_y
        return ds1 + ds2

    @property
    def thk_i2o(self) -> float:
        ds1 = 0.5 * self.outcell.info.thk_outcell + self.product.thk_c2s
        if self.incell.info.shape == "circle":
            return ds1 + 0.5 * self.incell.info.dia_incell
        elif self.incell.info.shape == "hexagon":
            # heptagon
            return ds1 + 0.5 * self.incell.info.dia_incell * np.cos(np.pi / 6)

    @property
    def lim_slit(self) -> float:
        ds1 = 0.5 * self.product.dia_eff
        if self.slit.num_ic_lim == 0:
            return ds1 - 0.5 * self.slit.thk_slit
        else:
            ds2 = (self.slit.num_ic_lim - 1) * self.pitch_y
            if self.incell.info.shape == "circle":
                return ds1 - ds2 - self.thk_i2o - 0.5 * self.incell.info.dia_incell
            elif self.incell.info.shape == "hexagon":
                # heptagon
                return ds1 - ds2 - self.thk_i2o - 0.5 * self.incell.info.dia_incell / np.cos(np.pi / 6)


@dataclass
class Product:
    dia_outer: float
    dia_eff: float
    ln_prod: float
    thk_wall: float
    thk_c2s: float
    offset_x: bool
    offset_y: bool


@dataclass
class ShapeCircle:
    shape: str
    dia_incell: float


@dataclass
class ShapeHexagon:
    shape: str
    dia_incell: float


@dataclass
class Incell:
    info: ShapeCircle | ShapeHexagon
    thk_top: float
    thk_mid: float


@dataclass
class ShapeOctagon:
    shape: str
    thk_outcell: float
    thk_wall_outcell: float


@dataclass
class ShapeSquare:
    shape: str
    thk_outcell: float
    thk_wall_outcell: float


@dataclass
class Outcell:
    info: ShapeOctagon | ShapeSquare
    num_oc: int


@dataclass
class Slit:
    thk_slit: float
    ratio_slit: int
    num_ic_lim: int
