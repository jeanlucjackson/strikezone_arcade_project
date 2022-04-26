#!/usr/bin/env python3

"""The LoadGame module creates variables at game startup.
Current implementation creates the game's Pitchers and
Baseball Teams to play with."""


# -------------------- Import Modules -------------------- #
from players.player import Player
from players.baseballteam import BaseballTeam
from players.pitcher import Pitcher






# -------------------- Module Functions -------------------- #

def create_baseball_teams():
    """This function creates baseball teams and returns them in a dictionary."""
    loaded_teams = {}
    # --- Seattle Mariners
    crawford = Player("J.P.", "Crawford", 'Seattle', "Mariners", 'SS', 0.273)
    mitch = Player("Mitch", "Haniger", 'Seattle', 'Mariners', 'RF', .253)
    seager = Player("Kyle", 'Seager', 'Seattle', 'Mariners', '3B', .212)
    france = Player('Ty', 'France', 'Seattle', 'Mariners', '2B', .291)
    toro = Player("Abraham", 'Toro', 'Seattle', 'Mariners', '3B', .239)
    torrens = Player("Luis", 'Torrens', 'Seattle', 'Mariners', 'C', .243)
    kelenic = Player("Jarred", 'Kelenic', 'Seattle', 'Mariners', 'LF', .181)
    murphy = Player("Tom", 'Murphy', 'Seattle', 'Mariners', 'C', .202)
    marmo = Player("Jose", 'Marmolejos', 'Seattle', 'Mariners', '1B', .160)
    Seattle_Mariners = BaseballTeam('Seattle', 'Mariners', 
                                    [crawford, mitch, seager, france, toro, torrens, kelenic, murphy, marmo]
                                    )
    loaded_teams['Seattle Mariners'] = Seattle_Mariners
    
    return loaded_teams

def create_pitchers():
    """This function loads available pitchers and returns them in a dictionary."""
    loaded_pitchers = {}

    # -- Clayton Kershaw
    kershaw = Pitcher("Clayton", "Kershaw", "Los Angeles", "Dodgers", repertoire=('Fastball', 'Breaking'))
    kershaw.load_popz_from_json()
    loaded_pitchers['Clayton Kershaw'] = kershaw

    return loaded_pitchers