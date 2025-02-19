import sys
import yaml
import argparse
from pathlib import Path
from logging import getLogger, config

from Pre import Dimensions
from Solver import LayoutProcesser
from Utils import Parameters


def logging_setup(inp_path: Path) -> dict:
    # "inp.yaml"の読込み
    try:
        with open(inp_path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
    except Exception:
        raise Exception

    # config設定
    data["logging_config"]["handlers"]["file"]["filename"] = inp_path.parent / "log.txt"
    config.dictConfig(data["logging_config"])

    return data


def main(data: dict) -> None:
    # 図面寸法, 製品寸法の成立性確認
    dims = Dimensions(data["drawing_dimensions"])
    dims.execute_check()
    dims.execute_valid()

    # 配置計算
    dwg_dims = Parameters(dims.dwg)
    prod_dims = Parameters(dims.prod)
    dwg = LayoutProcesser(dwg_dims)
    prod = LayoutProcesser(prod_dims)

    from pprint import pprint

    print(type(dwg_dims.shrinkage_rate))
    print(dwg_dims.shrinkage_rate)

    # ファイル出力
    # drawing_info.json(dims.dwg, dwg_prop, incell配置, outcell配置, slit配置)
    # product_info.json(dims.prod, prod_prop, incell配置, outcell配置, slit配置)
    # layout.csv

    del dwg, prod


if __name__ == "__main__":
    # コマンドライン引数の取得
    parser = argparse.ArgumentParser(description="Cell Layout Generator")
    parser.add_argument("--i", type=str, required=True, help="inp.yaml")
    args = parser.parse_args()

    # ロギング設定
    try:
        inp_path = Path(args.i).resolve()
        data = logging_setup(inp_path)
    except Exception:
        print("Error: Failed to load inp.yaml")
        sys.exit(1)

    logger = getLogger("root")

    try:
        main(data)
        logger.info("===== Done =====")
    except Exception as e:
        logger.exception(e)
