from dataclasses import dataclass
from logging import getLogger

import numpy as np

from ..Utils import Parameters

logger = getLogger(__name__)


@dataclass
class ValidationProcess:
    prod_dims: Parameters

    def __post_init__(self):
        # eff_dia_incell size check
        value = self.prod_dims.eff_dia_incell
        if np.isclose(value, 0) or value < 0:
            logger.error("'eff_dia_incell' is too small.")
            raise ValueError

        # dia_eff size check
        value = self.prod_dims.product.dia_eff - self.prod_dims.incell.info.dia_incell
        if np.isclose(value, 0) or value < 0:
            logger.error("'eff_dia_incell' is too small.")
            raise ValueError

        # thk_slit vs thk_outcell
        flag_1 = np.isclose(self.prod_dims.slit.thk_slit, self.prod_dims.outcell.info.thk_outcell)
        flag_2 = self.prod_dims.slit.thk_slit != self.prod_dims.outcell.info.thk_outcell
        if flag_1 and flag_2:
            logger.error("'thk_slit' is close to 'thk_outcell' but does not match.")
            raise ValueError

        # thk_slit vs thk_outcell(chamfer)
        value = self.prod_dims.outcell.info.thk_outcell - 2 * self.prod_dims.chamfer_y
        flag_1 = np.isclose(self.prod_dims.slit.thk_slit, value)
        flag_2 = self.prod_dims.slit.thk_slit != value
        if flag_1 and flag_2:
            logger.error("'thk_slit' is close to 'thk_outcell' but does not match.")
            raise ValueError

        # thk_slit vs in-hex
        value = self.prod_dims.thk_i2o - 0.5 * self.prod_dims.pitch_x / np.cos(np.pi / 6)
        flag_1 = np.isclose(self.prod_dims.slit.thk_slit, 2 * value)
        flag_2 = self.prod_dims.slit.thk_slit >= value
        if flag_1 and flag_2:
            logger.error("'thk_slit' and 'in-hex' contact.")
            raise ValueError


# Shapelyにしよう
class ValidationFunctions:
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
        # if ValidParams().__line_i2o(xxx, thk_i2o, pitch_x) < 0.5 * thk_outcell:
        #     message = [
        #         f"{name}: 'thk_outcell' is too large",
        #         f"thk_outcell: {thk_outcell}",
        #         f"thk_wall_outcell: {thk_wall_outcell}",
        #         f"pitch_x: {pitch_x}",
        #         f"thk_i2o: {thk_i2o}",
        #     ]
        #     raise ValueError("\n".join(message))
        return xxx
