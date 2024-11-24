from pathlib import Path
from logging import getLogger, config
import argparse

from Pre import CheckDimensinons, dimensions_to_parameters

# from Solver import CellParameters, CircleOctagon, HexgonOctagon
from Utils import read_yaml


def main() -> None:
    # コマンドライン引数の取得
    # parser = argparse.ArgumentParser(description="Cell Layout Generator")
    # parser.add_argument("--i", type=str, required=False, help="inp.yaml")
    # args = parser.parse_args()

    # inp.yamlの読込み
    # data = read_yaml(Path(args.i).resolve())
    inp_path = Path("inp.yaml").absolute()  # temp
    data = read_yaml(inp_path)  # temp

    # ロギング設定
    config.dictConfig(data["logging_config"])
    # logger = getLogger(__name__)

    # 口金図面寸法の確認
    dd = data["draing_dimensions"]
    CheckDimensinons(**dd)

    # 口金図面寸法からセルパラメータへの変換
    param = dimensions_to_parameters(dd)

    # セルパラメータの成立性確認
    del param

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
