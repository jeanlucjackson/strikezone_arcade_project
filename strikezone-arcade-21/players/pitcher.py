#!/usr/bin/env python3

"""The Pitcher module builds upon the Player class to provide
further, pitcher-specific actions. A Pitcher can be loaded
from and saved to a JSON file for loading in future games.
A Pitcher's primary ability is to create probabilities from a
POPZ table, which are translated into a Pitch object for the
batter to receive."""


# -------------------- Import Modules -------------------- #
import json
import os.path

from players.player import Player
from game_structure.pitch import Pitch
from game_structure.strikezoneexceptions import PitchTypeError


# -------------------- Initialize Global Variables -------------------- #

pitch_types = ("Fastball", "Offspeed", "Breaking")

# Define possible outcomes a batter may produce from any given pitch
pitch_outcomes = ("Called Strike",
                "Swinging Strike",
                "Ball", 
                "Foul Ball",
                "In Play Out",
                "Single",
                "Double",
                "Triple",
                "Homerun",
                "Hit By Pitch")

# Statcast attack zones per baseballsavant.mlb.com
# Zone 10 is skipped to match statcast
pitch_zones = ("zone1", "zone2", "zone3", "zone4", "zone5", "zone6", "zone7", "zone8", "zone9", 
        "zone11", "zone12", "zone13", "zone14")

# Data directory shortcuts
popz_json_dir = 'data/popz/'
popz_json_filepath = os.path.join( os.path.split(os.path.dirname(__file__))[0] , popz_json_dir )

# Float of MLB's batting average.
# This adjusts the game's difficulty (higher decimal = easier game).
avg_bat_avg = 0.245
# Game difficulty exponent (I'm still figuring out the best way to make this game difficult)
difficulty_mult = 8


# -------------------- Pitcher Class -------------------- #

class Pitcher(Player):
    """The Pitcher class is a child of the Player class.
    It is modeled after a real-life MLB pitcher, having 
    as attributes the pitcher’s pitch repertoire and 
    respective strike zone outcome probabilities for each 
    zone and for each pitch type."""

    def __init__(self, first_name, last_name, team_city, team_name, 
                repertoire=pitch_types):
        
        # Initialize pitcher name and team using Player's constructor
        super().__init__(first_name, last_name, team_city, team_name, position='Pitcher')

        self.pitch_types = repertoire

        self.popz = {}
    
    def interactive_popz_to_json(self):
        """This method creates a POPZ table by guiding the user to
        input outcome probabilities for each zone and each pitch type.
        The table is then saved to a json file for future loading."""

        # Inform user how this works
        print('Beginning interactive POPZ table creation.')
        print('Input all probabilities as full percentages with 2 decimals: XX.XX (%)')
        print('For example, input 23.3% as: 23.3\n')

        # Loop through pitch types (class variable)
        for pitch_type in self.pitch_types:
            pitch_type_dict = {}

            # Loop through zones (global variable)
            for zone in pitch_zones:
                zone_dict = {}
                print(f'Pitch: {pitch_type} \nZone: {zone}')
                # Loop through outcomes (global variable) to update zone_dict
                for outcome in pitch_outcomes:
                    # For each zone collect the outcome probability
                    while True:
                        # Error handling if user does not provide a float
                        try:
                            prob = float(input(f'Probability of {outcome}: '))
                            break
                        except TypeError:
                            print('Please provide a valid float.')
                    
                    # Add this probability to the zone_dict
                    zone_dict[outcome] = prob

                # Add this zone_dict to the pitch_type_dict
                pitch_type_dict[zone] = zone_dict
                print(f'Zone: {zone} added to {pitch_type}')

            # Add this pitch_type_dict to the POPZ dict
            self.popz[pitch_type] = pitch_type_dict
            print(f'Pitch type {pitch_type} added to POPZ.\n')

        # Calling method to save to json file
        self.write_popz_to_json()


    def write_popz_to_json(self):
        """Write this pitcher's POPZ table to a JSON file in data/popz/"""
        if self.popz != {}:
            try:
                # example filename = data/popz/clayton_kershaw.json
                popz_json_filename = popz_json_filepath + self.first_name.lower() + '_' + self.last_name.lower() + '.json'
                print(f'Writing POPZ data to {popz_json_filename}')
                # Open file for writing
                with open(popz_json_filename, 'w+') as outfile:
                    json.dump(self.popz, outfile)
                print(f'POPZ data saved to {popz_json_filename}')
            except:
                print('An error occurred while saving POPZ table to JSON file.')
        else:
            # No POPZ data created yet, so there's nothing to save
            print(f'This pitcher has no POPZ data yet. Import an existing JSON file or manually input with interactive_popz_to_json().')

    def load_popz_from_json(self):
        """Load a POPZ table from a JSON file in data/popz/"""
        if self.popz != {}:
            print(f"{self.first_name} {self.last_name}'s POPZ table is not currently empty.")
            print(f"Importing a POPZ table from JSON will overwrite this pitcher's data.")
            while True:
                proceed = input(f"Would you like to proceed? (Y/N) ")
                if proceed.lower() in ['n', 'no', 'q', 'quit']:
                    # User has chosen to quit, so return and end function
                    print(f'POPZ import cancelled.')
                    return 'UserCancel'
                if proceed.lower() in ['y', 'yes']:
                    # User has chosen to proceed, so break from while loop
                    break
                else:
                    # User has provided invalid input
                    print('Please provide a valid input.')
        try:
            # example filename = data/popz/clayton_kershaw.json
            popz_json_filename = popz_json_filepath + self.first_name.lower() + '_' + self.last_name.lower() + '.json'
            # Open file for reading
            with open(popz_json_filename, 'r') as infile:
                self.popz = json.load(infile)
        except FileNotFoundError:
            print(f'File not found.')
        except Exception as err:
            print(f'An error occurred while importing json data: {type(err)} {err}')

    def pitch(self, pitch_type, zone, batter=None):
        """This method acts as a getter to pull the correct Probability of Outcome
        based on the provided Pitch Type and Zone. It returns a Pitch object containing
        the zone dictionary with normalized values (all add up to 100.00%).
        The Batter parameter is used to factor the probabilities based on their batting
        average. A good batter will have a better chance of hitting a base hit."""

        # Check if pitch_type is in this Pitcher's repertoire
        if pitch_type not in self.pitch_types:
            # Raise custom exception to be handled by PlateAppearance
            raise PitchTypeError

        # Get zone_dict from input - create shallow copy to not alter original
        zone_dict = self.popz[pitch_type][zone].copy()
        
        # Factor the probabilities up/down based on the batter's batting avg
        bat_avg = batter.bat_avg
        league_avg = avg_bat_avg
        # bat_avg_factor = 1.0 + (0.1 * (bat_avg - league_avg) * 100)
        # bat_avg_factor_sign = (bat_avg - league_avg) / abs(bat_avg - league_avg)
        bat_avg_factor = 1.0 + 10.0 * (bat_avg - league_avg)
        batter_favored = ['Single', 'Double', 'Triple', 'Homerun']
        
        if batter is not None:
            
            for outcome in zone_dict:
                
                # Manipulate probabilities of outcomes if they are batter-favored
                if outcome in batter_favored:
                    
                    # If this is a good batter, 0.0 chance base hits become non-zero and amplified by factor
                    if bat_avg_factor > 1.0 and zone_dict[outcome] == 0.0:
                        zone_dict[outcome] = bat_avg_factor * ( min(zone_dict.values()) )
                        
                    elif bat_avg_factor > 1.0:
                        zone_dict[outcome] = (bat_avg_factor ** difficulty_mult) * zone_dict.get(outcome)

                    # If this is a bad batter, reduce batter-favored outcomes by the factor
                    elif bat_avg_factor < 1.0:
                        # Use max() to prevent a negative value
                        zone_dict[outcome] = max(0, zone_dict.get(outcome) * bat_avg_factor)
        
        # Normalize values so they all add up to 100% (make sure they're floats)
        zone_prob_sum = 0
        # Get the sum of all values
        for value in zone_dict.values():
            zone_prob_sum += float(value)
        # Update the values to standardized values
        for key in zone_dict.keys():
            zone_dict[key] = float(zone_dict[key]) * 100 / zone_prob_sum
        
        # Create a Pitch object and return it
        return Pitch(pitch_type, zone, zone_dict)


