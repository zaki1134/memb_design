from pprint import pprint

from Pre import Parameters, CalcParameters


def dimensions_to_parameters(draw_dimensions: dict) -> Parameters:
    res = {}
    scale = draw_dimensions["shrinkage_rate"]

    # product
    res["dia_outer"] = draw_dimensions["product"]["dia_outer"] / scale
    res["dia_eff"] = draw_dimensions["product"]["dia_eff"] / scale
    res["ln_prod"] = draw_dimensions["product"]["ln_prod"]
    res["thk_wall"] = draw_dimensions["product"]["thk_wall"] / scale
    res["thk_c2s"] = draw_dimensions["product"]["thk_c2s"] / scale
    res["offset_x"] = draw_dimensions["product"]["offset_x"]
    res["offset_y"] = draw_dimensions["product"]["offset_y"]

    # incell
    res["shape_incell"] = draw_dimensions["incell"]["shape"]
    if res["shape_incell"] == "circle":
        res["dia_incell"] = draw_dimensions["incell"]["info"]["dia_incell"] / scale
    elif res["shape_incell"] == "hexagon":
        res["dia_incell"] = draw_dimensions["incell"]["info"]["dia_incell"] / scale

    res["thk_top"] = draw_dimensions["incell"]["thk_top"]
    res["thk_mid"] = draw_dimensions["incell"]["thk_mid"]

    # outcell
    res["shape_outcell"] = draw_dimensions["outcell"]["shape"]
    res["num_oc"] = draw_dimensions["outcell"]["num_oc"]
    if res["shape_outcell"] == "octagon":
        res["thk_outcell"] = draw_dimensions["outcell"]["info"]["thk_outcell"] / scale
        res["thk_wall_outcell"] = draw_dimensions["outcell"]["info"]["thk_wall_outcell"] / scale
    elif res["shape_outcell"] == "square":
        res["thk_outcell"] = draw_dimensions["outcell"]["info"]["thk_outcell"] / scale
        res["thk_wall_outcell"] = draw_dimensions["outcell"]["info"]["thk_wall_outcell"] / scale

    # slit
    res["thk_slit"] = draw_dimensions["slit"]["thk_slit"]
    res["ratio_slit"] = draw_dimensions["slit"]["ratio_slit"]
    res["num_ic_lim"] = draw_dimensions["slit"]["num_ic_lim"]

    # calc parameters
    res["pitch_x"] = CalcParameters.pitch_x(res["dia_incell"], res["thk_wall"])

    pprint(res, sort_dicts=False)

    return Parameters(**res)
