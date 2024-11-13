import numpy as np


def filter_polygon(limit_radius: float, vertex: np.ndarray, coords: np.ndarray) -> np.ndarray:
    """多角形頂点座標が限界半径内にすべて収まる多角形中心座標を抽出する"""
    vertex_mat = coords + vertex[:, np.newaxis]
    vertex_mat = np.transpose(vertex_mat, (1, 0, 2))
    radius_mat: np.ndarray = np.linalg.norm(vertex_mat, axis=-1)
    check = radius_mat < limit_radius
    mask = np.all(check, axis=1)
    return coords[mask]


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


def calc_polygon_area(vertices: np.ndarray) -> float:
    # shoelace_formula
    xy = np.concatenate((vertices, [vertices[0]]))

    return 0.5 * np.abs(np.dot(xy[:, 0], np.roll(xy[:, 1], -1)) - np.dot(xy[:, 1], np.roll(xy[:, 0], -1)))


def calc_polygon_perimeter(vertices: np.ndarray) -> float:
    xy = np.roll(vertices, -1, axis=0)
    edge_vectors = xy - vertices

    return np.sum(np.linalg.norm(edge_vectors, axis=1))
