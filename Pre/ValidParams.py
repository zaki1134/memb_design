import numpy as np


# Shapelyにしよう


class ValidParams:
    @staticmethod
    def valid_dia_incell(
        name: str,
        dia_incell: float,
        thk_top: float,
        thk_mid: float,
    ) -> None:
        """dia_incellの値が適切かどうかをチェック.
        インセルの有効面積が0ではない."""
        value = dia_incell - 2 * (thk_top + thk_mid)
        if value <= 0:
            message = [
                f"{name}: 'dia_incell' must be greater than 2*(thk_top + thk_mid)",
                f"dia_incell: {dia_incell}",
                f"thk_top: {thk_top}",
                f"thk_mid: {thk_mid}",
            ]
            raise ValueError("\n".join(message))

    @staticmethod
    def valid_dia_prod(
        name: str,
        dia_prod: float,
        dia_incell: float,
        thk_prod: float,
    ) -> None:
        """dia_prodの値が適切かどうかをチェック.
        incelllが最低でも1つは配置されるようにする."""
        value = dia_prod - (dia_incell + 2 * thk_prod)
        if np.isclose(value, 0) or value < 0:
            message = [
                f"{name}: 'dia_prod' must be greater than dia_incell + 2*thk_prod",
                f"dia_prod: {dia_prod}",
                f"dia_incell: {dia_incell}",
                f"thk_prod: {thk_prod}",
            ]
            raise ValueError("\n".join(message))

    @staticmethod
    def valid_thk_slit_and_thk_outcell(
        name: str,
        thk_outcell: float,
        thk_y1: float,
        thk_slit: float,
    ) -> None:
        """thk_slitとthk_outcellの値が適切かどうかをチェック.
        thk_slitとthk_outcellの値が近い場合はエラー.薄いメッシュの作成を抑制"""
        if np.isclose(thk_slit, thk_outcell) and thk_slit != thk_outcell:
            message = [
                f"{name}: 'thk_slit' is close to 'thk_outcell' but does not match",
                f"thk_slit: {thk_slit}",
                f"thk_outcell: {thk_outcell}",
            ]
            raise ValueError("\n".join(message))

        yyy = thk_outcell - 2 * thk_y1
        if np.isclose(thk_slit, yyy) and thk_slit != yyy:
            message = [
                f"{name}: 'thk_slit' is close to 'thk_outcell' but does not match",
                f"thk_slit: {thk_slit}",
                f"thk_outcell: {thk_outcell}",
            ]
            raise ValueError("\n".join(message))

    @staticmethod
    def valid_thk_outcell(
        name: str,
        pitch_x: float,
        thk_wall_outcell: float,
        thk_outcell: float,
        thk_i2o: float,
        thk_x1: float,
    ) -> None:
        """thk_outcellの値が適切かどうかをチェック.
        incell-outcell間の境界をアウトセル角Y位置が通過するかどうかを確認.メッシュの対称性のため.
        """
        xxx = 0.5 * (pitch_x - thk_wall_outcell) - thk_x1
        if ValidParams().__line_i2o(xxx, thk_i2o, pitch_x) < 0.5 * thk_outcell:
            message = [
                f"{name}: 'thk_outcell' is too large",
                f"thk_outcell: {thk_outcell}",
                f"thk_wall_outcell: {thk_wall_outcell}",
                f"pitch_x: {pitch_x}",
                f"thk_i2o: {thk_i2o}",
            ]
            raise ValueError("\n".join(message))

    @staticmethod
    def valid_thk_slit(
        name: str,
        thk_slit: float,
        thk_i2o: float,
        pitch_x: float,
    ) -> None:
        """thk_slitの値が適切かどうかをチェック.
        incell-outcell間の境界をスリットY位置が通過するかどうかを確認.メッシュの対称性のため.
        """
        yyy = thk_i2o - 0.5 * pitch_x / np.cos(np.pi / 6)
        if np.isclose(0.5 * thk_slit, yyy) or 0.5 * thk_slit >= yyy:
            message = [
                f"{name}: 'thk_slit' is too large",
                f"thk_slit: {thk_slit}",
                f"thk_i2o: {thk_i2o}",
                f"pitch_x: {pitch_x}",
            ]
            raise ValueError("\n".join(message))

    @staticmethod
    def __line_i2o(
        x: float,
        thk_i2o: float,
        pitch_x: float,
    ) -> float:
        """incell-outcell間の境界を y=ax+b で表現"""
        a = -1 / np.sqrt(3)
        b = thk_i2o - 0.5 * pitch_x * np.tan(np.pi / 6)
        return a * x + b
