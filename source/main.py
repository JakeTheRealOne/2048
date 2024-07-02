"""
Author: Bilal Vandenberge
Date: June 2024
-> Run the game 2048 (cli, tui and qt)
"""

import random

# debug:
random.seed(593438)

INDEX_TO_POWER = [
    "N",
    2,
    4,
    8,
    16,
    32,
    64,
    128,
    256,
    512,
    1024,
    2048,
    4096,
    8192,
    16384,
    32768,
    65536,
    131072
]

class GameError(Exception):
    """represents a 2048 game intended exception"""

class Game:
    """represent a game of 2048"""

    AVAILABLE_DIRECTION = ["up", "down", "left", "right"]

    # methods:
    def __init__(self, width: int = 4, height: int = 4):
        self._width = width
        self._height = height
        self._size = width * height
        self._score = 0
        self._build_grid()

    def _build_grid(self) -> None:
        """
        build the grid of the game
        """
        self._grid = [[0 for _ in range(self._width)] for _ in range(self._height)]
        self._free_spots = set(range(self._width * self._height))

    def display(self) -> None:
        """
        show in the terminal the grid of the game
        """
        for line in self._grid:
            print(" ".join([str(INDEX_TO_POWER[e]) for e in line]))


    def is_losing(self) -> bool:
        """
        return if the game is in a dead end
        """
        pass

    def is_full(self) -> bool:
        """
        return if the grid is full
        """
        return not bool(len(self._free_spots))

    def random_pow(self, mode: str = "normal") -> int:
        """
        return a random power (2, 4, etc.) using the random table of 
        a mode
        ARG:
            - mode: the mode of the spawn (supported: start, normal and hell)
        """
        rand_val = random.random()
        match mode:
            case "start":
                return 1
            case "normal":
                if rand_val <= 0.1:
                    return 2
                else:
                    return 1
            case "hell":
                if rand_val <= 0.05:
                    return 6
                elif rand_val <= 0.2:
                    return 2
                else:
                    return 1
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
        if len(self._free_spots) < number:
            raise GameError("not enough space to spawn new tiles")
        for tile in range(number):
            # 1. find a line + column
            pos = random.choice(list(self._free_spots))
            # 2. choose a value for the tile
            val = self.random_pow(mode)
            # 3. update the grid, tiles number, free spots
            self._free_spots.remove(pos)
            self._grid[pos // self._width][pos % self._width] = val

    def change_gravity(self, orientation: str = "down") -> None:
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


    # ONE DAY, I WILL MERGE tmp_down, tmp_up, tmp_left and tmp_right together but now, i keep them ugly like that

    def tmp_down(self) -> None:
        """ TEMPORARY
        change the gravity to the down gravity
        """
        if self.is_full():
            return
        for column in range(self._width):
            for case in range(self._height - 2, -1, -1):
                current_pos = origin_pos = case * self._width + column
                if current_pos in self._free_spots:
                    continue
                current_pos += self._width
                while current_pos in self._free_spots:
                    current_pos += self._width
                current_pos -= self._width
                new_case = current_pos // self._width
                if origin_pos != current_pos:
                    self._grid[case][column], self._grid[new_case][column] = self._grid[new_case][column], self._grid[case][column]
                    # update free_spots
                    self._free_spots.remove(current_pos)
                    self._free_spots.add(origin_pos)
                # merge with the bottom tile if the values are identical
                if new_case < self._height - 1 and self._grid[new_case][column] == self._grid[new_case+1][column]:
                    # WHILE INSTEAD OF IF ? (in the real game its just an if but we can try our own rice here)
                    self._grid[new_case][column] = 0
                    self._grid[new_case + 1][column] += 1
                    self._free_spots.add(current_pos)

    def tmp_up(self) -> None:
        """ TEMPORARY
        change the gravity to the up gravity
        """
        if self.is_full():
            return
        for column in range(self._width):
            for case in range(1, self._height):
                current_pos = origin_pos = case * self._width + column
                if current_pos in self._free_spots:
                    continue
                current_pos -= self._width
                while current_pos in self._free_spots:
                    current_pos -= self._width
                current_pos += self._width
                new_case = current_pos // self._width
                if origin_pos != current_pos:
                    self._grid[case][column], self._grid[new_case][column] = self._grid[new_case][column], self._grid[case][column]
                    # update free_spots
                    self._free_spots.remove(current_pos)
                    self._free_spots.add(origin_pos)
                # merge with the bottom tile if the values are identical
                if new_case > 0 and self._grid[new_case][column] == self._grid[new_case - 1][column]:
                    # WHILE INSTEAD OF IF ? (in the real game its just an if but we can try our own rice here)
                    self._grid[new_case][column] = 0
                    self._grid[new_case - 1][column] += 1
                    self._free_spots.add(current_pos)
                

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
    def grid(self) -> list[list]:
        """
        return the grid of the game
        """
        return self._grid


if __name__ == "__main__":
    g1 = Game()
    g1.spawn_random(15, 'start')
    g1.display()
    g1.tmp_up()
    print()
    g1.display()
