# type hints
from typing import Tuple
from matplotlib.axes._axes import Axes

import re

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.gridspec import GridSpec

from Utils import PolygonVertex
from Utils import FuncCollection
from PRE.CellParameters import CellParameters


class PostProcessor:
    def __init__(self, instance: CellParameters) -> None:
        self.params = instance

    def proc_draw(self, export_keys: tuple, coords_incell: np.ndarray, coords_outcell: np.ndarray) -> Axes:
        #
        ax1, ax2 = self._set_axes()

        #
        dia = self.params.dia_prod
        self._draw_product(ax1, dia, facecolor="None")
        self._draw_product(ax1, dia, transparency=0.5)
        dia += -2.0 * self.params.thk_prod
        self._draw_product(ax1, dia, facecolor="None", transparency=1.0, linestyle="dashed")

        #
        self._draw_slit(ax1, coords_outcell)
        self._draw_incell(ax1, coords_incell)
        self._draw_outcell(ax1, coords_outcell)

        #
        self._calc_params(export_keys, coords_incell, coords_outcell)
        self._set_table(ax2)

        #
        coords = FuncCollection.regroup_by_slit(self.params.thk_i2o, coords_incell, coords_outcell)
        self.dummy_oc = self._dummy_xdir(coords_outcell)
        self.dummy_ic_main_x = self._dummy_xdir(coords[0])
        self.dummy_ic_top = self._dummy_xdir(coords[1])
        self.dummy_ic_btm = self._dummy_xdir(coords[2])
        dummy_ic = np.vstack([self.dummy_ic_main_x, self.dummy_ic_top, self.dummy_ic_btm])
        self.dummy_ic_main_y = self._dummy_ydir(coords_incell, dummy_ic)

        return ax1

    def _set_axes(self, fig_x: int = 1920, fig_y: int = 1080, fig_dpi: int = 100) -> Tuple[Axes, Axes]:
        #
        fig = plt.figure(figsize=(fig_x / fig_dpi, fig_y / fig_dpi), dpi=fig_dpi)
        fig.subplots_adjust(left=0.025, right=0.99, bottom=0.025, top=0.99)

        #
        gs = GridSpec(1, 10)
        ss1 = gs.new_subplotspec((0, 0), colspan=7)
        ss2 = gs.new_subplotspec((0, 8), colspan=2)

        #
        ax1 = plt.subplot(ss1)
        ax1.grid(linewidth=0.2)
        ax1.set_axisbelow(True)
        ax1.set_aspect("equal", adjustable="datalim")

        #
        scale = 0.52 * self.params.dia_prod
        ax1.set_xlim(-scale, scale)
        ax1.set_ylim(-scale, scale)

        #
        ax2 = plt.subplot(ss2)
        ax2.axis("off")

        return ax1, ax2

    def _draw_product(
        self,
        ax: Axes,
        diameter: float,
        facecolor: str = "#BFBFBF",
        transparency: float = 1.0,
        linestyle: str = "solid",
    ) -> None:
        circle = patches.Circle(
            xy=(0.0, 0.0),
            radius=0.5 * diameter,
            facecolor=facecolor,
            alpha=transparency,
            edgecolor="black",
            linestyle=linestyle,
        )
        ax.add_patch(circle)

    def _draw_slit(self, ax: Axes, coords_slit: np.ndarray) -> None:
        radius_prod = 0.5 * self.params.dia_prod
        thk_slit = self.params.thk_slit
        slit_vetex = [PolygonVertex.slit(radius_prod, thk_slit, y) for y in coords_slit[:, 1]]
        polygons = [patches.Polygon(slit, facecolor="#97B6D8", linewidth=0, alpha=0.1) for slit in slit_vetex]
        [ax.add_patch(polygon) for polygon in polygons]

    def _draw_incell(self, ax: Axes, coords_incell: np.ndarray) -> None:
        thk_mem = self.params.thk_top + self.params.thk_mid + self.params.thk_bot
        radius = 0.5 * self.params.dia_incell - 2.0 * thk_mem
        circles = [patches.Circle(xy, radius, facecolor="#4F81BD") for xy in coords_incell]
        [ax.add_patch(circle) for circle in circles]

    def _draw_outcell(self, ax: Axes, coords_outcell: np.ndarray) -> None:
        vertex = PolygonVertex.octagon(self.params.thk_cc, self.params.thk_x1, self.params.thk_y1)
        oct_mat = coords_outcell + vertex[:, np.newaxis]
        oct_mat = np.transpose(oct_mat, (1, 0, 2))
        polygons = [patches.Polygon(vertex, facecolor="#76913C", linewidth=0) for vertex in oct_mat]
        [ax.add_patch(polygon) for polygon in polygons]

    def _calc_params(self, export_keys: tuple, coords_incell: np.ndarray, coords_outcell: np.ndarray) -> None:
        #
        thk_mem = self.params.thk_top + self.params.thk_mid + self.params.thk_bot
        diameter_effective = self.params.dia_incell - 2.0 * thk_mem
        area_incell = 0.25 * (np.pi * diameter_effective**2.0)
        area_prod = 0.25 * (np.pi * self.params.dia_prod**2.0)
        area_mem = np.pi * diameter_effective * self.params.ln_prod * coords_incell.shape[0]
        total_area_incell = area_incell * coords_incell.shape[0]

        #
        self.export_params = {key: getattr(self.params, key) for key in export_keys}
        self.export_params["N(incell)"] = coords_incell.shape[0]
        self.export_params["N(outcell)"] = coords_outcell.shape[0]
        self.export_params["N(slit)"] = np.unique(coords_outcell[:, 1]).shape[0]
        self.export_params["A(membrane)"] = area_mem
        self.export_params["A(incell)"] = total_area_incell
        self.export_params["R_A(incell/prod)"] = (total_area_incell / area_prod) * 100.0

    def _set_table(self, ax: Axes) -> None:
        #
        params_str = {}
        for k, v in self.export_params.items():
            if re.compile(r"^dia_").match(k) or re.compile(r"^thk_").match(k) or re.compile(r"^ln_").match(k):
                params_str[k] = f"{v:.3f} [mm]"
            elif re.compile(r"^A\(").match(k):
                params_str[k] = f"{v:.3e} [mm2]"
            elif re.compile(r"^R_A\(").match(k):
                params_str[k] = f"{v:.2f} [%]"
            else:
                params_str[k] = f"{v}"

        #
        key = list(params_str.keys())
        val = [[v] for v in params_str.values()]
        tbl = ax.table(cellText=val, rowLabels=key, loc="center")
        tbl.set_fontsize(16)
        [cell.set_height(1 / len(val)) for _, cell in tbl.get_celld().items()]

    def _dummy_xdir(self, coords: np.ndarray, cnt: int = 10) -> np.ndarray:
        #
        coords_y = np.unique(coords[:, 1])
        masks = np.array([np.isclose(coords[:, 1], y) for y in coords_y])
        right = np.array([coords[mask][np.argmax(coords[mask][:, 0])] for mask in masks])
        left = np.array([coords[mask][np.argmin(coords[mask][:, 0])] for mask in masks])

        #
        num = np.arange(1, cnt + 1, 1)
        coords_right = np.tile(right, (cnt, 1)).reshape(cnt, coords_y.shape[0], 2)
        offset_x = num * self.params.pitch_x
        offset_mat = np.column_stack([offset_x, np.zeros_like(offset_x)])
        coords_right += offset_mat[:, np.newaxis]

        #
        coords_left = np.tile(left, (cnt, 1)).reshape(cnt, coords_y.shape[0], 2)
        offset_x = num * -self.params.pitch_x
        offset_mat = np.column_stack([offset_x, np.zeros_like(offset_x)])
        coords_left += offset_mat[:, np.newaxis]

        return np.vstack([np.concatenate(coords_right), np.concatenate(coords_left)])

    def _dummy_ydir(self, valid: np.ndarray, invalid: np.ndarray, cnt: int = 10) -> np.ndarray:
        #
        y_max = np.max(valid[:, 1])
        mask1 = np.isclose(valid[:, 1], y_max)
        mask2 = np.isclose(invalid[:, 1], y_max)
        ref_top = np.vstack([valid[mask1], invalid[mask2]])

        #
        top = np.tile(ref_top, (cnt, 1)).reshape(cnt, ref_top.shape[0], 2)
        num = np.arange(1, cnt + 1, 1)
        offset_y = num * self.params.pitch_y
        offset_mat = np.zeros(top.shape)
        offset_mat[::2, :, 0] += 0.5 * self.params.pitch_x
        offset_mat[:, :, 1] += offset_y[:, np.newaxis]
        coords_top = top + offset_mat

        #
        y_min = np.min(valid[:, 1])
        mask1 = np.isclose(valid[:, 1], y_min)
        mask2 = np.isclose(invalid[:, 1], y_min)
        ref_btm = np.vstack([valid[mask1], invalid[mask2]])

        #
        btm = np.tile(ref_btm, (cnt, 1)).reshape(cnt, ref_btm.shape[0], 2)
        num = np.arange(1, cnt + 1, 1)
        offset_y = num * -self.params.pitch_y
        offset_mat = np.zeros(btm.shape)
        offset_mat[::2, :, 0] += 0.5 * self.params.pitch_x
        offset_mat[:, :, 1] += offset_y[:, np.newaxis]
        coords_btm = btm + offset_mat

        return np.vstack([np.concatenate(coords_top), np.concatenate(coords_btm)])
