import yaml
import argparse
from pathlib import Path
from logging import getLogger, config


def logsetting() -> dict:
    # コマンドライン引数の取得
    # parser = argparse.ArgumentParser(description="Cell Layout Generator")
    # parser.add_argument("--i", type=str, required=False, help="inp.yaml")
    # args = parser.parse_args()

    # "inp.yaml"の読込み
    # inp_path = Path(args.i).resolve()
    # with open(inp_path, "r", encoding="utf-8") as file:
    #     data = yaml.safe_load(file)

    # ロギング設定
    # config.dictConfig(data["logging_config"])

    # TEMP
    inp_path = Path("inp.yaml").absolute()
    with open(inp_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)
    config.dictConfig(data["logging_config"])
    return data


def main(data: dict) -> None:
    from Pre import CheckDimensinons, dimensions_to_parameters

    # 口金図面寸法の確認
    dd = data["drawing_dimensions"]
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
    data = logsetting()
    try:
        main(data)
    except Exception as e:
        print(e)
