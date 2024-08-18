import json
from pathlib import Path
import numpy as np

from Utils.PolygonVertex import octagon


def export_to_json(inp: dict, coords_incell: np.ndarray, coords_outcell: np.ndarray, path: str):
    #
    oct = octagon(inp["thk_cc"], inp["thk_x1"], inp["thk_y1"])
    oct = np.vstack([oct, oct[0]])
    vertex_outcell = coords_outcell[:, np.newaxis, :] + oct

    #
    data = {
        "input_parameters": inp,
        "coords_incell": coords_incell.tolist(),
        "coords_outcell": vertex_outcell.tolist(),
    }

    #
    with open(path + ".json", "w") as f:
        json.dump(data, f, indent=4)


def ExportJSON(name: str, inp: dict, coords_incell: np.ndarray, coords_outcell: np.ndarray):
    #
    data = {
        "input_parameters": inp,
        "coords_incell": coords_incell.tolist(),
        "coords_outcell": coords_outcell.tolist(),
    }

    #
    with open(name + ".json", "w") as f:
        json.dump(data, f, indent=4)
