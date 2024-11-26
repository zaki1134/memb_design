import yaml
import argparse
from pathlib import Path
from logging import getLogger, config


def loggingsetup() -> dict:
    # コマンドライン引数の取得
    parser = argparse.ArgumentParser(description="Cell Layout Generator")
    parser.add_argument("--i", type=str, required=False, help="inp.yaml")
    args = parser.parse_args()

    # "inp.yaml"の読込み
    inp_path = Path(args.i).resolve()
    with open(inp_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    # ロギング設定
    config.dictConfig(data["logging_config"])

    return data


def main(data: dict) -> None:
    from Pre import CheckDimensinons, drawing_to_product, ValidationProcess
    from Solver import CellParameters

    # 口金図面寸法の確認
    dwg_dims = data["drawing_dimensions"]
    CheckDimensinons(**dwg_dims)

    # 口金図面寸法から製品寸法への変換
    prod_dims = drawing_to_product(dwg_dims)

    # 製品寸法の成立性確認
    # del proddims

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
    data = loggingsetup()
    try:
        main(data)
    except Exception as e:
        print(e.__class__)

    print("===== Done =====")
