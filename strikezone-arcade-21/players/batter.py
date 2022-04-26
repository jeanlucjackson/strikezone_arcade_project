#!/usr/bin/env python3

"""The Batter module builds upon the Player class to provide
further, batter-specific actions. A Player becomes a Batter
when they step up to the plate."""


# -------------------- Import Modules -------------------- #
import random

from players.player import Player






# -------------------- Batter Class -------------------- #

class Batter(Player):
    """The Batter class is a child of the Player class. 
    It is a representation of a baseball Player in the phase
    of batting, i.e. one who has just stepped up to the plate.
    The primary action added in this class is the get_pitch_outcome()
    method, which gives them the ability to read a Pitch and
    determine an outcome."""

    def __init__(self, player_object=None, first_name = "?", last_name = "?", team_city = "?", team_name = "?", position = "?", bat_avg = 0.0):
        
        # If we don't have a Player object to create this around, pass parameters to parent for initializing
        if player_object is None:
            super().__init__(first_name, last_name, team_city, team_name, position, bat_avg)
        
        # If we already have a Player object to create around, use their attributes
        else:
            super().__init__(player_object.first_name,
                            player_object.last_name,
                            player_object.team_city,
                            player_object.team_name,
                            player_object.position,
                            player_object.bat_avg)

    def get_pitch_outcome(self, pitch):
        """This method determines the outcome of delivering a Pitcher's pitch to
        this batter. The outcome is determined probabilistically with randomness
        included for a variety of outcomes given the same inputs."""

        pitch_thrown_probs = pitch.get_zone_outcome_probs()

        # Create a new dictionary whose values are ranges of integers
        # based on the probabilities. E.g. 4 inputs of 25% would result in:
        # 1 - 25, 26 - 50, 51 - 75, 76 - 100
        prob_ranges = {}
        sum = 1
        for outcome in pitch_thrown_probs.keys():
            # Convert this float probability to an integer by rounding
            this_prob = round(pitch_thrown_probs[outcome])
            
            # Add range of integers to dict
            prob_ranges[outcome] = range(sum, sum + this_prob)
            sum += this_prob


        # Pick a random number between 0 and 100
        # If this number falls in a given range, that outcome occurs
        r_num = random.randint(1, 99)
        pitch_outcome = [outcome for outcome,probs in prob_ranges.items() if r_num in probs][0]

        # The outcome is a string.
        return pitch_outcome


