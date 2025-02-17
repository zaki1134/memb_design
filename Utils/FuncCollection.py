import numpy as np


def regroup_by_slit(
    thk_i2o: float,
    coords_incell: np.ndarray,
    coords_outcell: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    y_unit = np.unique(coords_outcell[:, 1])
    y_top = y_unit + thk_i2o
    y_btm = y_unit - thk_i2o

    coords_top = coords_incell[np.any(np.isclose(coords_incell[:, 1][:, None], y_top), axis=1)]
    coords_btm = coords_incell[np.any(np.isclose(coords_incell[:, 1][:, None], y_btm), axis=1)]

    mask1 = ~(coords_incell[:, None] == coords_top).all(axis=2).any(axis=1)
    mask2 = ~(coords_incell[:, None] == coords_btm).all(axis=2).any(axis=1)
    coords = coords_incell[mask1 & mask2]

    return coords, coords_top, coords_btm
