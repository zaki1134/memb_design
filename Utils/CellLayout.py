# type hints
from matplotlib.axes._axes import Axes

import numpy as np
import matplotlib.patches as patches

from Utils.PostEditor import PostEditor
from Utils import FuncCollection
from Utils import CalcPolygonVertex


class CellLayout:
    def __init__(self, **kwargs) -> None:
        self.__dict__.update(kwargs)

    def execute_calc(self):
        #
        base_oc = self._calc_init_outcell()
        base_ic = self._calc_init_incell(base_oc)

        #
        copy_oc = self._copy_coords(base_oc)
        copy_ic = self._copy_coords(base_ic)
        self._offset_coords(copy_oc)
        self._offset_coords(copy_ic)

        #
        self.coords_outcell = self._filter_outcell(copy_oc)
        self.coords_incell = self._filter_incell(copy_ic, copy_oc)

    def _calc_init_outcell(self) -> np.ndarray:
        ref_length = 0.5 * self.__dict__["dia_prod"] + 2.0 * self.__dict__["pitch_x"]
        cnt = np.int64(np.ceil((ref_length / self.__dict__["pitch_x"])))
        num = np.arange(-cnt, cnt + 1, 1)
        coords_x = num * self.__dict__["pitch_x"]

        return np.column_stack((coords_x, np.zeros_like(coords_x)))

    def _calc_init_incell(self, base_outcell: np.ndarray) -> np.ndarray:
        res = np.tile(base_outcell, (self.__dict__["ratio_slit"], 1, 1))

        offset_y = np.arange(0.0, self.__dict__["pitch_y"] * self.__dict__["ratio_slit"], self.__dict__["pitch_y"])
        offset_y += self.__dict__["thk_i2o"]

        offset_mat = np.zeros(res.shape)
        offset_mat[::2, :, 0] += 0.5 * self.__dict__["pitch_x"]
        offset_mat[:, :, 1] += offset_y[:, np.newaxis]

        res += offset_mat

        return np.concatenate(res)

    def _copy_coords(self, coords: np.ndarray) -> np.ndarray:
        cnt = np.int64(np.ceil(self.__dict__["lim_slit"] / self.__dict__["pitch_slit"]))
        num = np.arange(-cnt, cnt + 1, 1)
        res = np.tile(coords, (num.shape[0], 1, 1))

        offset_mat = np.zeros_like(num).astype(np.float64)
        offset_mat[1::2] += 0.5 * self.__dict__["pitch_x"] if self.__dict__["ratio_slit"] % 2 == 0 else 0.0
        offset_mat = np.column_stack([offset_mat, num * self.__dict__["pitch_slit"]])

        res += offset_mat[:, np.newaxis]

        return np.concatenate(res)

    def _offset_coords(self, coords: np.ndarray) -> None:
        coords[:, 0] += 0.5 * self.__dict__["pitch_x"] if self.__dict__["mode_cell"] else 0.0
        coords[:, 1] += 0.5 * self.__dict__["pitch_slit"] if self.__dict__["mode_slit"] else 0.0

    def _filter_incell(self, coords_incell: np.ndarray, coords_outcell: np.ndarray) -> np.ndarray:
        limit_radius = 0.5 * (self.__dict__["dia_prod"] - self.__dict__["dia_incell"]) - self.__dict__["thk_prod"]
        mask = np.linalg.norm(coords_incell, axis=1) < limit_radius

        return coords_incell[mask]

    def _filter_outcell(self, coords_outcell: np.ndarray) -> np.ndarray:
        limit_radius = 0.5 * self.__dict__["dia_prod"] - self.__dict__["thk_prod"]
        mask1 = np.linalg.norm(coords_outcell, axis=1) < limit_radius
        mask2 = np.abs(coords_outcell[:, 1]) < self.__dict__["lim_slit"]
        coords = coords_outcell[mask1 & mask2]

        vertex = CalcPolygonVertex.octagon(self.__dict__["thk_cc"], self.__dict__["thk_x1"], self.__dict__["thk_y1"])
        coords = FuncCollection.filter_polygon(limit_radius, vertex, coords)

        return coords


class CircleOctagon(CellLayout, PostEditor):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def execute_post(self, export_keys: tuple) -> None:
        _ = self.proc_draw(export_keys, self.coords_incell, self.coords_outcell)


class HexgonOctagon(CellLayout, PostEditor):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def _filter_incell(self, coords_incell: np.ndarray, coords_outcell: np.ndarray) -> np.ndarray:
        #
        radius_incircle = 0.5 * self.__dict__["dia_incell"]
        limit_radius = 0.5 * self.__dict__["dia_prod"] - self.__dict__["thk_prod"]

        #
        coords_hex_hep = FuncCollection.regroup_by_slit(self.__dict__["thk_i2o"], coords_incell, coords_outcell)

        #
        hex = CalcPolygonVertex.hexagon(radius_incircle)
        self.coords_hex = FuncCollection.filter_polygon(limit_radius, hex, coords_hex_hep[0])

        #
        hep_top = CalcPolygonVertex.heptagon(radius_incircle)
        self.coords_hep_top = FuncCollection.filter_polygon(limit_radius, hep_top, coords_hex_hep[1])

        #
        hep_btm = CalcPolygonVertex.heptagon(radius_incircle, 180.0)
        self.coords_hep_btm = FuncCollection.filter_polygon(limit_radius, hep_btm, coords_hex_hep[2])

        return np.vstack([self.coords_hex, self.coords_hep_top, self.coords_hep_btm])

    def _draw_incell(self, ax: Axes, coords_incell: np.ndarray) -> None:
        #
        thk_mem = self.__dict__["thk_top"] + self.__dict__["thk_mid"] + self.__dict__["thk_bot"]
        radius_incircle = 0.5 * self.__dict__["dia_incell"] - thk_mem

        #
        hex = CalcPolygonVertex.hexagon(radius_incircle)
        hex_mat = self.coords_hex + hex[:, np.newaxis]
        hex_mat = np.transpose(hex_mat, (1, 0, 2))
        poly_hex = [patches.Polygon(vertex, facecolor="#4F81BD") for vertex in hex_mat]
        [ax.add_patch(polygon) for polygon in poly_hex]

        #
        hep_top = CalcPolygonVertex.heptagon(radius_incircle)
        hep_top_mat = self.coords_hep_top + hep_top[:, np.newaxis]
        hep_top_mat = np.transpose(hep_top_mat, (1, 0, 2))
        hep_top_poly = [patches.Polygon(vertex, facecolor="#4F81BD") for vertex in hep_top_mat]
        [ax.add_patch(polygon) for polygon in hep_top_poly]

        #
        hep_btm = CalcPolygonVertex.heptagon(radius_incircle, 180.0)
        hep_btm_mat = self.coords_hep_btm + hep_btm[:, np.newaxis]
        hep_btm_mat = np.transpose(hep_btm_mat, (1, 0, 2))
        hep_btm_poly = [patches.Polygon(vertex, facecolor="#4F81BD") for vertex in hep_btm_mat]
        [ax.add_patch(polygon) for polygon in hep_btm_poly]

    def _calc_params(self, export_keys: tuple, coords_incell: np.ndarray, coords_outcell: np.ndarray) -> None:
        #
        thk_mem = self.__dict__["thk_top"] + self.__dict__["thk_mid"] + self.__dict__["thk_bot"]
        radius_incircle = self.__dict__["dia_incell"] - 2.0 * thk_mem

        #
        hex = CalcPolygonVertex.hexagon(radius_incircle)
        area_hex = FuncCollection.calc_polygon_area(hex)
        peri_hex = FuncCollection.calc_polygon_perimeter(hex)
        total_area_hex = area_hex * self.coords_hex.shape[0]
        total_peri_hex = peri_hex * self.coords_hex.shape[0]

        #
        hep = CalcPolygonVertex.heptagon(radius_incircle)
        area_hep = FuncCollection.calc_polygon_area(hep)
        peri_hep = FuncCollection.calc_polygon_perimeter(hep)
        total_area_hep = area_hep * (self.coords_hep_top.shape[0] + self.coords_hep_btm.shape[0])
        total_peri_hep = peri_hep * (self.coords_hep_top.shape[0] + self.coords_hep_btm.shape[0])

        #
        area_prod = 0.25 * (np.pi * self.__dict__["dia_prod"] ** 2.0)
        total_area_incell = total_area_hex + total_area_hep
        area_mem = (total_peri_hex + total_peri_hep) * self.__dict__["ln_prod"]

        #
        self.export_params = {key: self.__dict__[key] for key in export_keys}
        self.export_params["N(incell)"] = coords_incell.shape[0]
        self.export_params["N(outcell)"] = coords_outcell.shape[0]
        self.export_params["N(slit)"] = np.unique(coords_outcell[:, 1]).shape[0]
        self.export_params["A(membrane)"] = area_mem
        self.export_params["A(incell)"] = total_area_incell
        self.export_params["R_A(incell/prod)"] = (total_area_incell / area_prod) * 100.0

    def execute_post(self, export_keys: tuple) -> None:
        _ = self.proc_draw(export_keys, self.coords_incell, self.coords_outcell)
