import numpy as np

from Solver import CellParameters
from Utils import FuncCollection, PolygonVertex


class Common:
    def __init__(self, params: CellParameters) -> None:
        self.params = params

    def _calc_init_outcell(self) -> np.ndarray:
        """初期アウトセル座標(Y=0)を計算.
        製品径より大きめに配置"""
        ref_length_x = 0.5 * self.params.dia_prod + 2.0 * self.params.pitch_x
        cnt = np.int64(np.ceil((ref_length_x / self.params.pitch_x)))
        num = np.arange(-cnt, cnt + 1, 1)
        coords_x = num * self.params.pitch_x
        return np.column_stack((coords_x, np.zeros_like(coords_x)))

    def _calc_init_incell(self, base_outcell: np.ndarray) -> np.ndarray:
        """初期インセル座標の計算.
        アウトセル座標を基準にオフセット"""
        res = np.tile(base_outcell, (self.params.ratio_slit, 1, 1))

        offset_y = np.arange(0, self.params.pitch_y * self.params.ratio_slit, self.params.pitch_y)
        offset_y += self.params.thk_i2o

        offset_mat = np.zeros(res.shape)
        offset_mat[::2, :, 0] += 0.5 * self.params.pitch_x
        offset_mat[:, :, 1] += offset_y[:, np.newaxis]

        res += offset_mat
        return np.concatenate(res)

    def _copy_coords(self, coords: np.ndarray) -> np.ndarray:
        """coordsをスリットの数だけコピー"""
        cnt = np.int64(np.ceil(self.params.lim_slit / self.params.pitch_slit))
        num = np.arange(-cnt, cnt + 1, 1)
        res = np.tile(coords, (num.shape[0], 1, 1))

        offset_mat = np.zeros_like(num).astype(np.float64)
        offset_mat[1::2] += 0.5 * self.params.pitch_x if self.params.ratio_slit % 2 == 0 else 0.0
        offset_mat = np.column_stack([offset_mat, num * self.params.pitch_slit])

        res += offset_mat[:, np.newaxis]
        return np.concatenate(res)

    def _offset_coords(self, coords: np.ndarray) -> None:
        """coordsをオフセット.
        mode_cell = False ならX方向に0.5*pitch_x.
        mode_slit = False ならY方向に0.5*pitch_slit"""
        if self.params.mode_cell:
            coords[:, 0] += 0.5 * self.params.pitch_x
        if self.params.mode_slit:
            coords[:, 1] += 0.5 * self.params.pitch_slit

    def _filter_incell(self, coords_incell: np.ndarray) -> np.ndarray:
        """インセル座標のフィルタリング.
        限界半径の内側にある座標を抽出"""
        limit_radius = 0.5 * (self.params.dia_prod - self.params.dia_incell) - self.params.thk_prod
        mask = np.linalg.norm(coords_incell, axis=1) <= limit_radius
        return coords_incell[mask]

    def _filter_outcell(self, coords_outcell: np.ndarray) -> np.ndarray:
        """アウトセル座標のフィルタリング.
        限界半径の内側にある座標を抽出"""
        # STEP1 限界半径より小さい座標を抽出
        limit_radius = 0.5 * self.params.dia_prod - self.params.thk_prod
        mask1 = np.linalg.norm(coords_outcell, axis=1) <= limit_radius
        mask2 = np.abs(coords_outcell[:, 1]) < self.params.lim_slit
        coords = coords_outcell[mask1 & mask2]

        # STEP2 八角形の頂点を取得し、すべての頂点が限界半径より小さい座標を抽出
        vertex = PolygonVertex.octagon(
            self.params.pitch_x - self.params.thk_wall_outcell,
            self.params.thk_outcell,
            self.params.thk_x1,
            self.params.thk_y1,
        )
        res = FuncCollection.filter_polygon(limit_radius, vertex, coords)
        return res


class CircleOctagon(Common):
    def __init__(self, params: CellParameters) -> None:
        super().__init__(params)

    def execute_calc(self) -> None:
        # Y=0からY+方向に配置されるインセル、アウトセルの初期座標を計算
        base_oc = self._calc_init_outcell()
        base_ic = self._calc_init_incell(base_oc)

        # 初期座標をコピー
        copy_oc = self._copy_coords(base_oc)
        copy_ic = self._copy_coords(base_ic)

        # mode_cell, mode_slitに応じてオフセット
        self._offset_coords(copy_oc)
        self._offset_coords(copy_ic)

        # 多めに作ったインセル、アウトセルをフィルタリング
        self.coords_outcell = self._filter_outcell(copy_oc)
        self.coords_incell = self._filter_incell(copy_ic)


class HexgonOctagon(Common):
    def __init__(self, params: CellParameters) -> None:
        super().__init__(params)

    def execute_calc(self) -> None:
        # Y=0からY+方向に配置されるインセル、アウトセルの初期座標を計算
        base_oc = self._calc_init_outcell()
        base_ic = self._calc_init_incell(base_oc)

        # 初期座標をコピー
        copy_oc = self._copy_coords(base_oc)
        copy_ic = self._copy_coords(base_ic)

        # mode_cell, mode_slitに応じてオフセット
        self._offset_coords(copy_oc)
        self._offset_coords(copy_ic)

        # 多めに作ったインセル、アウトセルをフィルタリング
        self.coords_outcell = self._filter_outcell(copy_oc)
        self.coords_incell = self._filter_incell(copy_ic, self.coords_outcell)

    def _filter_incell(self, coords_incell: np.ndarray, coords_outcell: np.ndarray) -> np.ndarray:
        """インセル座標のフィルタリング.
        六角形、七角形の頂点を取得し、すべての頂点が限界半径より小さい座標を抽出"""
        radius_incircle = 0.5 * self.params.dia_incell
        limit_radius = 0.5 * self.params.dia_prod - self.params.thk_prod

        coords_hex_hep = FuncCollection.regroup_by_slit(self.params.thk_i2o, coords_incell, coords_outcell)

        vertex = PolygonVertex.hexagon(radius_incircle)
        self.coords_hex = FuncCollection.filter_polygon(limit_radius, vertex, coords_hex_hep[0])

        vertex = PolygonVertex.heptagon(radius_incircle)
        self.coords_hep_top = FuncCollection.filter_polygon(limit_radius, vertex, coords_hex_hep[1])

        vertex = PolygonVertex.heptagon(radius_incircle, 180.0)
        self.coords_hep_btm = FuncCollection.filter_polygon(limit_radius, vertex, coords_hex_hep[2])

        return np.vstack([self.coords_hex, self.coords_hep_top, self.coords_hep_btm])
