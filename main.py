from pathlib import Path
import argparse

from Pre.CellParameters import CellParameters
from Pre.CellLayout import CircleOctagon
from Pre.CellLayout import HexgonOctagon
from Post.ExportQuadrant import Quadrant
from Post.ExportJSON import ExportJSON

from Utils.FileManager import read_yaml


def main() -> None:
    parser = argparse.ArgumentParser(description="Cell Layout Generator")
    parser.add_argument("--i", type=str, help="inp.yaml", required=False)
    args = parser.parse_args()

    data = read_yaml(Path(args.i).resolve())
    inp = data["parameters"]

    try:
        params = CellParameters(**inp)
    except Exception as e:
        print(e)
        return None

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
