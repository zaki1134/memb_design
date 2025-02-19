from dataclasses import dataclass

import numpy as np
import shapely.geometry as sg

from Utils import Parameters, regroup_by_slit, hexagon, heptagon, octagon, square


@dataclass(frozen=True)
class LayoutProcesser:
    par: Parameters

    def execute_calc(self) -> tuple[np.ndarray, np.ndarray]:
        # 初期座標, 複製, オフセット
        dupe_ic, dupe_oc = self.execute_calc_dupe()

        # 多めに複製したインセル, アウトセルをフィルタリング
        coords_outcell = self.__filter_outcell(dupe_oc)
        coords_incell = self.__filter_incell(dupe_ic, dupe_oc)

        return coords_incell, coords_outcell

    def execute_calc_dupe(self) -> tuple[np.ndarray, np.ndarray]:
        # Y=0からY+方向に配置されるインセル, アウトセルの初期座標を計算
        init_oc = self.__init_outcell()
        init_ic = self.__init_incell(init_oc)

        # 初期座標を複製
        dupe_oc = self.__duplicate_coords(init_oc)
        dupe_ic = self.__duplicate_coords(init_ic)

        # パラメータに応じてオフセット
        self.__offset_coords(dupe_oc)
        self.__offset_coords(dupe_ic)

        return dupe_ic, dupe_oc

    def __init_outcell(self) -> np.ndarray:
        """アウトセル初期座標(Y=0)を計算.
        最外径より大きめに配置

        Returns
        -------
        np.ndarray
            Shape: (N, 2)
        """
        ref_length_x = 0.5 * self.par.product.dia_outer
        cnt = np.int64(np.ceil((ref_length_x / self.par.pitch_x)))
        num = np.arange(-cnt, cnt + 1, 1)
        coords_x = num * self.par.pitch_x

        return np.column_stack((coords_x, np.zeros_like(coords_x)))

    def __init_incell(self, base_outcell: np.ndarray) -> np.ndarray:
        """インセル初期座標の計算.
        アウトセル座標を基準にオフセット

        Parameters
        ----------
        base_outcell : np.ndarray
            Shape: (N, 2)

        Returns
        -------
        np.ndarray
            Shape: (N, 2)
        """
        res = np.tile(base_outcell, (self.par.slit.ratio_slit, 1, 1))

        offset_y = np.arange(0, self.par.pitch_y * self.par.slit.ratio_slit, self.par.pitch_y)
        offset_y += self.par.thk_i2o

        offset_mat = np.zeros(res.shape)
        offset_mat[::2, :, 0] += 0.5 * self.par.pitch_x
        offset_mat[:, :, 1] += offset_y[:, np.newaxis]
        res += offset_mat

        return np.concatenate(res)

    def __duplicate_coords(self, coords: np.ndarray) -> np.ndarray:
        """セル座標をスリットの数だけ複製

        Parameters
        ----------
        coords : np.ndarray
            Shape: (N, 2)

        Returns
        -------
        np.ndarray
            Shape: (N, 2)
        """
        cnt = np.int64(np.ceil(self.par.lim_slit / self.par.pitch_slit))
        num = np.arange(-cnt, cnt + 1, 1)
        res = np.tile(coords, (num.shape[0], 1, 1))

        offset_mat = np.zeros_like(num).astype(np.float64)
        offset_mat[1::2] += 0.5 * self.par.pitch_x if self.par.slit.ratio_slit % 2 == 0 else 0.0
        offset_mat = np.column_stack([offset_mat, num * self.par.pitch_slit])
        res += offset_mat[:, np.newaxis]

        return np.concatenate(res)

    def __offset_coords(self, coords: np.ndarray) -> None:
        """座標をオフセット.
        offset_x = True ならX方向に0.5*pitch_x.
        offset_y = True ならY方向に0.5*pitch_slit

        Parameters
        ----------
        coords : np.ndarray
            Shape: (N, 2)
        """
        if self.par.product.offset_x:
            coords[:, 0] += 0.5 * self.par.pitch_x
        if self.par.product.offset_y:
            coords[:, 1] += 0.5 * self.par.pitch_slit

    def __filter_outcell(self, coords_outcell: np.ndarray) -> np.ndarray:
        """アウトセル座標のフィルタリング.
        dia_eff内側に収まるセルを抽出

        Parameters
        ----------
        coords_outcell : np.ndarray
            Shape: (N, 2)

        Returns
        -------
        np.ndarray
            Shape: (N, 2)
        """

        def check_octagon(x: float, y: float, dia_eff: sg.Polygon) -> bool:
            vert = octagon(
                self.par.thk_outcell_x,
                self.par.outcell.info.thk_outcell,
                self.par.chamfer_x,
                self.par.chamfer_y,
                (x, y),
            )
            return sg.Polygon(vert).within(dia_eff)

        def check_square(x: float, y: float, dia_eff: sg.Polygon) -> bool:
            vert = square(
                self.par.thk_outcell_x,
                self.par.outcell.info.thk_outcell,
                (x, y),
            )
            return sg.Polygon(vert).within(dia_eff)

        dia_eff = sg.Point(0, 0).buffer(0.5 * self.par.product.dia_eff)
        if self.par.outcell.info.shape == "octagon":
            return np.array([(x, y) for x, y in coords_outcell if check_octagon(x, y, dia_eff)])
        elif self.par.outcell.info.shape == "square":
            return np.array([(x, y) for x, y in coords_outcell if check_square(x, y, dia_eff)])
        else:
            raise ValueError("Invalid outcell shape")

    def __filter_incell(self, coords_incell: np.ndarray, coords_outcell: np.ndarray) -> np.ndarray:
        """インセル座標のフィルタリング.
        dia_eff内側に収まるセルを抽出

        Parameters
        ----------
        coords_incell : np.ndarray
            Shape: (N, 2)
        coords_outcell : np.ndarray
            Shape: (N, 2)

        Returns
        -------
        np.ndarray
            Shape: (N, 2)
        """

        def check_circle(x: float, y: float, dia_eff: sg.Polygon) -> bool:
            return sg.Point(x, y).buffer(self.par.incell.info.dia_incell).within(dia_eff)

        def check_hexagon(x: float, y: float, dia_eff: sg.Polygon) -> bool:
            vert = hexagon(self.par.incell.info.dia_incell, (x, y))
            return sg.Polygon(vert).within(dia_eff)

        def check_heptagon(x: float, y: float, rot_angle: float, dia_eff: sg.Polygon) -> bool:
            vert = heptagon(self.par.incell.info.dia_incell, rot_angle, (x, y))
            return sg.Polygon(vert).within(dia_eff)

        dia_eff = sg.Point(0, 0).buffer(0.5 * self.par.product.dia_eff)
        if self.par.incell.info.shape == "circle":
            return np.array([(x, y) for x, y in coords_incell if check_circle(x, y, dia_eff)])
        elif self.par.incell.info.shape == "hexagon":
            yc, yp, ym = regroup_by_slit(self.par.thk_i2o, coords_incell, coords_outcell)
            hex = np.array([(x, y) for x, y in yc if check_hexagon(x, y, dia_eff)])
            hep_0 = np.array([(x, y) for x, y in yp if check_heptagon(x, y, 0, dia_eff)])
            hep_1 = np.array([(x, y) for x, y in ym if check_heptagon(x, y, 180, dia_eff)])
            return np.vstack([hex, hep_0, hep_1])
        else:
            raise ValueError("Invalid incell shape")
