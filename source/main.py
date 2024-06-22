"""
Author: Bilal Vandenberge
Date: June 2024
-> Run the game 2048 (cli, tui and qt)
"""

class Game:
    """represent a game of 2048"""

    # methods:
    def __init__(self, width: int, height: int):
        self._width = width
        self._height = height

    # getters:
    @property
    def width(self) -> int:
        """
        return the width of the game grid
        """
        return self._width

    @property
    def height(self) -> int:
        """
        return the height of the game grid
        """
        return self._height

    


if __name__ == "__main__":
    print("coming soon...")