"""
Author: Bilal Vandenberge
Date: June 2024
-> Run the game 2048 (cli, tui and qt)
"""

import random
import sys

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

help_msg = ("Help page:\n  Welcome to 2048! Programmed by JakeTheRealOne"
+ "\n  Goal: get the highest score possible by adjusting the grid gravity\n"
+ "        two tiles with the same value can merge after changing the gravity\n"
+ "        you loose if you reach a dead end\n  Arguments:\n    --azerty : Start"
+ " a game in Azerty mode\n    --qwerty : Start a game in Qwerty mode"
+ "\n    --vim : Start a game as a GigaChad\n  Credit: the author of the game is Gabriele Cirulli")


class GameError(Exception):
    """represent a 2048 game intended exception"""
    pass

class Game:
    """represent a game of 2048"""

    AVAILABLE_DIRECTIONS = ["up", "down", "left", "right"]

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

    def change_gravity(self, orientation: int = 0) -> None:
        """
        update the grid with a new gravity (down, up, left, right)
        ARG:
            - orientation: the index of the new orientation in the AVAILABLE_DIRECTIONS:
                0 -> up
                1 -> down
                2 -> left
                3 -> right
        """
        assert isinstance(orientation, int) and 0 <= orientation < 4
        (self.tmp_up, self.tmp_down, self.tmp_left, self.tmp_right)[orientation]()


    # ONE DAY, I WILL MERGE tmp_down, tmp_up, tmp_left and tmp_right together but now, i keep them ugly like that

    def tmp_down(self) -> None:
        """ TEMPORARY
        change the gravity to the down gravity
        """
        # for column in range(self._width):
        #     for case in range(self._height - 2, -1, -1):
        #         current_pos = origin_pos = case * self._width + column
        #         if current_pos in self._free_spots:
        #             continue
        #         current_pos += self._width
        #         while current_pos in self._free_spots:
        #             current_pos += self._width
        #         current_pos -= self._width
        #         new_case = current_pos // self._width
        #         if origin_pos != current_pos:
        #             self._grid[case][column], self._grid[new_case][column] = self._grid[new_case][column], self._grid[case][column]
        #             # update free_spots
        #             self._free_spots.remove(current_pos)
        #             self._free_spots.add(origin_pos)
        #         # merge with the bottom tile if the values are identical
        #         if new_case < self._height - 1 and self._grid[new_case][column] == self._grid[new_case+1][column]:
        #             # WHILE INSTEAD OF IF ? (in the real game its just an if but we can try our own rice here)
        #             self._grid[new_case][column] = 0
        #             self._grid[new_case + 1][column] += 1
        #             self._free_spots.add(current_pos)
        for column in range(self._width):
            for case in range(self._height - 2, -1, -1):
                y_pos = case
                # stop if case is empty
                pos = column + case * self._width
                if pos in self._free_spots:
                    continue
                # the tile falls
                while y_pos < self._height - 1 and pos + self._width in self._free_spots:
                    y_pos += 1
                    pos += self._width
                if case != y_pos:
                    # update position in the grid
                    self._grid[case][column], self._grid[y_pos][column] = self._grid[y_pos][column], self._grid[case][column]
                    # update free_spots
                    self._free_spots.remove(pos)
                    self._free_spots.add(case * self._width + column)
                # merge with the bottom tile if the values are identical
                if y_pos < self._height - 1 and self._grid[y_pos][column] == self._grid[y_pos + 1][column]:
                    self._grid[y_pos][column] = 0
                    self._grid[y_pos + 1][column] += 1
                    self._free_spots.add(pos)

    def tmp_up(self) -> None:
        """ TEMPORARY
        change the gravity to the up gravity
        """
        for column in range(self._width):
            for case in range(1, self._height):
                y_pos = case
                # stop if case is empty
                pos = column + case * self._width
                if pos in self._free_spots:
                    continue
                # the tile falls
                while y_pos > 0 and pos - self._width in self._free_spots:
                    y_pos -= 1
                    pos -= self._width
                if case != y_pos:
                    # update position in the grid
                    self._grid[case][column], self._grid[y_pos][column] = self._grid[y_pos][column], self._grid[case][column]
                    # update free_spots
                    self._free_spots.remove(pos)
                    self._free_spots.add(case * self._width + column)
                # merge with the bottom tile if the values are identical
                if y_pos > 0 and self._grid[y_pos][column] == self._grid[y_pos - 1][column]:
                    self._grid[y_pos][column] = 0
                    self._grid[y_pos - 1][column] += 1
                    self._free_spots.add(pos)

    def tmp_left(self) -> None:
        """ TEMPORARY
        change the gravity to the left gravity
        """
        for line in range(self._height):
            y_pos = line * self._width
            for case in range(1, self._width):
                x_pos = case
                # stop if case is empty
                pos = y_pos + x_pos
                if pos in self._free_spots:
                    continue
                # the tile falls
                while x_pos > 0 and pos - 1 in self._free_spots:
                    x_pos -= 1
                    pos -= 1
                if case != x_pos:
                    # update position in the grid
                    self._grid[line][case], self._grid[line][x_pos] = self._grid[line][x_pos], self._grid[line][case]
                    # update free_spots
                    self._free_spots.remove(y_pos + x_pos)
                    self._free_spots.add(y_pos + case)
                # merge with the bottom tile if the values are identical
                if x_pos > 0 and self._grid[line][x_pos] == self._grid[line][x_pos - 1]:
                    self._grid[line][x_pos] = 0
                    self._grid[line][x_pos - 1] += 1
                    self._free_spots.add(y_pos + x_pos)

    def tmp_right(self) -> None:
        """ TEMPORARY
        change the gravity to the right gravity
        """
        for line in range(self._height):
            y_pos = line * self._width
            for case in range(self._width - 2, -1, -1):
                x_pos = case
                # stop if case is empty
                pos = y_pos + x_pos
                if pos in self._free_spots:
                    continue
                # the tile falls
                while x_pos < self._width - 1 and pos + 1 in self._free_spots:
                    x_pos += 1
                    pos += 1
                if case != x_pos:
                    # update position in the grid
                    self._grid[line][case], self._grid[line][x_pos] = self._grid[line][x_pos], self._grid[line][case]
                    # update free_spots
                    self._free_spots.remove(y_pos + x_pos)
                    self._free_spots.add(y_pos + case)
                # merge with the bottom tile if the values are identical
                if x_pos < self._width - 1 and self._grid[line][x_pos] == self._grid[line][x_pos + 1]:
                    self._grid[line][x_pos] = 0
                    self._grid[line][x_pos + 1] += 1
                    self._free_spots.add(y_pos + x_pos)

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


class GameSettings:
    """represent settings of a game of 2048"""

    AVAILABLE_LANGUAGES = {"English"}
    AVAILABLE_LAYOUTS = {"cross", "square", "linear", "custom"}

    def __init__(self, up_key: str, down_key: str,
    left_key: str, right_key: str, language: str = "English",
    keys_layout: str = "square", crosses: str = None):
        self._build_keys(up_key, down_key, left_key, right_key)
        self._build_layout(keys_layout, crosses)
        self._build_language(language)

    def _build_keys(self, up_key: str, down_key: str,
    left_key: str, right_key: str) -> None:
        """
        build the directional keys of the settings
        RESTRICTION:
            the lenght of a key must be 1
        ARGS:
            - up_key: the key assigned to moving upward the tiles
            - down_key: the key assigned to moving downward the tiles
            - left_key: the key assigned to moving leftward the tiles
            - right_key: the key assigned to moving rightward the tiles
        """
        assert (isinstance(up_key, str) and len(up_key) == 1 
        and isinstance(down_key, str) and len(down_key) == 1
        and isinstance(left_key, str) and len(left_key) == 1
        and isinstance(right_key, str) and len(right_key) == 1)
        self._keys = [up_key, down_key, left_key, right_key]

    def _build_layout(self, layout: str = "square", crosses: str = None) -> None:
        """
        build the layout of the keys to display each turn of the game
        AVAILABLES:
            {"cross", "square", "linear", "custom"}
        CUSTOM:
            if layout == custom: the arg is a string that contains letters U, D, L and R
            (up down left right) and as much blank caracters as you want. Ex:
                LUR
                 D
        ARGS:
            - layout: the layout type (see AVAILABLE above)
            - crosses: ONLY if layout == custom, is the manual layout of the keys
        """
        match layout:
            case "cross": # ex: wasd on Qwerty keyboards
                self._layout = f"   [{self.up_key.upper()}]   \n[{self.left_key.upper()}][{self.down_key.upper()}][{self.right_key.upper()}]"
            case "square": # default
                self._layout = f"[{self.up_key.upper()}][{self.down_key.upper()}]\n[{self.left_key.upper()}][{self.right_key.upper()}]"
            case "linear": # ex: VIM keys
                self._layout = f"[{self.left_key.upper()}][{self.down_key.upper()}][{self.up_key.upper()}][{self.right_key.upper()}]"
            case "custom":
                if crosses:
                    self._build_custom(crosses)
                else:
                    raise GameError("building a custom layout require a manual layout"
                    " as last argument of the constructor\nEXAMPLE:\nLUR\n D ")
            case _:
                raise GameError(f"unkown layout: {layout[:16] + ('...' if len(layout) > 16 else '')}")

    def _build_custom(crosses: str) -> None:
        """
        build the layout as custom
        crosses ARG:
            the crosses argument is a string that contains exactly 4 "X"
            and as much blank caracters as you want. Ex:
                X  X
                 XX
        """
        self._layout = ""

    def _build_language(self, language: str):
        """
        build the language of the settings
        ARG:
            - language: the selected language
        """
        assert isinstance(language, str) and language in GameSettings.AVAILABLE_LANGUAGES
        self._language = language

    def __str__(self) -> str:
        """
        return str(self)
        """
        return ("Game settings:\n  Directional keys:\n" +
        "\n".join([f"    {Game.AVAILABLE_DIRECTIONS[i].upper()} : {self._keys[i]}" for i in range(4)]) +
        f"\n  Language:\n    {self._language}"
        )

    def __eq__(self, gs2: "GameSettings") -> bool:
        """
        return self == gs2
        ARG:
            - gs2: the other game settings
        """
        return self._keys == gs2._keys and self._language == gs2._language

    @property
    def keys(self) -> list[str]:
        """
        return the list of keys
        """
        return self._keys
    
    @property
    def up_key(self) -> str:
        """
        return the UP key
        """
        return self._keys[0]

    @property
    def down_key(self) -> str:
        """
        return the DOWN key
        """
        return self._keys[1]

    @property
    def left_key(self) -> str:
        """
        return the RIGHT key
        """
        return self._keys[2]

    @property
    def right_key(self) -> str:
        """
        return the LEFT key
        """
        return self._keys[3]

    @property
    def layout(self) -> str:
        """
        return the layout of the directonal keys
        """
        return self._layout

    @property
    def language(self) -> str:
        """
        return the language of the interface
        """
        return self._language


def run_game(settings: GameSettings):
    """
    run a game of 2048
    ARG:
        - settings: the Game settings (keys, etc.)
    """
    g = Game()
    g.spawn_random(2, "start")
    while True:
        g.display()
        print(f"use the Z Q S D keys\n{settings.layout}")
        direction = input("choose a direction: ")
        match direction.lower():
            case settings.up_key:
                g.change_gravity(0)
            case settings.down_key:
                g.change_gravity(1)
            case settings.left_key:
                g.change_gravity(2)
            case settings.right_key:
                g.change_gravity(3)
            case _:
                print(f"unkown direction: [{(direction.upper()[0] + "..." if len(direction) > 1 else "") if len(direction) else ""}]")
        if g.is_full():
            break
        g.spawn_random(2)
        print()

    print("\nyou loose")

def main():
    """run the program"""
    if "--help" in sys.argv[1:]:
        print(help_msg)
    elif "--azerty" in sys.argv[1:]:
        run_game(GameSettings("z", "s", "q", "d", keys_layout="cross"))
    elif "--qwerty" in sys.argv[1:]:
        run_game(GameSettings("w", "s", "a", "d", keys_layout="cross"))
    elif "--vim" in sys.argv[1:]:
        run_game(GameSettings("k", "j", "h", "l", keys_layout="linear"))
    else:
        run_game(GameSettings("z", "s", "q", "d", keys_layout="cross"))


if __name__ == "__main__":
    #azerty_settings = GameSettings("z", "s", "q", "d")
    #print(azerty_settings)
    main()

#{TODO}
# 1. fix up and down movements (the while loop use the pos and its just worng because it can jump columns)
# 2. add settings management and remember preferences in a settings file