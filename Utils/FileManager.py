import yaml
import json

import numpy as np


def export_to_json(inp: dict, coords_incell: np.ndarray, coords_outcell: np.ndarray, path: str):
    data = {
        "input_parameters": inp,
        "coords_incell": coords_incell.tolist(),
        "coords_outcell": coords_outcell.tolist(),
    }

    with open("a.json", "w") as f:
        json.dump(data, f, indent=4)
