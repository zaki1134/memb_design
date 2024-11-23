from dataclasses import dataclass


@dataclass(frozen=True)
class Dimensinons:
    shrinkage_rate: float
    offset_x: bool
    offset_y: bool

    def __post_init__(self) -> None:
        self.__type_check()
        self.__value_check()

    def __type_check(self) -> None:
        name = self.__class__.__name__
        if not isinstance(self.shrinkage_rate, float):
            raise TypeError(f"{name}: 'shrinkage_rate' must be a float")
        if not isinstance(self.offset_x, bool):
            raise TypeError(f"{name}: 'offset_x' must be a boolean")
        if not isinstance(self.offset_y, bool):
            raise TypeError(f"{name}: 'offset_y' must be a boolean")

    def __value_check(self) -> None:
        name = self.__class__.__name__
        if self.shrinkage_rate <= 0:
            raise ValueError(f"{name}: 'shrinkage_rate' <= 0")


@dataclass(frozen=True)
class Product:
    dia_land_out: float
    dia_land: float
    ln_prod: float
    thk_c2s: float

    def __post_init__(self) -> None:
        self.__type_check()
        self.__value_check()

    def __type_check(self) -> None:
        name = self.__class__.__name__
        if not isinstance(self.dia_land_out, float):
            raise TypeError(f"{name}: 'dia_land_out' must be a float")
        if not isinstance(self.dia_land, float):
            raise TypeError(f"{name}: 'dia_land' must be a float")
        if not isinstance(self.ln_prod, float):
            raise TypeError(f"{name}: 'ln_prod' must be a float")
        if not isinstance(self.thk_c2s, float):
            raise TypeError(f"{name}: 'thk_c2s' must be a float")

    def __value_check(self) -> None:
        name = self.__class__.__name__
        if self.dia_land_out <= 0:
            raise ValueError(f"{name}: 'dia_land_out' <= 0")
        if self.dia_land <= 0:
            raise ValueError(f"{name}: 'dia_land' <= 0")
        if self.ln_prod <= 0:
            raise ValueError(f"{name}: 'ln_prod' <= 0")
        if self.thk_c2s <= 0:
            raise ValueError(f"{name}: 'thk_c2s' <= 0")


@dataclass(frozen=True)
class Incell:
    shape: str
    info: float
    thk_top: float
    thk_mid: float
    thk_wall: float

    def __post_init__(self) -> None:
        self.__type_check()
        self.__value_check()

    def __type_check(self) -> None:
        name = self.__class__.__name__
        if not isinstance(self.shape, str):
            raise TypeError(f"{name}: 'shape' must be a str")

        if isinstance(self.info, dict):
            if self.shape == "circle":
                ShapeCircle(**self.info)
        else:
            raise TypeError(f"{name}: 'info' must be a dict")

        if not isinstance(self.thk_top, float):
            raise TypeError(f"{name}: 'thk_top' must be a float")
        if not isinstance(self.thk_mid, float):
            raise TypeError(f"{name}: 'thk_mid' must be a float")
        if not isinstance(self.thk_wall, float):
            raise TypeError(f"{name}: 'thk_wall' must be a float")

    def __value_check(self) -> None:
        name = self.__class__.__name__
        if self.thk_top < 0:
            raise ValueError(f"{name}: 'thk_top' < 0")
        if self.thk_mid < 0:
            raise ValueError(f"{name}: 'thk_mid' < 0")
        if self.thk_wall <= 0:
            raise ValueError(f"{name}: 'thk_wall' <= 0")


@dataclass(frozen=True)
class ShapeCircle:
    dia_incell: float

    def __post_init__(self) -> None:
        self.__type_check()
        self.__value_check()

    def __type_check(self) -> None:
        name = self.__class__.__name__
        if not isinstance(self.dia_incell, float):
            raise TypeError(f"{name}: 'dia_incell' must be a float")

    def __value_check(self) -> None:
        name = self.__class__.__name__
        if self.dia_incell <= 0:
            raise ValueError(f"{name}: 'dia_incell' <= 0")


@dataclass(frozen=True)
class Outcell:
    shape: str
    info: float

    def __post_init__(self) -> None:
        self.__type_check()

    def __type_check(self) -> None:
        name = self.__class__.__name__
        if not isinstance(self.shape, str):
            raise TypeError(f"{name}: 'shape' must be a str")

        if isinstance(self.info, dict):
            if self.shape == "octagon":
                ShapeOctagon(**self.info)
        else:
            raise TypeError(f"{name}: 'info' must be a dict")


@dataclass(frozen=True)
class ShapeOctagon:
    thk_outcell: float
    thk_wall_outcell: float
    chamfer_deg: float
    chamfer_ratio_x: float
    chamfer_ratio_y: float

    def __post_init__(self) -> None:
        self.__type_check()
        self.__value_check()

    def __type_check(self) -> None:
        name = self.__class__.__name__
        if not isinstance(self.thk_outcell, float):
            raise TypeError(f"{name}: 'thk_outcell' must be a float")
        if not isinstance(self.thk_wall_outcell, float):
            raise TypeError(f"{name}: 'thk_wall_outcell' must be a float")
        if not isinstance(self.chamfer_deg, float):
            raise TypeError(f"{name}: 'chamfer_deg' must be a float")
        if not isinstance(self.chamfer_ratio_x, float):
            raise TypeError(f"{name}: 'chamfer_ratio_x' must be a float")
        if not isinstance(self.chamfer_ratio_y, float):
            raise TypeError(f"{name}: 'chamfer_ratio_y' must be a float")

    def __value_check(self) -> None:
        name = self.__class__.__name__
        if self.thk_outcell <= 0:
            raise ValueError(f"{name}: 'thk_outcell' <= 0")
        if self.thk_wall_outcell <= 0:
            raise ValueError(f"{name}: 'thk_wall_outcell' <= 0")
        if self.chamfer_deg < 0:
            raise ValueError(f"{name}: 'chamfer_deg' < 0")
        if self.chamfer_ratio_x <= 0:
            raise ValueError(f"{name}: 'chamfer_ratio_x' <= 0")
        if self.chamfer_ratio_y <= 0:
            raise ValueError(f"{name}: 'chamfer_ratio_y' <= 0")


@dataclass(frozen=True)
class Slit:
    thk_slit: float
    ratio_slit: int

    def __post_init__(self) -> None:
        self.__type_check()
        self.__value_check()

    def __type_check(self) -> None:
        name = self.__class__.__name__
        if not isinstance(self.thk_slit, float):
            raise TypeError(f"{name}: 'thk_slit' must be a float")
        if not isinstance(self.ratio_slit, int):
            raise TypeError(f"{name}: 'ratio_slit' must be a int")

    def __value_check(self) -> None:
        name = self.__class__.__name__
        if self.thk_slit <= 0:
            raise ValueError(f"{name}: 'thk_slit' <= 0")
        if self.ratio_slit < 1:
            raise ValueError(f"{name}: 'ratio_slit' < 1")
