from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class CommonParameters:
    dia_incell: float
    dia_land: float
    dia_land_out: float
    ln_prod: float
    offset_x: bool
    offset_y: bool
    ratio_slit: int
    shape_incell: str
    shape_outcell: str
    thk_c2s: float
    thk_mid: float
    thk_outcell: float
    thk_slit: float
    thk_top: float
    thk_wall: float
    thk_wall_outcell: float

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
        """インセルからアウトセルまでの距離
        CircleとHexagonで異なる
        """
        ds1 = 0.5 * max(self.thk_slit, self.thk_outcell) + self.thk_c2s
        if self.shape_incell == "circle":
            return ds1 + 0.5 * self.dia_incell
        elif self.shape_incell == "hexagon":
            # heptagon
            return ds1 + 0.5 * self.dia_incell * np.cos(np.pi / 6)

    @property
    def lim_slit(self, num: int = 1) -> float:
        """スリットの制限サイズ
        Y方向末端では少なくともnum個のインセルが配置される
        """
        if num <= 0:
            raise ValueError("lim_slit: num must be greater than 0")

        ds1 = 0.5 * self.dia_land - self.dia_land_out
        ds2 = (num - 1) * self.pitch_y

        if self.shape_incell == "circle":
            return ds1 - ds2 - self.thk_i2o - 0.5 * self.dia_incell
        elif self.shape_incell == "hexagon":
            # heptagon
            return ds1 - ds2 - self.thk_i2o - 0.5 * self.dia_incell / np.cos(np.pi / 6)
