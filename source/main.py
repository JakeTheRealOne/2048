"""
Author: Bilal Vandenberge
Date: June 2024
-> Run the game 2048 (cli, tui and qt)
"""

import shutil as st
import os
from getkey import getkey
import argparse as ap

import read_theme
import dictionnary
import game


def clear_terminal() -> None:
    """
    clear the terminal
    """
    if os.name == "posix": # Unix
        os.system("clear")
    else: # Windows
        os.system("cls")


def format_cross_os(unknown) -> str:
    """
    On some OS, the getkey output is either:
        - a string object (Windows 11)
        - a bytes object (Ubuntu/Debian)
        - a tuple with both (Arch linux)
    return the string
    """
    if isinstance(unknown, str):
        return unknown
    elif isinstance(unknown, bytes):
        return unknown.decode()
    elif isinstance(unknown, tuple):
        return format_cross_os(unknown[0])
    else:
        raise game.GameError("the getkey librairy has an unknown output format on your OS")


def show_help(language: str) -> None:
    match language:
        case "English":
            print(dictionnary.ALLS["help_msg"][0])
        case "French":
            print(dictionnary.ALLS["help_msg"][1])
        case "Chinese":
            print(dictionnary.ALLS["help_msg"][2])
        case _:
            raise game.GameError(f"internal error while print the help page in {language}")


def get_best_score() -> int:
    """
    return the best score stored in memory/best_score
    """
    init_memory()
    with open("memory/best_score", mode="r") as f:
        best_score = int(f.read())
    return best_score    


def update_best_score(current_score: int) -> None:
    """
    update the best score stored in memory/best_score if the current score
    is better
    ARG:
        current_score: the score reached after a game
    """
    # init_memory must be called before just to be sure that the file exist
    with open("memory/best_score", mode="r") as f:
        best_score = int(f.read())
    if best_score < current_score:
        print("We have a new best score!")
        with open("memory/best_score", mode="w") as f:
            f.write(str(current_score))  


def run_game(settings: game.GameSettings) -> None:
    """
    run a game of 2048
    ARG:
        - settings: the Game settings (keys, etc.)
    """
    clear_terminal()
    g = game.Game()
    g.spawn_random(2, "start")
    direction = "?"
    win_flag = False
    lose_flag = False
    err_flag = False
    while not lose_flag:
        g.display(settings.theme)
        print(f"{dictionnary.ALLS["current_score"][settings.language_index]}: {g.score}")
        if err_flag:
            print(dictionnary.ALLS["unknown_direction"][settings.language_index] +
            f" [{(repr(direction.upper()[0])[1:-1] + ("..." if len(direction) > 1 else "")) if len(direction) else ""}]")
            err_flag = False
        print(f"{dictionnary.ALLS["use"][settings.language_index]} {{{" ".join(settings.keys)}}}\n\n{settings.layout}\n")
        if not win_flag and g.max_tile == 11:
            win_flag = True
            if input(dictionnary.ALLS["won_msg"][settings.language_index]).lower() != dictionnary.ALLS["yes"][settings.language_index]:
                clear_terminal()
                break
        print(dictionnary.ALLS["select_direction"][settings.language_index])
        direction = format_cross_os(getkey())
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
                err_flag = True
                clear_terminal()
                continue
        g.spawn_random(2, settings.difficulty)
        lose_flag = g.is_lost()
        clear_terminal()
    if lose_flag:
        print(f"{dictionnary.ALLS["you_lost"][settings.language_index]} ({dictionnary.ALLS["final_score"][settings.language_index]}: {g.score})")
    else:
        print(f"{dictionnary.ALLS["final_score"][settings.language_index]}: {g.score}")
    update_best_score(g.score)


def init_memory() -> None:
    """
    create memory files if not yet existing
    """
    if not os.path.exists("memory") or not os.path.isdir("memory"):
        os.mkdir("memory")
        with open("memory/best_score", mode="w+") as f:
            f.write("0")
    if not os.path.exists("memory/best_score") or not os.path.isfile("memory/best_score"):
        with open("memory/best_score", mode="w+") as f:
            f.write("0")


def build_parser() -> ap.ArgumentParser:
    """
    build the argument parser
    """
    parser = ap.ArgumentParser(add_help=False)
    parser.add_argument(
        "--help", "-h", help="get the custom help page", action="store_true"
    )
    keyboard = parser.add_mutually_exclusive_group()
    keyboard.add_argument(
        "--azerty", help="run the game with the Z Q S D keys as directional keys", action="store_true"
    )
    keyboard.add_argument(
        "--qwerty", help="run the game with the W A S D keys as directional keys", action="store_true"
    )
    keyboard.add_argument(
        "--vim", help="run the game as a gigachad (VIM keys)", action="store_true"
    )
    language = parser.add_mutually_exclusive_group()
    language.add_argument(
        "--english", "-en", help="run the game in English", action="store_true"
    )
    language.add_argument(
        "--french", "-fr", help="run the game in French", action="store_true"
    )
    language.add_argument(
        "--chinese", "-zh", help="run the game in Mandarin Chinese", action="store_true"
    )
    parser.add_argument("--best-score", help="get the best score (local)", action="store_true")
    parser.add_argument("--clear", help="clear all user data", action="store_true")
    return parser


def parse_language(args: ap.ArgumentParser) -> str:
    """
    get the selected language from the arguments
    """
    lang = "English"
    if args.french:
        lang = "French"
    elif args.chinese:
        lang = "Chinese"
    return lang


def parse_keyboard(args: ap.ArgumentParser) -> tuple:
    """
    get the selected keyboard setting from the arguments
    """
    keys = "z", "s", "q", "d"
    layout = "cross"
    if args.qwerty:
        keys = "w", "s", "a", "d"
    elif args.vim:
        keys = "k", "j", "h", "l"
        layout = "linear"
    return keys, layout


def clear_memory(language: str):
    """
    clear all datas saved
    """
    try:
        st.rmtree("memory")
    except Exception:
        match language:
            case "English":
                print(dictionnary.ALLS["clear_error"][0])
            case "French":
                print(dictionnary.ALLS["clear_error"][1])
            case "Chinese":
                print(dictionnary.ALLS["clear_error"][2])
            case _:
                print(dictionnary.ALLS["clear_success"][0])
    else:
        match language:
            case "English":
                print(dictionnary.ALLS["clear_success"][0])
            case "French":
                print(dictionnary.ALLS["clear_success"][1])
            case "Chinese":
                print(dictionnary.ALLS["clear_success"][2])
            case _:
                print(dictionnary.ALLS["clear_success"][0])


def main() -> None:
    """
    run the program
    """
    init_memory()
    parser = build_parser()
    args = parser.parse_args()
    lang = parse_language(args)
    if args.best_score:
        print(get_best_score())
    elif args.clear:
        clear_memory(lang)
    elif args.help:
        show_help(lang)
    else:
        keys, layout = parse_keyboard(args)
        theme = read_theme.Theme("themes/base.dmqu")
        settings = game.GameSettings(*keys, theme=theme, language=lang, keys_layout=layout)
        run_game(settings)


if __name__ == "__main__":
    main()

#{TODO}
# 2. add settings management and remember preferences in a settings file
# 3. block the turn if no movement are mades
