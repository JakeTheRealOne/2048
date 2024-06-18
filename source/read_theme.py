"""
Author: Bilal Vandenberge
Date: June 2024
-> Convert a theme file into a python Theme instance
"""

class ColorError(Exception):
    """expected exception in the Color class"""

class Color:
    """represent a color of a theme for the 2048 game"""
    # methods
    def __init__(self, red: int, green: int, blue: int):
        if (red < 0 or red > 255) or (green < 0 or green > 255) or (blue < 0 or blue > 255):
            raise ColorError(f"invalid rgb values: {(red, green, blue)}")
        self._rgb = (red, green, blue)


    def __str__(self) -> str:
        """
        return str(self)
        """
        return f"rgb{self._rgb}"

    def __eq__(self, c2: 'Color') -> bool:
        """
        return self == c2
        """
        return self._rgb == c2._rgb

    def __int__(self) -> int:
        """
        return int(self)
        """
        return (self.red << 16) + (self.green << 8) + self.blue

    # getters:
    @property
    def red(self):
        """
        return the red intensity of the color
        """
        return self._rgb[0]

    @property
    def green(self):
        """
        return the green intensity of the color
        """
        return self._rgb[1]

    @property
    def blue(self):
        """
        return the blue intensity of the color
        """
        return self._rgb[2]


class ThemeError(Exception):
    """expected exception in the Theme class"""

class Theme:
    # based color:
    BG_COLOR = Color(60, 58, 50) # Dark grey - #3c3a32
    LABEL_COLOR = Color(249, 246, 242) # White - #f9f6f2

    def __init__(self, path: str):
        with