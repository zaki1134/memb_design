import numpy as np

from Pre.CellParameters import CellParameters
from Utils import FuncCollection
from Utils import PolygonVertex


class CellLayout:
    def __init__(self, params: CellParameters) -> None:
        self.params = params

    def _calc_init_outcell(self) -> np.ndarray:
        ref_length_x = 0.5 * self.params.dia_prod + 2.0 * self.params.pitch_x
        cnt = np.int64(np.ceil((ref_length_x / self.params.pitch_x)))
        num = np.arange(-cnt, cnt + 1, 1)
        coords_x = num * self.params.pitch_x
        return np.column_stack((coords_x, np.zeros_like(coords_x)))

    def _calc_init_incell(self, base_outcell: np.ndarray) -> np.ndarray:
        res = np.tile(base_outcell, (self.params.ratio_slit, 1, 1))

        #
        offset_y = np.arange(0, self.params.pitch_y * self.params.ratio_slit, self.params.pitch_y)
        offset_y += self.params.thk_i2o

        #
        offset_mat = np.zeros(res.shape)
        offset_mat[::2, :, 0] += 0.5 * self.params.pitch_x
        offset_mat[:, :, 1] += offset_y[:, np.newaxis]

        #
        res += offset_mat
        return np.concatenate(res)

    def _copy_coords(self, coords: np.ndarray) -> np.ndarray:
        #
        cnt = np.int64(np.ceil(self.params.lim_slit / self.params.pitch_slit))
        num = np.arange(-cnt, cnt + 1, 1)
        res = np.tile(coords, (num.shape[0], 1, 1))

        #
        offset_mat = np.zeros_like(num).astype(np.float64)
        offset_mat[1::2] += 0.5 * self.params.pitch_x if self.params.ratio_slit % 2 == 0 else 0.0
        offset_mat = np.column_stack([offset_mat, num * self.params.pitch_slit])

        #
        res += offset_mat[:, np.newaxis]
        return np.concatenate(res)

    def _offset_coords(self, coords: np.ndarray) -> None:
        if self.params.mode_cell:
            coords[:, 0] += 0.5 * self.params.pitch_x
        if self.params.mode_slit:
            coords[:, 1] += 0.5 * self.params.pitch_slit

    def _filter_incell(self, coords_incell: np.ndarray) -> np.ndarray:
        limit_radius = 0.5 * (self.params.dia_prod - self.params.dia_incell) - self.params.thk_prod
        mask = np.linalg.norm(coords_incell, axis=1) <= limit_radius
        return coords_incell[mask]

    def _filter_outcell(self, coords_outcell: np.ndarray) -> np.ndarray:
        # step1
        limit_radius = 0.5 * self.params.dia_prod - self.params.thk_prod
        mask1 = np.linalg.norm(coords_outcell, axis=1) <= limit_radius
        mask2 = np.abs(coords_outcell[:, 1]) < self.params.lim_slit
        coords = coords_outcell[mask1 & mask2]

        # step2
        vertex = PolygonVertex.octagon(
            self.params.pitch_x - self.params.thk_wall_outcell,
            self.params.thk_outcell,
            self.params.thk_x1,
            self.params.thk_y1,
        )
        coords = FuncCollection.filter_polygon(limit_radius, vertex, coords)
        return coords


class CircleOctagon(CellLayout):
    def __init__(self, params: CellParameters) -> None:
        super().__init__(params)

    def execute_calc(self) -> None:
        #
        base_oc = self.__calc_init_outcell()
        base_ic = self.__calc_init_incell(base_oc)

        #
        copy_oc = self.__copy_coords(base_oc)
        copy_ic = self.__copy_coords(base_ic)

        #
        self.__offset_coords(copy_oc)
        self.__offset_coords(copy_ic)

        #
        self.coords_outcell = self.__filter_outcell(copy_oc)
        self.coords_incell = self.__filter_incell(copy_ic)


class HexgonOctagon(CellLayout):
    def __init__(self, params: CellParameters) -> None:
        super().__init__(params)

    def execute_calc(self) -> None:
        #
        base_oc = self._calc_init_outcell()
        base_ic = self._calc_init_incell(base_oc)

        #
        copy_oc = self._copy_coords(base_oc)
        copy_ic = self._copy_coords(base_ic)

        #
        self._offset_coords(copy_oc)
        self._offset_coords(copy_ic)

        #
        self.coords_outcell = self._filter_outcell(copy_oc)
        self.coords_incell = self._filter_incell(copy_ic, self.coords_outcell)

    def _filter_incell(self, coords_incell: np.ndarray, coords_outcell: np.ndarray) -> np.ndarray:
        #
        radius_incircle = 0.5 * self.params.dia_incell
        limit_radius = 0.5 * self.params.dia_prod - self.params.thk_prod

        #
        coords_hex_hep = FuncCollection.regroup_by_slit(self.params.thk_i2o, coords_incell, coords_outcell)

        #
        vertex = PolygonVertex.hexagon(radius_incircle)
        self.coords_hex = FuncCollection.filter_polygon(limit_radius, vertex, coords_hex_hep[0])

        #
        vertex = PolygonVertex.heptagon(radius_incircle)
        self.coords_hep_top = FuncCollection.filter_polygon(limit_radius, vertex, coords_hex_hep[1])

        #
        vertex = PolygonVertex.heptagon(radius_incircle, 180.0)
        self.coords_hep_btm = FuncCollection.filter_polygon(limit_radius, vertex, coords_hex_hep[2])

        return np.vstack([self.coords_hex, self.coords_hep_top, self.coords_hep_btm])

    # def _calc_params(self, export_keys: tuple, coords_incell: np.ndarray, coords_outcell: np.ndarray) -> None:
    #     #
    #     thk_mem = self.params.thk_top + self.params.thk_mid + self.params.thk_bot
    #     radius_incircle = self.params.dia_incell - 2.0 * thk_mem

    #     #
    #     hex = PolygonVertex.hexagon(radius_incircle)
    #     area_hex = FuncCollection.calc_polygon_area(hex)
    #     peri_hex = FuncCollection.calc_polygon_perimeter(hex)
    #     total_area_hex = area_hex * self.coords_hex.shape[0]
    #     total_peri_hex = peri_hex * self.coords_hex.shape[0]

    #     #
    #     hep = PolygonVertex.heptagon(radius_incircle)
    #     area_hep = FuncCollection.calc_polygon_area(hep)
    #     peri_hep = FuncCollection.calc_polygon_perimeter(hep)
    #     total_area_hep = area_hep * (self.coords_hep_top.shape[0] + self.coords_hep_btm.shape[0])
    #     total_peri_hep = peri_hep * (self.coords_hep_top.shape[0] + self.coords_hep_btm.shape[0])

    #     #
    #     area_prod = 0.25 * (np.pi * self.params.dia_prod**2.0)
    #     total_area_incell = total_area_hex + total_area_hep
    #     area_mem = (total_peri_hex + total_peri_hep) * self.params.ln_prod

    #     #
    #     self.export_params = {key: getattr(self.params, key) for key in export_keys}
    #     self.export_params["N(incell)"] = coords_incell.shape[0]
    #     self.export_params["N(outcell)"] = coords_outcell.shape[0]
    #     self.export_params["N(slit)"] = np.unique(coords_outcell[:, 1]).shape[0]
    #     self.export_params["A(membrane)"] = area_mem
    #     self.export_params["A(incell)"] = total_area_incell
    #     self.export_params["R_A(incell/prod)"] = (total_area_incell / area_prod) * 100.0
