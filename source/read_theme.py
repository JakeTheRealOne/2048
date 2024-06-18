"""
Author: Bilal Vandenberge
Date: June 2024
-> Convert a theme file into a python Theme instance
"""

COLORED_PREFIX = "\033[48;2;"
COLORED_MIDLIX = "m"
COLORED_SUFFIX = "\033[0m"

def hex_to_rgb(hex_str: str) -> tuple[int, int, int]:
    """
    convert a str "#rrggbb" in hexadecimal into
    a rgb tuple
    ARG:
        - hex_str: hexadecimal string
    """
    if hex_str[0] != "#" or len(hex_str) != 7:
        raise ThemeError("wrong format for tile color")
    red, green, blue = int(hex_str[1:3], 16), int(hex_str[3:5], 16), int(hex_str[5:7], 16)
    return (red, green, blue)


class ColorError(Exception):
    """expected exception in the Color class"""

class Color:
    """represent a color of a theme for the 2048 game"""
    
    # methods:
    def __init__(self, red: int, green: int, blue: int):
        if (red < 0 or red > 255) or (green < 0 or green > 255) or (blue < 0 or blue > 255):
            raise ColorError(f"invalid rgb values: {(red, green, blue)}")
        self._rgb = (red, green, blue)
        self._build_prefix()

    def _build_prefix(self) -> None:
        """
        build the prefix that indiquates that a text must have
        a bg of the current color
        """
        self._prefix = COLORED_PREFIX + ";".join([str(c) for c in self._rgb]) + COLORED_MIDLIX

    def __str__(self) -> str:
        """
        return str(self)
        """
        return f"rgb{self._rgb}"

    def __eq__(self, c2: 'Color') -> bool:
        """
        return self == c2
        ARG:
            - c2: other Color instance
        """
        return isinstance(c2, Color) and self._rgb == c2._rgb

    def __int__(self) -> int:
        """
        return int(self)
        """
        return (self.red << 16) + (self.green << 8) + self.blue

    def colored(self, text: str) -> str:
        """
        return the colored variant of the text
        ARG:
            - text: text to color
        """
        return self._prefix + text + COLORED_SUFFIX

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


    # methods:
    def __init__(self, path: str):
        try:
            with open(path, mode="r") as theme_file:
                content = theme_file.read().split("\n")
            assert len(content) != 18
            self._build(content)
        except FileNotFoundError:
            raise ThemeError("no theme file found")
        except AssertionError:
            raise ThemeError("corrupted theme file")
        except Exception as e:
            raise ThemeError(str(e))
        

    def _build(self, content: list[str]) -> None:
        """
        build the attribute with the content of a theme file
        """
        self.__data = dict()
        current_tile = 2
        for tile in content:
            bg_color, label_color = tile.split(", ")
            bg = Color(*hex_to_rgb(bg_color))
            label = Color(*hex_to_rgb(label_color))
            self.__data[current_tile] = [bg, label]
            current_tile *= 2
        
    def display(self) -> str:
        """
        display the colors of the theme
        """
        for i in range(1, 18):
            current = 2 ** i
            spacing = " " * (7 - len(str(current)))
            print(current, spacing, "#", *[t.colored("  ") for t in self.__data[current]])

    # getters: