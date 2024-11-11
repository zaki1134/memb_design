# type hints
from typing import Tuple

import pandas as pd
import numpy as np


class DataEditor:
    colum_names = ("unit", "x", "y", "quadrant")

    def __init__(self) -> None:
        self.__data = pd.DataFrame(columns=self.colum_names)

    def get_data(self) -> pd.DataFrame:
        return self.__data

    def set_data(self, unit: np.ndarray, x: np.ndarray, y: np.ndarray, quadrant: np.ndarray) -> None:
        # Check if all arrays have the same length
        if not (unit.shape[0] == x.shape[0] == y.shape[0] == quadrant.shape[0]):
            raise ValueError("All input arrays must have the same length.")

        # Check if all arrays are 1-dimensional
        if not (unit.ndim == x.ndim == y.ndim == quadrant.ndim == 1):
            raise ValueError("All input arrays must be 1-dimensional.")

        #
        add_data = {
            self.colum_names[0]: unit,
            self.colum_names[1]: x,
            self.colum_names[2]: y,
            self.colum_names[3]: quadrant,
        }
        add_df = pd.DataFrame(add_data, columns=self.colum_names)

        #
        if not self.__data.empty:
            self.__data = pd.concat([self.__data, add_df], ignore_index=True)
        else:
            self.__data = add_df


class Quadrant:
    tiny_length = 1.0e-3

    def __init__(self) -> None:
        self.__info = DataEditor()

    def proc(self, coords: np.ndarray, unit: str) -> pd.DataFrame:
        #
        main, center, xdir, ydir = self._classification_to_q1(coords)

        #
        if not center.shape[0] == 0:
            self._set_info(center, [1], unit)

        #
        if not xdir.shape[0] == 0:
            self._set_info(xdir, [1, 2], unit)

        #
        if not ydir.shape[0] == 0:
            self._set_info(ydir, [1, 4], unit)

        #
        if not main.shape[0] == 0:
            self._set_info(main, [1, 2, 3, 4], unit)

        return self.get_info()

    def get_info(self) -> pd.DataFrame:
        return self.__info.get_data()

    def _set_info(self, src: np.ndarray, num_quad: list[int], unit: str) -> None:
        quads = np.tile(num_quad, src.shape[0])
        units = np.repeat([unit], quads.shape[0])
        coords = np.repeat(src, len(num_quad), axis=0)
        self.__info.set_data(units, coords[:, 0], coords[:, 1], quads)

    def _classification_to_q1(self, coords: np.ndarray) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        _ = self._filter_q1(coords)
        center = self._filter_center(_)
        xdir = self._filter_xdir(_)
        ydir = self._filter_ydir(_)
        main = self._extract_coords(_, np.vstack([center, xdir, ydir]))

        return main, center, xdir, ydir

    def _filter_q1(self, coords: np.ndarray) -> np.ndarray:
        mask1 = -self.tiny_length <= coords[:, 0]
        mask2 = -self.tiny_length <= coords[:, 1]
        return np.copy(coords[mask1 & mask2])

    def _filter_center(self, coords: np.ndarray) -> np.ndarray:
        distances = np.linalg.norm(coords, axis=1)
        return np.copy(coords[distances <= self.tiny_length])

    def _filter_xdir(self, coords: np.ndarray) -> np.ndarray:
        mask1 = self.tiny_length <= coords[:, 0]
        mask2 = np.abs(coords[:, 1]) <= self.tiny_length
        return np.copy(coords[mask1 & mask2])

    def _filter_ydir(self, coords: np.ndarray) -> np.ndarray:
        mask1 = np.abs(coords[:, 0]) <= self.tiny_length
        mask2 = self.tiny_length <= coords[:, 1]
        return np.copy(coords[mask1 & mask2])

    def _extract_coords(self, src: np.ndarray, trg: np.ndarray) -> np.ndarray:
        mask = ~(src[:, None] == trg).all(axis=2).any(axis=1)
        return np.copy(src[mask])
