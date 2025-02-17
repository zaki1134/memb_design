import yaml
import argparse
from pathlib import Path
from logging import getLogger, config
import traceback


def logging_setup() -> dict:
    # コマンドライン引数の取得
    parser = argparse.ArgumentParser(description="Cell Layout Generator")
    parser.add_argument("--i", type=str, required=False, help="inp.yaml")
    args = parser.parse_args()

    # "inp.yaml"の読込み エラーチェック追記
    inp_path = Path(args.i).resolve()
    with open(inp_path, "r", encoding="utf-8") as file:
        try:
            data = yaml.safe_load(file)
        except Exception:
            raise Exception

    # ロギング設定
    config.dictConfig(data["logging_config"])

    return data


def main(data: dict) -> None:
    from Pre import CheckDimensinons, dwg_to_prod, ValidationProcess
    from Utils import Parameters

    # 口金図面寸法の確認
    dwg_dims = data["drawing_dimensions"]
    CheckDimensinons(**dwg_dims)

    # 口金図面寸法から製品寸法への変換
    prod_dims_dict = dwg_to_prod(dwg_dims)
    prod_dims = Parameters(prod_dims_dict)

    # 製品寸法の成立性確認
    ValidationProcess(prod_dims)

    # 配置計算 Solve

    # ファイル出力
    # layout.csv, params.json(dwg_dims, prod_dims, incell配置、outcell配置、slit配置)
    # Utils.FileManager Quadrantの外だし

    # post processer 外だし 見直し 各種計算の実装

    del prod_dims


if __name__ == "__main__":
    try:
        data = logging_setup()
        main(data)
        print("===== Done =====")
    except Exception:
        traceback.print_exc()
