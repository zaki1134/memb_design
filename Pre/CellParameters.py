from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Parameters:
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
    pitch_x: float
    pitch_y: float
    pitch_slit: float
    thk_i2o: float
    lim_slit: float


@dataclass
class CalcParameters:
    @staticmethod
    def pitch_x(dia_incell: float, thk_wall: float) -> float:
        return dia_incell + thk_wall

    @staticmethod
    def pitch_y(pitch_x: float) -> float:
        return pitch_x * np.sin(np.pi / 3)

    @staticmethod
    def pitch_slit(thk_i2o: float, pitch_y: float, ratio_slit: int) -> float:
        ds1 = 2 * thk_i2o
        ds2 = (ratio_slit - 1) * pitch_y
        return ds1 + ds2

    @staticmethod
    def thk_i2o(
        shape_incell: str,
        thk_c2s: float,
        dia_incell: float,
        hight: float,  # 形状で異なるoutcellの高さ
    ) -> float:
        ds1 = 0.5 * hight + thk_c2s
        if shape_incell == "circle":
            return ds1 + 0.5 * dia_incell
        elif shape_incell == "hexagon":
            # heptagon
            return ds1 + 0.5 * dia_incell * np.cos(np.pi / 6)

    @staticmethod
    def lim_slit(
        dia_eff: float,
        shape_incell: str,
        dia_incell: float,
        thk_slit: float,
        num_ic_lim: int,
        pitch_y: float,
        thk_i2o: float,
    ) -> float:
        ds1 = 0.5 * dia_eff
        if num_ic_lim == 0:
            return ds1 - 0.5 * thk_slit
        else:
            ds2 = (num_ic_lim - 1) * pitch_y
            if shape_incell == "circle":
                return ds1 - ds2 - thk_i2o - 0.5 * dia_incell
            elif shape_incell == "hexagon":
                # heptagon
                return ds1 - ds2 - thk_i2o - 0.5 * dia_incell / np.cos(np.pi / 6)
