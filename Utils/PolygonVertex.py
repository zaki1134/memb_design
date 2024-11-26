import numpy as np


def slit(radius_prod: float, thk_slit: float, y: float) -> np.ndarray:
    """スリット形状を多角形としたときの頂点座標を計算"""
    ref_points_y = np.array([y - 0.5 * thk_slit, y + 0.5 * thk_slit])
    ref_points_x = radius_prod * np.cos(np.arcsin(ref_points_y / radius_prod))
    ref_angles = np.arctan2(ref_points_y, ref_points_x)

    angles = np.linspace(np.min(ref_angles), np.max(ref_angles), 10)
    coordinates = radius_prod * np.column_stack((np.cos(angles), np.sin(angles)))

    copied_coordinates = np.copy(coordinates)
    copied_coordinates[:, 0] *= -1.0
    coordinates = np.vstack([coordinates, copied_coordinates])

    sorted_angles = np.arctan2(coordinates[:, 1], coordinates[:, 0])
    sorted_angles[sorted_angles < 0] += 2 * np.pi
    slit_points = coordinates[np.argsort(sorted_angles)]

    return slit_points


def hexagon(radius_incircle: float) -> np.ndarray:
    """六角形の頂点座標を計算"""
    circumscribed_radius = radius_incircle / np.cos(np.pi / 6)
    angles = np.deg2rad(np.arange(-30, 330, 60))
    hex_points = circumscribed_radius * np.column_stack((np.cos(angles), np.sin(angles)))
    return hex_points


def heptagon(radius_incircle: float, rot_angle: float = 0.0) -> np.ndarray:
    """七角形の頂点座標を計算"""
    circumscribed_radius = radius_incircle / np.cos(np.pi / 6)
    angles = np.deg2rad(np.arange(-30, 270, 60))
    hex_points = circumscribed_radius * np.column_stack((np.cos(angles), np.sin(angles)))

    tmp_points = np.array(
        [
            (-radius_incircle * np.cos(np.pi / 3), -radius_incircle * np.sin(np.pi / 3)),
            (radius_incircle * np.cos(np.pi / 3), -radius_incircle * np.sin(np.pi / 3)),
        ]
    )
    res = np.vstack([hex_points, tmp_points])

    radian = np.deg2rad(rot_angle)
    rot_mat = np.array([[np.cos(radian), -np.sin(radian)], [np.sin(radian), np.cos(radian)]])
    res = np.dot(res, rot_mat)
    return res


def octagon(width: float, hight: float, x1: float, y1: float) -> np.ndarray:
    """八角形の頂点座標を計算"""
    dx = 0.5 * width
    dy = 0.5 * hight
    oct_points = np.array(
        [
            (dx, dy - y1),
            (dx - x1, dy),
            (-(dx + x1), dy),
            (-dx, dy - y1),
        ]
    )

    rot_mat = np.array([[np.cos(np.pi), -np.sin(np.pi)], [np.sin(np.pi), np.cos(np.pi)]])
    dummy_points = np.dot(oct_points, rot_mat)
    return np.vstack([oct_points, dummy_points])
