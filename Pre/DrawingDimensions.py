from dataclasses import dataclass
from logging import getLogger

logger = getLogger(__name__)


@dataclass(frozen=True)
class CheckDimensinons:
    shrinkage_rate: float
    product: dict
    incell: dict
    outcell: dict
    slit: dict

    def __post_init__(self) -> None:
        self.__type_check()
        self.__value_check()

    def __type_check(self) -> None:
        if not isinstance(self.shrinkage_rate, float):
            logger.error("'shrinkage_rate' must be a float")

        if isinstance(self.product, dict):
            CheckProduct(**self.product)
        else:
            logger.error("'product' must be a dict")

        if isinstance(self.incell, dict):
            CheckIncell(**self.incell)
        else:
            logger.error("'incell' must be a dict")

        if isinstance(self.outcell, dict):
            CheckOutcell(**self.outcell)
        else:
            logger.error("'outcell' must be a dict")

        if isinstance(self.slit, dict):
            CheckSlit(**self.slit)
        else:
            logger.error("'slit' must be a dict")

    def __value_check(self) -> None:
        if self.shrinkage_rate <= 0:
            logger.error("'shrinkage_rate' <= 0")


@dataclass(frozen=True)
class CheckProduct:
    dia_outer: float
    dia_eff: float
    ln_prod: float
    thk_wall: float
    thk_c2s: float
    offset_x: bool
    offset_y: bool

    def __post_init__(self) -> None:
        self.__type_check()
        self.__value_check()

    def __type_check(self) -> None:
        if not isinstance(self.dia_outer, float):
            logger.error("'dia_outer' must be a float")
        if not isinstance(self.dia_eff, float):
            logger.error("'dia_eff' must be a float")
        if not isinstance(self.ln_prod, float):
            logger.error("'ln_prod' must be a float")
        if not isinstance(self.thk_wall, float):
            logger.error("'thk_wall' must be a float")
        if not isinstance(self.thk_c2s, float):
            logger.error("'thk_c2s' must be a float")
        if not isinstance(self.offset_x, bool):
            logger.error("'offset_x' must be a bool")
        if not isinstance(self.offset_y, bool):
            logger.error("'offset_y' must be a bool")

    def __value_check(self) -> None:
        if self.dia_outer <= 0:
            logger.error("'dia_outer' <= 0")
        if self.dia_eff <= 0:
            logger.error("'dia_eff' <= 0")
        if self.ln_prod <= 0:
            logger.error("'ln_prod' <= 0")
        if self.thk_wall <= 0:
            logger.error("'thk_wall' <= 0")
        if self.thk_c2s <= 0:
            logger.error("'thk_c2s' <= 0")


@dataclass(frozen=True)
class CheckIncell:
    shape: str
    info: dict
    thk_top: float
    thk_mid: float

    def __post_init__(self) -> None:
        self.__type_check()
        self.__value_check()

    def __type_check(self) -> None:
        if not isinstance(self.shape, str):
            logger.error("'shape' must be a str")

        if isinstance(self.info, dict):
            if self.shape == "circle":
                ShapeCircle(**self.info)
            elif self.shape == "hexagon":
                ShapeHexagon(**self.info)
            else:
                logger.error("Invalid 'incell shape'")
        else:
            logger.error("'info' must be a dict")

        if not isinstance(self.thk_top, float):
            logger.error("'thk_top' must be a float")
        if not isinstance(self.thk_mid, float):
            logger.error("'thk_mid' must be a float")

    def __value_check(self) -> None:
        if self.thk_top < 0:
            logger.error("'thk_top' < 0")
        if self.thk_mid < 0:
            logger.error("'thk_mid' < 0")


@dataclass(frozen=True)
class ShapeCircle:
    dia_incell: float

    def __post_init__(self) -> None:
        self.__type_check()
        self.__value_check()

    def __type_check(self) -> None:
        if not isinstance(self.dia_incell, float):
            logger.error("'dia_incell' must be a float")

    def __value_check(self) -> None:
        if self.dia_incell <= 0:
            logger.error("'dia_incell' <= 0")


@dataclass(frozen=True)
class ShapeHexagon:
    dia_incell: float

    def __post_init__(self) -> None:
        self.__type_check()
        self.__value_check()

    def __type_check(self) -> None:
        if not isinstance(self.dia_incell, float):
            logger.error("'dia_incell' must be a float")

    def __value_check(self) -> None:
        if self.dia_incell <= 0:
            logger.error("'dia_incell' <= 0")


@dataclass(frozen=True)
class CheckOutcell:
    shape: str
    num_oc: int
    info: dict

    def __post_init__(self) -> None:
        self.__type_check()
        self.__value_check()

    def __type_check(self) -> None:
        if not isinstance(self.shape, str):
            logger.error("'shape' must be a str")
        if not isinstance(self.num_oc, int):
            logger.error("'num_oc' must be an int")

        if isinstance(self.info, dict):
            if self.shape == "octagon":
                ShapeOctagon(**self.info)
            elif self.shape == "square":
                ShapeSquare(**self.info)
            else:
                logger.error("Invalid 'outcell shape'")
        else:
            logger.error("'info' must be a dict")

    def __value_check(self) -> None:
        if self.num_oc < 0:
            logger.error("'num_oc' < 0")


@dataclass(frozen=True)
class ShapeOctagon:
    thk_outcell: float
    thk_wall_outcell: float

    def __post_init__(self) -> None:
        self.__type_check()
        self.__value_check()

    def __type_check(self) -> None:
        if not isinstance(self.thk_outcell, float):
            logger.error("'thk_outcell' must be a float")
        if not isinstance(self.thk_wall_outcell, float):
            logger.error("'thk_wall_outcell' must be a float")

    def __value_check(self) -> None:
        if self.thk_outcell <= 0:
            logger.error("'thk_outcell' <= 0")
        if self.thk_wall_outcell <= 0:
            logger.error("'thk_wall_outcell' <= 0")


@dataclass(frozen=True)
class ShapeSquare:
    thk_outcell: float
    thk_wall_outcell: float

    def __post_init__(self) -> None:
        self.__type_check()
        self.__value_check()

    def __type_check(self) -> None:
        if not isinstance(self.thk_outcell, float):
            logger.error("'thk_outcell' must be a float")
        if not isinstance(self.thk_wall_outcell, float):
            logger.error("'thk_wall_outcell' must be a float")

    def __value_check(self) -> None:
        if self.thk_outcell <= 0:
            logger.error("'thk_outcell' <= 0")
        if self.thk_wall_outcell <= 0:
            logger.error("'thk_wall_outcell' <= 0")


@dataclass(frozen=True)
class CheckSlit:
    thk_slit: float
    ratio_slit: int
    num_ic_lim: int

    def __post_init__(self) -> None:
        self.__type_check()
        self.__value_check()

    def __type_check(self) -> None:
        if not isinstance(self.thk_slit, float):
            logger.error("'thk_slit' must be a float")
        if not isinstance(self.ratio_slit, int):
            logger.error("'ratio_slit' must be an int")
        if not isinstance(self.num_ic_lim, int):
            logger.error("'num_ic_lim' must be an int")

    def __value_check(self) -> None:
        if self.thk_slit <= 0:
            logger.error("'thk_slit' <= 0")
        if self.ratio_slit < 1:
            logger.error("'ratio_slit' < 1")
        if self.num_ic_lim < 0:
            logger.error("'num_ic_lim' < 0")
        elif self.num_ic_lim > self.ratio_slit:
            logger.error("'num_ic_lim' > 'ratio_slit'")
