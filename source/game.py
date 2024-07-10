"""
Author: Bilal Vandenberge
Date: June 2024
-> the file with the Game, GameSettings and GameError class
"""


from read_theme import Theme
import random

INDEX_TO_POWER = [
    ".",
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
        self._max_tile = 1 # the value of the biggest tile on the grid
        self._build_grid()

    def _build_grid(self) -> None:
        """
        build the grid of the game
        """
        self._grid = [[0 for _ in range(self._width)] for _ in range(self._height)]
        self._free_spots = set(range(self._width * self._height))

    def display(self, theme: Theme = None) -> None:
        """
        show in the terminal the grid of the game
        """
        max_len = len(str(INDEX_TO_POWER[self._max_tile])) + 1
        if theme is None:
            for line in self._grid:
                print(" ".join([str(INDEX_TO_POWER[e]) for e in line]))
        else:
            for line in self._grid:
                for e in line:
                    colors = theme.index(e)
                    print(colors[1].fg(colors[0].bg(str(INDEX_TO_POWER[e]).rjust(max_len))), end="")
                print()

    def is_lost(self) -> bool:
        """
        return if the game is in a dead end
        """
        if self.is_full():
            for y in range(self._width - 1):
                for x in range(self._height - 1):
                    if self._grid[x][y] == self._grid[x][y + 1] or self._grid[x][y] == self._grid[x + 1][y]:
                        return False
            return True
        else:
            return False

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
            # raise GameError("not enough space to spawn new tiles")
            number = len(self._free_spots) # Will stop after reaching the full grid completion
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
    # (and modify the return value to specify if there was a change in the grid during the execution)

    def tmp_down(self) -> bool:
        """ TEMPORARY
        change the gravity to the down gravity
        """
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
                    add_to_score = self._grid[y_pos + 1][column]
                    self._score += INDEX_TO_POWER[add_to_score]
                    self._max_tile = max(self._max_tile, add_to_score)
                    self._free_spots.add(pos)

    def tmp_up(self) -> bool:
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
                    add_to_score = self._grid[y_pos - 1][column]
                    self._score += INDEX_TO_POWER[add_to_score]
                    self._max_tile = max(self._max_tile, add_to_score)
                    self._free_spots.add(pos)

    def tmp_left(self) -> bool:
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
                    add_to_score = self._grid[line][x_pos - 1]
                    self._score += INDEX_TO_POWER[add_to_score]
                    self._max_tile = max(self._max_tile, add_to_score)
                    self._free_spots.add(y_pos + x_pos)

    def tmp_right(self) -> bool:
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
                    add_to_score = self._grid[line][x_pos + 1]
                    self._score += INDEX_TO_POWER[add_to_score]
                    self._max_tile = max(self._max_tile, add_to_score)
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

    @property
    def free_spots(self) -> list[list]:
        """
        return the list of free spots (without a tile)
        """
        return self._free_spots

    @property
    def max_tile(self) -> list[list]:
        """
        return the list of free spots (without a tile)
        """
        return self._max_tile


class GameSettings:
    """represent settings of a game of 2048"""

    AVAILABLE_LANGUAGES = {"English": 0, "French": 1, "Chinese": 2}
    AVAILABLE_LAYOUTS = {"cross", "square", "linear", "custom"}
    AVAILABLE_DIFFICULTIES = {"normal", "hell"}

    # methods:
    def __init__(self, up_key: str, down_key: str,
    left_key: str, right_key: str, theme: Theme, difficulty: str = "normal", language: str = "English",
    keys_layout: str = "square", custom_UDLR: str = None):
        self._build_keys(up_key, down_key, left_key, right_key)
        self._build_layout(keys_layout, custom_UDLR)
        self._build_language(language)
        self._build_theme(theme)
        self._build_difficulty(difficulty)

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

    def _build_layout(self, layout: str = "square", custom_UDLR: str = None) -> None:
        """
        build the layout of the keys to display each turn of the game
        AVAILABLES:
            {"cross", "square", "linear", "custom"}
        CUSTOM:
            if layout == 'custom': the arg is a string that contains letters U, D, L and R
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
                if custom_UDLR:
                    self._build_custom(custom_UDLR)
                else:
                    raise GameError("building a custom layout require a manual layout"
                    " as last argument of the constructor\nEXAMPLE:\nLUR\n D ")
            case _:
                raise GameError(f"unkown layout: {layout[:16] + ('...' if len(layout) > 16 else '')}")

    def _build_custom(self, custom_UDLR: str) -> None:
        """
        build the layout as custom
        custom_UDLR ARG:
            is a string that contains letters U, D, L and R (up down left right)
            and as much blank caracters as you want. Ex:
                U  D
                 LR
        """
        self._layout = (custom_UDLR.replace("U", f"[{self.up_key}]").replace("D", f"[{self.down_key}]")
        .replace("L", f"[{self.left_key}]").replace("R", f"[{self.right_key}]").replace(" ", "   "))

    def _build_language(self, language: str):
        """
        build the language of the settings
        ARG:
            - language: the selected language
        """
        assert isinstance(language, str) and language in GameSettings.AVAILABLE_LANGUAGES
        self._language = language
        self._lg_index = GameSettings.AVAILABLE_LANGUAGES[language]

    def _build_theme(self, theme: Theme) -> None:
        """
        build the theme of the game
        ARG:
            - theme: the Theme instance
        """
        assert isinstance(theme, Theme)
        self._theme = theme

    def _build_difficulty(self, difficulty: str = "normal") -> None:
        """
        build the difficulty of the level
        SUPPORTED:
            - normal
            - hell
        (see the docstring of Game.spawn_random() to see the changes)
        """
        assert isinstance(difficulty, str) and difficulty in GameSettings.AVAILABLE_DIFFICULTIES
        self._difficulty = difficulty

    def __str__(self) -> str:
        """
        return str(self)
        """
        return ("Game settings:\n  Directional keys:\n" +
        "\n".join([f"    {Game.AVAILABLE_DIRECTIONS[i].upper()} : {self._keys[i]}" for i in range(4)]) +
        f"\n  Language:\n    {self._language}\n  Theme:\n    {self._theme.name}\n  Difficulty:\n    {self._difficulty}"
        )

    def __eq__(self, gs2: "GameSettings") -> bool:
        """
        return self == gs2
        ARG:
            - gs2: the other game settings
        """
        return self._keys == gs2._keys and self._language == gs2._language

    # getters:
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

    @property
    def language_index(self) -> str:
        """
        return the language index for the dictionnary
        """
        return self._lg_index
  
    @property
    def theme(self) -> str:
        """
        return the language of the interface
        """
        return self._theme

    @property
    def difficulty(self) -> str:
        """
        return the language of the interface
        """
        return self._difficulty
