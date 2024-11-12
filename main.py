from pathlib import Path
import argparse

from Pre.CellParameters import CellParameters
from Pre.CellLayout import CircleOctagon
from Pre.CellLayout import HexgonOctagon
from Post.ExportQuadrant import Quadrant

from Utils.FileManager import read_yaml


def main() -> None:
    # parser = argparse.ArgumentParser(description="Cell Layout Generator")
    # parser.add_argument("--i", type=str, required=False, help="inp.yaml")
    # args = parser.parse_args()

    # data = read_yaml(Path(args.i).resolve())
    data = read_yaml("inp.yaml")
    inp = data["parameters"]
    for key, value in inp.items():
        print(f"{key}: {value}")

    try:
        params = CellParameters(**inp)
    except Exception as e:
        print(e)
        return

    if params.mode_cell == "circle":
        obj = CircleOctagon(params)
    elif params.mode_cell == "hexagon":
        obj = HexgonOctagon(params)

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
