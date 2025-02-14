from dataclasses import dataclass
from logging import getLogger

logger = getLogger(__name__)


@dataclass
class CheckDimensinons:
    """inp.yamlの内容をチェックするクラス

    Raises
    ------
    ValueError
        入力値が負数の場合
    """

    shrinkage_rate: float
    product: dict
    incell: dict
    outcell: dict
    slit: dict

    def __post_init__(self) -> None:
        if self.shrinkage_rate <= 0:
            logger.error("'shrinkage_rate' <= 0")
            raise ValueError
        CheckProduct(**self.product)
        CheckIncell(**self.incell)
        CheckOutcell(**self.outcell)
        CheckSlit(**self.slit)


@dataclass
class CheckProduct:
    dia_outer: float
    dia_eff: float
    ln_prod: float
    thk_wall: float
    thk_c2s: float
    offset_x: bool
    offset_y: bool

    def __post_init__(self) -> None:
        if self.dia_outer <= 0:
            logger.error("'dia_outer' <= 0")
            raise ValueError
        if self.dia_eff <= 0:
            logger.error("'dia_eff' <= 0")
            raise ValueError
        if self.ln_prod <= 0:
            logger.error("'ln_prod' <= 0")
            raise ValueError
        if self.thk_wall <= 0:
            logger.error("'thk_wall' <= 0")
            raise ValueError
        if self.thk_c2s <= 0:
            logger.error("'thk_c2s' <= 0")
            raise ValueError


@dataclass
class CheckIncell:
    info: dict
    thk_top: float
    thk_mid: float

    def __post_init__(self) -> None:
        if self.info["shape"] == "circle":
            ShapeCircle(**self.info)
        elif self.info["shape"] == "hexagon":
            ShapeHexagon(**self.info)
        else:
            logger.error("Invalid 'incell info shape'")
            raise ValueError

        if self.thk_top < 0:
            logger.error("'thk_top' < 0")
            raise ValueError
        if self.thk_mid < 0:
            logger.error("'thk_mid' < 0")
            raise ValueError


@dataclass
class CheckOutcell:
    info: dict
    num_oc: int

    def __post_init__(self) -> None:
        if self.info["shape"] == "octagon":
            ShapeOctagon(**self.info)
        elif self.info["shape"] == "square":
            ShapeSquare(**self.info)
        else:
            logger.error("Invalid 'outcell info shape'")
            raise ValueError

        if self.num_oc < 0:
            logger.error("'num_oc' < 0")
            raise ValueError


@dataclass
class CheckSlit:
    thk_slit: float
    ratio_slit: int
    num_ic_lim: int

    def __post_init__(self) -> None:
        if self.thk_slit <= 0:
            logger.error("'thk_slit' <= 0")
            raise ValueError
        if self.ratio_slit < 1:
            logger.error("'ratio_slit' < 1")
            raise ValueError
        if self.num_ic_lim < 0:
            logger.error("'num_ic_lim' < 0")
            raise ValueError
        elif self.num_ic_lim > self.ratio_slit:
            logger.error("'num_ic_lim' > 'ratio_slit'")
            raise ValueError


# incell info shape


@dataclass
class ShapeCircle:
    shape: str
    dia_incell: float

    def __post_init__(self) -> None:
        if self.dia_incell <= 0:
            logger.error("'dia_incell' <= 0")
            raise ValueError


@dataclass
class ShapeHexagon:
    shape: str
    dia_incell: float

    def __post_init__(self) -> None:
        if self.dia_incell <= 0:
            logger.error("'dia_incell' <= 0")
            raise ValueError


# outcell info shape


@dataclass
class ShapeOctagon:
    shape: str
    thk_outcell: float
    thk_wall_outcell: float

    def __post_init__(self) -> None:
        if self.thk_outcell <= 0:
            logger.error("'thk_outcell' <= 0")
            raise ValueError
        if self.thk_wall_outcell <= 0:
            logger.error("'thk_wall_outcell' <= 0")
            raise ValueError


@dataclass
class ShapeSquare:
    shape: str
    thk_outcell: float
    thk_wall_outcell: float

    def __post_init__(self) -> None:
        if self.thk_outcell <= 0:
            logger.error("'thk_outcell' <= 0")
            raise ValueError
        if self.thk_wall_outcell <= 0:
            logger.error("'thk_wall_outcell' <= 0")
            raise ValueError
