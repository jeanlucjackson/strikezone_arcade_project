#!/usr/bin/env python3

"""This is the main file that starts and runs the game:
            StrikeZone Arcade '21
Please see the README.md file for more information, as well
as the "Game Information" option in the game's Main Menu."""


# -------------------- Import Modules -------------------- #
from game_structure.mainmenu import MainMenu



# -------------------- Command Line Access -------------------- #

if __name__ == "__main__":

    # Begin the game by starting the MainMenu.
    # From there, the rest of the game is handled by this MainMenu.

    menu = MainMenu()

