from pathlib import Path
import argparse

from Pre.CellParameters import CellParameters
from Pre.CellLayout import CircleOctagon
from Pre.CellLayout import HexgonOctagon
from Post.ExportQuadrant import Quadrant
from Post.ExportJSON import ExportJSON

from Utils.FileManager import read_yaml


def main() -> None:
    inp = {
        "index": 0,
        "shape_incell": "hexagon",  # "circle", "hexagon"
        "shape_outcell": "octagon",
        "dia_incell": 3.0,
        "thk_top": 0.020,
        "thk_mid": 0.250,
        "thk_bot": 0.000,
        "thk_wall": 0.500,
        "thk_c2s": 0.500,
        "dia_prod": 30.000,
        "thk_prod": 1.000,
        "thk_outcell": 1.000,
        "thk_wall_outcell": 0.500,
        "thk_slit": 0.500,
        "ratio_slit": 3,
        "mode_cell": False,
        "mode_slit": False,
        "ln_prod": 1000.0,
    }
    parser = argparse.ArgumentParser(description="Process input YAML file.")
    parser.add_argument("--inp", type=str, help="Path to the input YAML file")
    args = parser.parse_args()

    input_file_path = Path(args.inp).resolve()
    print(f"Full path to the input YAML file: {input_file_path}")

    # data = read_yaml(args.input_file)
    # data = read_yaml("inp.yaml")
    # print(data["parameters"])

    # try:
    #     params = CellParameters(**inp)
    # except Exception as e:
    #     print(e)
    #     return None

    # # obj = CircleOctagon(params)
    # obj = HexgonOctagon(params)
    # obj.execute_calc()

    # ExportJSON(
    #     "output",
    #     obj.params.__dict__,
    #     obj.coords_incell,
    #     obj.coords_outcell,
    # )


# export_keys = (
#     "dia_incell",
#     "thk_top",
#     "thk_mid",
#     "thk_bot",
#     "thk_wall",
#     "thk_c2s",
#     "dia_prod",
#     "thk_prod",
#     "thk_outcell",
#     "thk_wall_outcell",
#     "thk_slit",
#     "ratio_slit",
#     "mode_cell",
#     "mode_slit",
# )

# obj.execute_calc()
# obj.execute_post(export_keys)
# for x in dir(obj):
#     print(x)
# export_to_json(inp, obj.coords_incell, obj.coords_outcell, "output")


if __name__ == "__main__":
    main()
