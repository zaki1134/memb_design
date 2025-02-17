import sys
from pathlib import Path

sys.path.append(str(Path.cwd().parent))

from dataclasses import dataclass
from logging import getLogger

import numpy as np
from shapely.geometry import Polygon

from Utils import Parameters, hexagon, octagon, square

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
            logger.error("'thk_slit' and 'in-hex' overlap.")
            raise ValueError

        # outcell vs in-hex
        flag = ValidationFunctions.valid_thk_outcell(self.prod_dims)
        if flag:
            logger.error("'outcell' and 'in-hex' overlap.")
            raise ValueError


class ValidationFunctions:
    @staticmethod
    def valid_thk_outcell(par: Parameters) -> bool:
        # outcell
        pitch_oc = par.outcell.info.thk_wall_outcell + par.thk_outcell_x
        offset = np.arange(0, par.outcell.num_oc, dtype=int) * pitch_oc

        if par.outcell.info.shape == "octagon":
            outcell = octagon(
                par.thk_outcell_x,
                par.outcell.info.thk_wall_outcell,
                par.chamfer_x,
                par.chamfer_y,
            )
        elif par.outcell.info.shape == "square":
            outcell = square(par.thk_outcell_x, par.outcell.info.thk_wall_outcell)

        outcell_mat = np.tile(outcell, (par.outcell.num_oc, 1, 1))
        outcell_mat[:, :, 0] += offset[:, np.newaxis]

        # in-hex
        inhex = hexagon(0.5 * par.pitch_x)
        inhex[:, 0] += 0.5 * par.pitch_x
        inhex[:, 1] += par.thk_i2o

        # make Polygon
        inhex = Polygon(inhex)
        outcells = [Polygon(cell) for cell in outcell_mat]

        # check
        intersects = [inhex.intersects(cell) for cell in outcells]

        return np.any(intersects)
