"""
Author: Bilal Vandenberge
Date: June 2024
-> Run the game 2048 (cli, tui and qt)
"""

import random

# debug:
random.seed(593438)

class GameError(Exception):
    """represents a 2048 game intended exception"""

class Game:
    """represent a game of 2048"""

    AVAILABLE_DIRECTION = ["up", "down", "left", "right"]

    # methods:
    def __init__(self, width: int = 4, height: int = 4):
        self._width = width
        self._height = height
        self._score = self._max_tile = self._tiles_number = 0
        self._build_grid()

    def _build_grid(self) -> None:
        """
        build the grid of the game
        GRID:
        list [dict() for _ in range(self.height)] (list of lines)
        each dict keep pairs column:power (where column is the column index
        and power is the power of the tuile (from 2 to 131072))
        """
        self._grid = [dict() for _ in range(self.height)]
        self._available_lines = list(range(self.height))
        self._available_cases = [set(range(self.width)) for _ in range(self.height)]

    def display(self) -> None:
        """
        show in the terminal the grid of the game
        """
        full_len = len(str(self._max_tile))
        for line in range(self.height):
            for case in range(self.width):
                to_print = str(self._grid[line].get(case, " " * full_len))
                spacing = full_len - len(to_print)
                print((" " * ((spacing + 1) // 2)) + to_print + (" " * round(spacing / 2)), end="|")
            print("\n", end="")
        print()


    def is_losing(self) -> bool:
        """
        return if the game is in a dead end
        """
        pass

    def is_full(self) -> bool:
        """
        return if the game grid is complete

        """
        return self._tiles_number == self._width * self._height

    def random_pow(self, mode: str = "start") -> int:
        """
        return a random power (2, 4, etc.) using the random table of 
        a mode
        ARG:
            - mode: the mode of the spawn (supported: start, normal and hell)
        """
        rand_val = random.random()
        match mode:
            case "start":
                return 2
            case "normal":
                if rand_val <= 0.1:
                    return 4
                else:
                    return 2
            case "hell":
                if rand_val <= 0.05:
                    return 64
                elif rand_val <= 0.2:
                    return 4
                else:
                    return 2
            case _:
                raise GameError(f"unkown game mode: {mode[:32]}{"..." if len(mode) > 32 else ""}")

    def spawn_random(self, number: int, mode: str = "normal") -> None:
        """
        spawn randoms 2 and 4 tiles on the grid
        SPAWN RATE (start mode):
            - 2: 100%
        SPAWN RATE (normal mode):
            - 2: 90%
            - 4: 10%
        SPAWN RATE (hell mode):
            - 2: 80%
            - 4: 15%
            - 64: 5%
        ARGS:
            - number: the number of tiles to spawn
            - mode: the mode of the spawn (supported: normal and hell)
        """
        if self._tiles_number + number > self._width * self._height:
            raise GameError("not enough space to spawn new tiles")
        for tile in range(number):
            # 1. find a line
            # 2. find a column if line is free
            # 3. choose a value for the tile
            # 4. update the grid, tiles number, free spots
            rand_val = random.randint(0, len(self._available_lines) - 1)
            line = self._available_lines[rand_val]
            case = random.choice(list(self._available_cases[line]))
            value = self.random_pow(mode)
            self._max_tile = max(value, self._max_tile)
            self._grid[line][case] = value
            self._tiles_number += 1
            self._available_cases[line].remove(case)
            if not self._available_cases[line]:
                del self._available_lines[rand_val]
            self.display()




    def change_gravity(orientation: str = "down") -> None:
        """
        update the grid with a new gravity (down, up, left, right)
        STRUCTURE: (example with down 4x4)
            for each column:
                from bottom to top for each tile:
                    while there is nothing underneath:
                        move bottom
                    if there is a tile and the value are the same:
                        merge and delete
                    if there is the end or another diff. tile:
                        stop
        """
        pass

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

    @property
    def score(self) -> int:
        """
        return the score of the game
        """
        return self._score

    @property
    def grid(self) -> list[dict]:
        """
        return the grid of the game
        """
        return self._grid

    @property
    def tiles_number(self) -> int:
        """
        return the total number of tiles in the grid
        """
        return self._tiles_number

    @property
    def available_lines(self) -> list[int]:
        """
        return the list of index of available lines
        """
        return self._available_lines

    @property
    def max_tile(self) -> list[int]:
        """
        return the max tile value of the grid
        """
        return self._max_tile


if __name__ == "__main__":
    g1 = Game()
    g1.spawn_random(10, 'hell')
