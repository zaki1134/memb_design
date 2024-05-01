# import sys
# from pathlib import Path, WindowsPath
# from datetime import datetime

# import pandas as pd

from Utils.CellLayout import CircleOctagon
from Utils.CellLayout import HexgonOctagon


# ax1.scatter(self.dummy_oc[:, 0], self.dummy_oc[:, 1], c="green")
# ax1.scatter(self.dummy_ic_main_y[:, 0], self.dummy_ic_main_y[:, 1], c="navy")
# ax1.scatter(self.dummy_ic_main_x[:, 0], self.dummy_ic_main_x[:, 1], c="blue")
# ax1.scatter(self.dummy_ic_top[:, 0], self.dummy_ic_top[:, 1], c="cyan")
# ax1.scatter(self.dummy_ic_btm[:, 0], self.dummy_ic_btm[:, 1], c="orange")


def main() -> None:
    sw = 0
    if sw == 0:
        inp = {
            "shape_incell": "circle",
            "shape_outcell": "octagon",
            "dia_incell": 2.000,
            "thk_bot": 0.000,
            "thk_mid": 0.000,
            "thk_top": 0.000,
            "thk_wall": 0.500,
            "thk_c2s": 0.500,
            "dia_prod": 60.000,
            "thk_prod": 1.000,
            "thk_outcell": 1.000,
            "thk_wall_outcell": 0.500,
            "thk_slit": 0.500,
            "ratio_slit": 3,
            "mode_cell": False,
            "mode_slit": False,
            "ln_prod": 1000.000,
            "pitch_x": 2.5000e00,
            "pitch_y": 2.1651e00,
            "pitch_slit": 8.3301e00,
            "thk_i2o": 2.0000e00,
            "thk_cc": 3.0000e-01,
            "thk_x1": 7.0000e-01,
            "thk_y1": 2.0000e-01,
            "lim_slit": 2.6000e01,
        }
        obj = CircleOctagon(**inp)
    else:
        inp = {
            "shape_incell": "hexagon",
            "shape_outcell": "octagon",
            "dia_incell": 2.000,
            "thk_bot": 0.000,
            "thk_mid": 0.000,
            "thk_top": 0.000,
            "thk_wall": 0.500,
            "thk_c2s": 0.500,
            "dia_prod": 60.000,
            "thk_prod": 1.000,
            "thk_outcell": 1.000,
            "thk_wall_outcell": 0.500,
            "thk_slit": 0.500,
            "ratio_slit": 3,
            "mode_cell": False,
            "mode_slit": False,
            "ln_prod": 1000.000,
            "pitch_x": 2.5000e00,
            "pitch_y": 2.1651e00,
            "pitch_slit": 8.0622e00,
            "thk_i2o": 1.8660e00,
            "thk_cc": 3.0000e-01,
            "thk_x1": 7.0000e-01,
            "thk_y1": 2.0000e-01,
            "lim_slit": 2.5979e01,
        }
        obj = HexgonOctagon(**inp)

    export_keys = (
        "dia_incell",
        "thk_bot",
        "thk_mid",
        "thk_top",
        "thk_wall",
        "thk_c2s",
        "dia_prod",
        "thk_prod",
        "thk_outcell",
        "thk_wall_outcell",
        "thk_slit",
        "ratio_slit",
        "mode_cell",
        "mode_slit",
    )

    obj.execute_calc()
    obj.execute_post(export_keys)


if __name__ == "__main__":
    main()
