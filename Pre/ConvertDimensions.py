from copy import deepcopy


def dwg_to_prod(draw_dimensions: dict) -> dict:
    res = deepcopy(draw_dimensions)
    scale = draw_dimensions["shrinkage_rate"]

    res["product"]["dia_outer"] /= scale
    res["product"]["dia_eff"] /= scale

    if res["incell"]["info"]["shape"] == "circle":
        res["incell"]["info"]["dia_incell"] /= scale
    elif res["incell"]["info"]["shape"] == "hexagon":
        res["incell"]["info"]["dia_incell"] /= scale

    if res["outcell"]["info"]["shape"] == "octagon":
        res["outcell"]["info"]["thk_outcell"] /= scale
        res["outcell"]["info"]["thk_wall_outcell"] /= scale
    elif res["outcell"]["info"]["shape"] == "square":
        res["outcell"]["info"]["thk_outcell"] /= scale
        res["outcell"]["info"]["thk_wall_outcell"] /= scale

    return res
