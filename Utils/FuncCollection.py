import numpy as np


def regroup_by_slit(
    thk_i2o: float,
    coords_incell: np.ndarray,
    coords_outcell: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """インセル座標をグループ分け.
    yp : スリット上側の座標
    ym : スリット下側の座標
    yc : yp, ymに含まれない座標

    Parameters
    ----------
    thk_i2o : float
    coords_incell : np.ndarray
        Shape: (N, 2)
    coords_outcell : np.ndarray
        Shape: (N, 2)

    Returns
    -------
    tuple[np.ndarray, np.ndarray, np.ndarray]
        Shape: (N, 2) = (yc, yp, ym)
    """
    y_unit = np.unique(coords_outcell[:, 1])
    y_plus = y_unit + thk_i2o
    y_minus = y_unit - thk_i2o

    coords_plus = coords_incell[np.any(np.isclose(coords_incell[:, 1][:, None], y_plus), axis=1)]
    coords_minus = coords_incell[np.any(np.isclose(coords_incell[:, 1][:, None], y_minus), axis=1)]

    mask1 = ~(coords_incell[:, None] == coords_plus).all(axis=2).any(axis=1)
    mask2 = ~(coords_incell[:, None] == coords_minus).all(axis=2).any(axis=1)
    coords = coords_incell[mask1 & mask2]

    return coords, coords_plus, coords_minus
