import numpy as np


def slit(radius_prod: float, thk_slit: float, y: float) -> np.ndarray:
    #
    ref_points_y = np.array([y - 0.5 * thk_slit, y + 0.5 * thk_slit])
    ref_points_x = radius_prod * np.cos(np.arcsin(ref_points_y / radius_prod))
    ref_angles = np.arctan2(ref_points_y, ref_points_x)

    #
    angles = np.linspace(np.min(ref_angles), np.max(ref_angles), 10)
    coordinates = radius_prod * np.column_stack((np.cos(angles), np.sin(angles)))

    #
    copied_coordinates = np.copy(coordinates)
    copied_coordinates[:, 0] *= -1.0
    coordinates = np.vstack([coordinates, copied_coordinates])

    #
    sorted_angles = np.arctan2(coordinates[:, 1], coordinates[:, 0])
    sorted_angles[sorted_angles < 0] += 2 * np.pi
    slit_points = coordinates[np.argsort(sorted_angles)]

    return slit_points


def hexagon(radius_incircle: float) -> np.ndarray:
    #
    circumscribed_radius = radius_incircle / np.cos(np.pi / 6)

    #
    angles = np.arange(-np.pi / 6, 3 * np.pi / 2, np.pi / 3)

    #
    hex_points = circumscribed_radius * np.column_stack((np.cos(angles), np.sin(angles)))

    return hex_points


def heptagon(radius_incircle: float, rot_angle: float = 0.0) -> np.ndarray:
    #
    circumscribed_radius = radius_incircle / np.cos(np.pi / 6)

    #
    angles_5_points = np.arange(-np.pi / 6, 4 * np.pi / 3, np.pi / 3)
    hep_points = circumscribed_radius * np.column_stack((np.cos(angles_5_points), np.sin(angles_5_points)))

    #
    angles_2_points = np.array([4 * np.pi / 3, 5 * np.pi / 3])
    dummy_points = radius_incircle * np.column_stack((np.cos(angles_2_points), np.sin(angles_2_points)))

    #
    hep_points = np.vstack([hep_points, dummy_points])

    #
    radian = np.deg2rad(rot_angle)
    rot_mat = np.array([[np.cos(radian), -np.sin(radian)], [np.sin(radian), np.cos(radian)]])
    hep_points = np.dot(hep_points, rot_mat)

    return hep_points


def octagon(thk_cc: float, thk_x1: float, thk_y1: float) -> np.ndarray:
    #
    oct_points = np.array(
        [
            (thk_x1 + thk_cc, thk_y1),
            (thk_x1, thk_y1 + thk_cc),
            (-thk_x1, thk_y1 + thk_cc),
            (-(thk_x1 + thk_cc), thk_y1),
        ]
    )

    #
    rot_mat = np.array([[np.cos(np.pi), -np.sin(np.pi)], [np.sin(np.pi), np.cos(np.pi)]])
    dummy_points = np.dot(oct_points, rot_mat)

    return np.vstack([oct_points, dummy_points])
