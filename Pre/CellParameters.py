from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class CellParameters:
    shape_incell: str
    shape_outcell: str
    dia_incell: float
    thk_top: float
    thk_mid: float
    thk_wall: float
    thk_c2s: float
    dia_prod: float
    thk_prod: float
    thk_outcell: float
    thk_wall_outcell: float
    thk_slit: float
    ratio_slit: int
    mode_cell: bool
    mode_slit: bool
    ln_prod: float
    chamfer_deg: float = np.pi / 4
    chamfer_size: float = 0.25

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

        ds1 = 0.5 * self.dia_prod - self.thk_prod
        ds2 = (num - 1) * self.pitch_y

        if self.shape_incell == "circle":
            return ds1 - ds2 - self.thk_i2o - 0.5 * self.dia_incell
        elif self.shape_incell == "hexagon":
            # heptagon
            return ds1 - ds2 - self.thk_i2o - 0.5 * self.dia_incell / np.cos(np.pi / 6)

    @property
    def thk_x1(self) -> float:
        """アウトセルのC面取りX方向サイズ"""
        height = self.thk_outcell
        width = self.pitch_x - self.thk_wall_outcell
        if height < width:
            return self.chamfer_size * height * np.tan(self.chamfer_deg)
        else:
            return self.chamfer_size * width

    @property
    def thk_y1(self) -> float:
        """アウトセルのC面取りY方向サイズ"""
        height = self.thk_outcell
        width = self.pitch_x - self.thk_wall_outcell
        if height < width:
            return self.chamfer_size * height
        else:
            return self.chamfer_size * width / np.tan(self.chamfer_deg)

    def __post_init__(self) -> None:
        self.__type_check()
        self.__value_check()  # 負数チェック、ゼロを許容するかどうか
        self.__validate()  # 各パラメータの成立性のチェック

    def __type_check(self) -> None:
        name = self.__class__.__name__
        if not isinstance(self.shape_incell, str):
            raise TypeError(f"{name}: 'shape_incell' must be a string")
        if not isinstance(self.shape_outcell, str):
            raise TypeError(f"{name}: 'shape_outcell' must be a string")
        if not isinstance(self.dia_incell, float):
            raise TypeError(f"{name}: 'dia_incell' must be a float")
        if not isinstance(self.thk_top, float):
            raise TypeError(f"{name}: 'thk_top' must be a float")
        if not isinstance(self.thk_mid, float):
            raise TypeError(f"{name}: 'thk_mid' must be a float")
        if not isinstance(self.thk_wall, float):
            raise TypeError(f"{name}: 'thk_wall' must be a float")
        if not isinstance(self.thk_c2s, float):
            raise TypeError(f"{name}: 'thk_c2s' must be a float")
        if not isinstance(self.dia_prod, float):
            raise TypeError(f"{name}: 'dia_prod' must be a float")
        if not isinstance(self.thk_prod, float):
            raise TypeError(f"{name}: 'thk_prod' must be a float")
        if not isinstance(self.thk_outcell, float):
            raise TypeError(f"{name}: 'thk_outcell' must be a float")
        if not isinstance(self.thk_wall_outcell, float):
            raise TypeError(f"{name}: 'thk_wall_outcell' must be a float")
        if not isinstance(self.thk_slit, float):
            raise TypeError(f"{name}: 'thk_slit' must be a float")
        if not isinstance(self.ratio_slit, int):
            raise TypeError(f"{name}: 'ratio_slit' must be an integer")
        if not isinstance(self.mode_cell, bool):
            raise TypeError(f"{name}: 'mode_cell' must be a boolean")
        if not isinstance(self.mode_slit, bool):
            raise TypeError(f"{name}: 'mode_slit' must be a boolean")
        if not isinstance(self.ln_prod, float):
            raise TypeError(f"{name}: 'ln_prod' must be a float")

    def __value_check(self) -> None:
        name = self.__class__.__name__
        if self.shape_incell not in ["circle", "hexagon"]:
            raise ValueError(f"{name}: 'mode_cell' must be either 'circle' or 'hexagon'")
        if self.shape_outcell not in ["octagon"]:
            raise ValueError(f"{name}: 'mode_cell' must be 'octagon'")
        if self.dia_incell <= 0:
            raise ValueError(f"{name}: 'dia_incell' must be greater than 0")
        if self.thk_top < 0:
            raise ValueError(f"{name}: 'thk_top' must be greater than or equal to 0")
        if self.thk_mid < 0:
            raise ValueError(f"{name}: 'thk_mid' must be greater than or equal to 0")
        if self.thk_wall <= 0:
            raise ValueError(f"{name}: 'thk_wall' must be greater than 0")
        if self.thk_c2s <= 0:
            raise ValueError(f"{name}: 'thk_c2s' must be greater than 0")
        if self.dia_prod <= 0:
            raise ValueError(f"{name}: 'dia_prod' must be greater than 0")
        if self.thk_prod <= 0:
            raise ValueError(f"{name}: 'thk_prod' must be greater than 0")
        if self.thk_outcell <= 0:
            raise ValueError(f"{name}: 'thk_outcell' must be greater than 0")
        if self.thk_wall_outcell <= 0:
            raise ValueError(f"{name}: 'thk_wall_outcell' must be greater than 0")
        if self.thk_slit <= 0:
            raise ValueError(f"{name}: 'thk_slit' must be greater than 0")
        if self.ratio_slit <= 1:
            raise ValueError(f"{name}: 'ratio_slit' must be greater than 1")
        if self.ln_prod <= 0:
            raise ValueError(f"{name}: 'ln_prod' must be greater than 0")

    def __validate(self) -> None:
        name = self.__class__.__name__

        # dia_prod, dia_incell, thk_prod
        ValidateParameters.valid_dia_prod(
            name,
            self.dia_prod,
            self.dia_incell,
            self.thk_prod,
        )

        # dia_incell, thk_top, thk_mid
        ValidateParameters.valid_dia_incell(
            name,
            self.dia_incell,
            self.thk_top,
            self.thk_mid,
        )

        if self.shape_outcell == "octagon":
            # thk_slit, thk_outcell
            ValidateParameters.valid_thk_slit_and_thk_outcell(
                name,
                self.thk_outcell,
                self.thk_y1,
                self.thk_slit,
            )

            # thk_slit, pitch_x
            ValidateParameters.valid_thk_slit(
                name,
                self.thk_slit,
                self.thk_i2o,
                self.pitch_x,
            )

            # thk_outcell, thk_wall_outcell, pitch_x, thk_i2o
            ValidateParameters.valid_thk_outcell(
                name,
                self.pitch_x,
                self.thk_wall_outcell,
                self.thk_outcell,
                self.thk_i2o,
                self.thk_x1,
            )


class ValidateParameters:
    @staticmethod
    def valid_dia_incell(
        name: str,
        dia_incell: float,
        thk_top: float,
        thk_mid: float,
    ) -> None:
        """dia_incellの値が適切かどうかをチェック.
        インセルの有効面積が0ではない."""
        value = dia_incell - 2 * (thk_top + thk_mid)
        if value <= 0:
            message = [
                f"{name}: 'dia_incell' must be greater than 2*(thk_top + thk_mid)",
                f"dia_incell: {dia_incell}",
                f"thk_top: {thk_top}",
                f"thk_mid: {thk_mid}",
            ]
            raise ValueError("\n".join(message))

    @staticmethod
    def valid_dia_prod(
        name: str,
        dia_prod: float,
        dia_incell: float,
        thk_prod: float,
    ) -> None:
        """dia_prodの値が適切かどうかをチェック.
        incelllが最低でも1つは配置されるようにする."""
        value = dia_prod - (dia_incell + 2 * thk_prod)
        if np.isclose(value, 0) or value < 0:
            message = [
                f"{name}: 'dia_prod' must be greater than dia_incell + 2*thk_prod",
                f"dia_prod: {dia_prod}",
                f"dia_incell: {dia_incell}",
                f"thk_prod: {thk_prod}",
            ]
            raise ValueError("\n".join(message))

    @staticmethod
    def valid_thk_slit_and_thk_outcell(
        name: str,
        thk_outcell: float,
        thk_y1: float,
        thk_slit: float,
    ) -> None:
        """thk_slitとthk_outcellの値が適切かどうかをチェック.
        thk_slitとthk_outcellの値が近い場合はエラー.薄いメッシュの作成を抑制"""
        if np.isclose(thk_slit, thk_outcell) and thk_slit != thk_outcell:
            message = [
                f"{name}: 'thk_slit' is close to 'thk_outcell' but does not match",
                f"thk_slit: {thk_slit}",
                f"thk_outcell: {thk_outcell}",
            ]
            raise ValueError("\n".join(message))

        yyy = thk_outcell - 2 * thk_y1
        if np.isclose(thk_slit, yyy) and thk_slit != yyy:
            message = [
                f"{name}: 'thk_slit' is close to 'thk_outcell' but does not match",
                f"thk_slit: {thk_slit}",
                f"thk_outcell: {thk_outcell}",
            ]
            raise ValueError("\n".join(message))

    @staticmethod
    def valid_thk_outcell(
        name: str,
        pitch_x: float,
        thk_wall_outcell: float,
        thk_outcell: float,
        thk_i2o: float,
        thk_x1: float,
    ) -> None:
        """thk_outcellの値が適切かどうかをチェック.
        incell-outcell間の境界をアウトセル角Y位置が通過するかどうかを確認.メッシュの対称性のため.
        """
        xxx = 0.5 * (pitch_x - thk_wall_outcell) - thk_x1
        if ValidateParameters().__line_i2o(xxx, thk_i2o, pitch_x) < 0.5 * thk_outcell:
            message = [
                f"{name}: 'thk_outcell' is too large",
                f"thk_outcell: {thk_outcell}",
                f"thk_wall_outcell: {thk_wall_outcell}",
                f"pitch_x: {pitch_x}",
                f"thk_i2o: {thk_i2o}",
            ]
            raise ValueError("\n".join(message))

    @staticmethod
    def valid_thk_slit(
        name: str,
        thk_slit: float,
        thk_i2o: float,
        pitch_x: float,
    ) -> None:
        """thk_slitの値が適切かどうかをチェック.
        incell-outcell間の境界をスリットY位置が通過するかどうかを確認.メッシュの対称性のため.
        """
        yyy = thk_i2o - 0.5 * pitch_x / np.cos(np.pi / 6)
        if np.isclose(0.5 * thk_slit, yyy) or 0.5 * thk_slit >= yyy:
            message = [
                f"{name}: 'thk_slit' is too large",
                f"thk_slit: {thk_slit}",
                f"thk_i2o: {thk_i2o}",
                f"pitch_x: {pitch_x}",
            ]
            raise ValueError("\n".join(message))

    @staticmethod
    def __line_i2o(
        x: float,
        thk_i2o: float,
        pitch_x: float,
    ) -> float:
        """incell-outcell間の境界を y=ax+b で表現"""
        a = -1 / np.sqrt(3)
        b = thk_i2o - 0.5 * pitch_x * np.tan(np.pi / 6)
        return a * x + b
