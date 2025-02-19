from dataclasses import dataclass


@dataclass
class CheckProcess:
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

    def __post_init__(self):
        if self.shrinkage_rate <= 0:
            raise ValueError("'shrinkage_rate' <= 0")
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

    def __post_init__(self):
        if self.dia_outer <= 0:
            raise ValueError("'dia_outer' <= 0")
        if self.dia_eff <= 0:
            raise ValueError("'dia_eff' <= 0")
        if self.ln_prod <= 0:
            raise ValueError("'ln_prod' <= 0")
        if self.thk_wall <= 0:
            raise ValueError("'thk_wall' <= 0")
        if self.thk_c2s <= 0:
            raise ValueError("'thk_c2s' <= 0")


@dataclass
class CheckIncell:
    info: dict
    thk_top: float
    thk_mid: float

    def __post_init__(self):
        if self.info["shape"] == "circle":
            ShapeCircle(**self.info)
        elif self.info["shape"] == "hexagon":
            ShapeHexagon(**self.info)
        else:
            raise ValueError("Invalid 'incell info shape'")

        if self.thk_top < 0:
            raise ValueError("'thk_top' < 0")
        if self.thk_mid < 0:
            raise ValueError("'thk_mid' < 0")


@dataclass
class CheckOutcell:
    info: dict
    num_oc: int

    def __post_init__(self):
        if self.info["shape"] == "octagon":
            ShapeOctagon(**self.info)
        elif self.info["shape"] == "square":
            ShapeSquare(**self.info)
        else:
            raise ValueError("Invalid 'outcell info shape'")

        if self.num_oc < 1:
            raise ValueError("'num_oc' < 1")


@dataclass
class CheckSlit:
    thk_slit: float
    ratio_slit: int
    num_ic_lim: int

    def __post_init__(self):
        if self.thk_slit <= 0:
            raise ValueError("'thk_slit' <= 0")
        if self.ratio_slit < 2:
            raise ValueError("'ratio_slit' < 2")

        if self.num_ic_lim < 0:
            raise ValueError("'num_ic_lim' < 0")
        elif self.num_ic_lim > self.ratio_slit:
            raise ValueError("'num_ic_lim' > 'ratio_slit'")


# incell info shape


@dataclass
class ShapeCircle:
    shape: str
    dia_incell: float

    def __post_init__(self):
        if self.dia_incell <= 0:
            raise ValueError("'dia_incell' <= 0")


@dataclass
class ShapeHexagon:
    shape: str
    dia_incell: float

    def __post_init__(self):
        if self.dia_incell <= 0:
            raise ValueError("'dia_incell' <= 0")


# outcell info shape


@dataclass
class ShapeOctagon:
    shape: str
    thk_outcell: float
    thk_wall_outcell: float

    def __post_init__(self):
        if self.thk_outcell <= 0:
            raise ValueError("'thk_outcell' <= 0")
        if self.thk_wall_outcell <= 0:
            raise ValueError("'thk_wall_outcell' <= 0")


@dataclass
class ShapeSquare:
    shape: str
    thk_outcell: float
    thk_wall_outcell: float

    def __post_init__(self):
        if self.thk_outcell <= 0:
            raise ValueError("'thk_outcell' <= 0")
        if self.thk_wall_outcell <= 0:
            raise ValueError("'thk_wall_outcell' <= 0")
