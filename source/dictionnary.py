"""
Author: Bilal Vandenberge
Date: July 2024
-> remember the messages for different languages
"""

# INDEXES:
# 0 English
# 1 French
# 2 Mandarin Chinese
# 3 Spanish (removed from production)
# 4 Russian (removed from production)

ALLS = {
    "help_msg":
    [
        (
        "usage: main.py [--help] [--azerty | --qwerty | --vim] [--english | --french | --chinese] [--theme] [--clear] [--best-score]\n"
        "\n"
        "options:\n"
        "    -h, --help          show the help page\n"
        "  keys:\n"
        "    --azerty            start a game with the Z Q S D keys as directional keys\n"
        "    --qwerty            start a game with the W A S D keys as directional keys\n"
        "    --vim               start a game as a gigachad (VIM keys)\n"
        "  languages:\n"
        "    --english, -en      set the language to English\n"
        "    --french, -fr       set the language to French\n"
        "    --chinese, -zh      set the language to Mandarin Chinese\n"
        "  extras:\n"
        "    --theme 'my_theme'  start a game with custom theme (all available in the themes directory)\n"
        "    --clear             clear all datas about the user (best score etc.)\n"
        "    --best-score        print the best score of the local player\n"
        "    --difficulty 'diff' set the game difficulty (available: normal, hell)\n"
        "\n"
        "credits:\n"
        "  the author of the game is Gabriele Cirulli\n"
        ),
        (
        "utilisation: main.py [--help] [--azerty | --qwerty | --vim] [--english | --french | --chinese] [--theme] [--clear] [--best-score]\n"
        "\n"
        "options:\n"
        "    -h, --help          affiche cette page d'aide\n"
        "  touches:\n"
        "    --azerty            débute une partie en utilisant les touches Z Q S D\n"
        "    --qwerty            débute une partie en utilisant les touches W A S D\n"
        "    --vim               devient un gigachad (touches VIM)\n"
        "  langues:\n"
        "    --english, -en      règle la langue sur Anglais\n"
        "    --french, -fr       règle la langue sur Français\n"
        "    --chinese, -zh      règle la langue sur Mandarin\n"
        "  extras:\n"
        "    --theme 'mon_theme' débute une partie avec un thème personnalisé (tous sont disponibles dans le dossier themes)\n"
        "    --clear             supprime toutes les données enregistrées (meilleur score etc.)\n"
        "    --best-score        affiche le meilleur score du joueur locale\n"
        "    --difficulty 'diff' règle la difficulté de la partie (disponibles: normal, hell)\n"
        "\n"
        "crédits:\n"
        "  l'auteur du jeu est Gabriele Cirulli\n"
        ),
        (
        "论点: main.py [--help] [--azerty | --qwerty | --vim] [--english | --french | --chinese] [--theme] [--clear] [--best-score]\n"
        "\n"
        "选项:\n"
        "    -h, --help          显示此帮助页面\n"
        "  按钮:\n"
        "    --azerty            用 Z Q S D 键作为方向键开始游戏\n"
        "    --qwerty            用 W A S D 键作为方向键开始游戏\n"
        "    --vim               使用 VIM 方向键开始游戏\n"
        "  语言:\n"
        "    --english, -en      将语言设置为英语\n"
        "    --french, -fr       将语言设置为法语\n"
        "    --chinese, -zh      将语言设置为普通话\n"
        "  更多:\n"
        "    --theme 'my_theme'  使用自定义主题（所有主题均可在主题文件夹中找到）开始游戏\n"
        "    --clear             删除所有保存的数据（最佳成绩等）。\n"
        "    --best-score        打印本地玩家的最好成绩。\n"
        "    --difficulty 'diff' 设置游戏难度 (可用: normal, hell)\n"
        "\n"
        "学分:\n"
        "  游戏的作者是加布里埃尔-西鲁利（Gabriele Cirulli\n"
        )
    ],
    "current_score":
    [
        "Current score",
        "Score actuel",
        "当前得分"
    ],
    "use":
    [
        "Use these keys:",
        "Touches directionnelles:",
        "方向键:"
    ],
    "won_msg":
    [
        "You won! Do you want to continue {yes/no}: ",
        "Vous avez gagné! Voulez-vous continuer {oui/non}: ",
        "您赢了！还想继续吗？ {是的/没有} :"
    ],
    "yes":
    [
        "yes",
        "oui",
        "是的"
    ],
    "select_direction":
    [
        "⌄ Select a direction",
        "⌄ Choisissez une direction",
        "选择方向"
    ],
    "unknown_direction":
    [
        "Unknown direction",
        "Direction inconnue",
        "方向不明"

    ],
    "final_score":
    [
        "final score",
        "score final",
        "最后得分"
    ],
    "you_lost":
    [
        "You lost.",
        "Vous avez perdu.",
        "你输了"
    ],
    "clear_error":
    [
        "There was an error while deleting user data.",
        "Il y a eu une erreur lors de la suppression des données utilisateurs.",
        "删除用户数据时出现错误"
    ],
    "clear_success":
    [
        "User data successfully deleted!",
        "Données utilisateur supprimées avec succès!",
        "用户数据已成功删除！"
    ]
}