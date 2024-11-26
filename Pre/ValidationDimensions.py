from dataclasses import dataclass
from logging import getLogger

import numpy as np

logger = getLogger(__name__)

# Shapelyにしよう


@dataclass(frozen=True)
class ValidationProcess:
    prod_dims: dict

    def __post_init__(self):
        ValidationFunctions.valid_dia_incell(
            self.prod_dims["incell"]["info"]["dia_incell"],
            self.prod_dims["incell"]["thk_top"],
            self.prod_dims["incell"]["thk_mid"],
        )
        ValidationFunctions.valid_dia_prod(
            self.prod_dims["product"]["dia_eff"],
            self.prod_dims["incell"]["info"]["dia_incell"],
        )


class ValidationFunctions:
    @staticmethod
    def valid_dia_incell(
        dia_incell: float,
        thk_top: float,
        thk_mid: float,
    ) -> None:
        """dia_incellの値が適切かどうかをチェック.
        インセルの有効面積が0以下ではないかを確認."""
        value = dia_incell - 2 * (thk_top + thk_mid)
        if np.isclose(value, 0) or value < 0:
            logger.error("'dia_incell' is too small.")
            raise ValueError

    @staticmethod
    def valid_dia_prod(
        dia_eff: float,
        dia_incell: float,
    ) -> None:
        """dia_prodの値が適切かどうかをチェック.
        incelllが最低でも1つは配置されるようにする."""
        value = dia_eff - dia_incell
        if np.isclose(value, 0) or value < 0:
            logger.error("'dia_prod' is too small.")
            raise ValueError

    @staticmethod
    def valid_thk_slit_and_thk_outcell(
        name: str,
        thk_outcell: float,
        thk_y1: float,
        thk_slit: float,
    ) -> None:
        """thk_slitとthk_outcellの値が適切かどうかをチェック. thk_outcell vs thk_slit
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
        """thk_outcellの値が適切かどうかをチェック. outcell vs in-hex
        incell-outcell間の境界をアウトセル角Y位置が通過するかどうかを確認.メッシュの対称性のため.
        """
        xxx = 0.5 * (pitch_x - thk_wall_outcell) - thk_x1
        if ValidParams().__line_i2o(xxx, thk_i2o, pitch_x) < 0.5 * thk_outcell:
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
        """thk_slitの値が適切かどうかをチェック. slit vs in-hex
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
