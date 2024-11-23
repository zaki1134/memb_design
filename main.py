from pathlib import Path
import argparse

from Pre import Dimensinons

# from Solver import CellParameters, CircleOctagon, HexgonOctagon
from Utils import read_yaml


def main() -> None:
    # コマンドライン引数の取得
    # parser = argparse.ArgumentParser(description="Cell Layout Generator")
    # parser.add_argument("--i", type=str, required=False, help="inp.yaml")
    # args = parser.parse_args()

    # inp.yamlの読み込み
    # data = read_yaml(Path(args.i).resolve())
    data = read_yaml("inp.yaml")  # temp
    dd = data["draing_dimensions"]
    Dimensinons(dd["shrinkage_rate"], dd["offset_x"], dd["offset_y"])

    # try:
    #     params = CellParameters(**inp)
    # except Exception as e:
    #     raise Exception(f"Error: {e}")

    # if params.shape_incell == "circle" and params.shape_outcell == "octagon":
    #     obj = CircleOctagon(params)
    # elif params.shape_incell == "hexagon" and params.shape_outcell == "octagon":
    #     obj = HexgonOctagon(params)
    # else:
    #     raise Exception("Error: Invalid shape")

    # obj.execute_calc()

    # Utils.FileManager Quadrantの外だし
    # post processer 見直し 各種計算の実装


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(e)


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
