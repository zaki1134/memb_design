from dataclasses import dataclass
from copy import deepcopy

from Pre.DimsCheck import CheckProcess
from Pre.DimsValidation import ValidationProcess
from Utils import Parameters


@dataclass
class Dimensions:
    dwg: dict

    def __post_init__(self):
        res = deepcopy(self.dwg)
        scale = self.dwg["shrinkage_rate"]

        res["product"]["dia_outer"] /= scale
        res["product"]["dia_eff"] /= scale

        if res["incell"]["info"]["shape"] == "circle":
            res["incell"]["info"]["dia_incell"] /= scale
        elif res["incell"]["info"]["shape"] == "hexagon":
            res["incell"]["info"]["dia_incell"] /= scale

        if res["outcell"]["info"]["shape"] == "octagon":
            res["outcell"]["info"]["thk_outcell"] /= scale
            res["outcell"]["info"]["thk_wall_outcell"] /= scale
        elif res["outcell"]["info"]["shape"] == "square":
            res["outcell"]["info"]["thk_outcell"] /= scale
            res["outcell"]["info"]["thk_wall_outcell"] /= scale

        self.prod = res

    def execute_check(self) -> None:
        CheckProcess(**self.dwg)
        CheckProcess(**self.prod)

    def execute_valid(self) -> None:
        ValidationProcess(Parameters(self.dwg))
        ValidationProcess(Parameters(self.prod))
