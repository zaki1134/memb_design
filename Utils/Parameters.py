from dataclasses import dataclass
from typing import Union

import numpy as np


class Parameters:
    def __init__(self, data: dict) -> None:
        self.shrinkage_rate = data["shrinkage_rate"]
        self.product = Product(**data["product"])

        if data["incell"]["info"]["shape"] == "circle":
            self.incell = Incell(
                info=ShapeCircle(**data["incell"]["info"]),
                thk_mid=data["incell"]["thk_mid"],
                thk_top=data["incell"]["thk_top"],
            )
        elif data["incell"]["info"]["shape"] == "hexagon":
            self.incell = Incell(
                info=ShapeHexagon(**data["incell"]["info"]),
                thk_mid=data["incell"]["thk_mid"],
                thk_top=data["incell"]["thk_top"],
            )

        if data["outcell"]["info"]["shape"] == "octagon":
            self.outcell = Outcell(
                info=ShapeOctagon(**data["outcell"]["info"]),
                num_oc=data["outcell"]["num_oc"],
            )
        elif data["outcell"]["info"]["shape"] == "square":
            self.outcell = Outcell(
                info=ShapeSquare(**data["outcell"]["info"]),
                num_oc=data["outcell"]["num_oc"],
            )

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
    def aspect_ratio_outcell(self) -> float:
        return self.outcell.info.thk_outcell / self.thk_outcell_x

    @property
    def chamfer_x(self) -> float:
        """octagonのみ"""
        if self.outcell.info.shape in ["octagon"]:
            if self.aspect_ratio_outcell >= 1:
                return 0.25 * self.thk_outcell_x
            else:
                return self.chamfer_y * np.tan(np.pi / 3)
        else:
            return 0.0

    @property
    def chamfer_y(self) -> float:
        """octagonのみ"""
        if self.outcell.info.shape in ["octagon"]:
            if self.aspect_ratio_outcell >= 1:
                return self.chamfer_x * np.tan(np.pi / 6)
            else:
                return 0.25 * self.outcell.info.thk_wall_outcell
        else:
            return 0.0

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
    info: Union[ShapeCircle, ShapeHexagon]
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
    info: Union[ShapeOctagon, ShapeSquare]
    num_oc: int


@dataclass
class Slit:
    thk_slit: float
    ratio_slit: int
    num_ic_lim: int
