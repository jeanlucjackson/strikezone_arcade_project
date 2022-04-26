#!/usr/bin/env python3

"""The PlateAppearance module contains the information related to
the current interaction between this Batter and the Pitcher.
It also scores the PA outcomes based on a scoring dictionary."""


# -------------------- Import Modules -------------------- #
from os import system
import time

from game_structure.strikezone import StrikeZone
from game_structure.strikezoneexceptions import PitchTypeError


# -------------------- Initialize Global Variables -------------------- #

# Scoring dictionary for Plate Appearance outcomes
PA_outcome_scoring_dict = {
                            # Batter-friendly outcomes = negative points
                            "Single": -1000,
                            "Double": -2000,
                            "Triple": -3000,
                            "Homerun": -6000,
                            "Hit By Pitch": -1500,
                            "Walk": -1000,
                            # Pitcher-friendly outcomes = positive points
                            "Strikeout": 3000,
                            "In Play Out": 2000
                            }






# -------------------- PlateAppearance Class -------------------- #

class PlateAppearance:
    """The PlateAppearance class manages the interaction between the 
    Pitcher and the current Batter. It keeps track of the pitches that 
    have been thrown (the count) and their outcomes; it updates the 
    StrikeZone object to display past pitches to the user; and it is 
    the primary point of interaction for the user during game-mode."""

    plate_app_count = 0

    def __init__(self, Pitcher = None, Batter = None, player_score = 0, mound_visits = 2, outcome_history = []):
        
        # Validate parameters first
        if Pitcher is None or Batter is None:
            print("Please provide valid Pitcher and Batter.")
            return None
        else:
            # Increment count of plate appearances
            PlateAppearance.plate_app_count += 1

            # Initialize players
            self.pitcher = Pitcher
            self.batter = Batter
            self.pitch_decode = {'F': 'Fastball', 'O': 'Offspeed', 'B': 'Breaking'}

            # Continue player score and outcome history
            self.player_score = player_score
            self.game_outcome_history = outcome_history

            # Initialize trackers
            self.the_count = [0, 0] # The Balls & Strikes for this At Bat
            self.pitch_history = [] # List of Pitch objects in order delivered
            self.pitch_outcome_history = [] # List of outcome strings in order they occurred
            self.mound_visits = mound_visits

            # Strikezone objects and strings
            self.strikezone = StrikeZone() # initiate an empty strike zone when batter-up
            self.strikezone_big_legend = self.strikezone.get_a_strikezone('zones', 'string')
            self.strikezone_small_legend = self.strikezone.get_a_strikezone('legend', 'string')

            # Outcome of Plate Appearance
            self.PA_outcome = ''

    def at_bat(self):
        """This method runs the interactive at bat sequence, fetching a Pitch from
        the Pitcher based on the user's input then passing this Pitch to the Batter
        and updating the game state based on the outcome."""

        # Begin main while loop
        while True:
            # Clear the console
            system('clear')
        
            # Print the At Bat Header string
            self.display_at_bat()
            
            # Prompt user for pitch command
            command = input('Please provide a pitch command (q to quit): ')
            
            # Case: User quits
            if command.lower() in ['', 'q', 'quit', 'exit']:
                # Send return code to BaseballGame class above
                return 'quit'
            
            # Try user's command
            else:
                proceed = False

                # Validate command input
                try:
                    command_pitch_code = self.pitch_decode[command[0].upper()]
                    command_pitch_zone = int(command[1:])
                    proceed = True

                except:
                    print("Please provide a valid pitch command.")

                # Try to pitch the inputted Pitch
                if proceed:
                    try:
                        the_pitch = self.pitcher.pitch(command_pitch_code,
                                                        'zone' + str(command_pitch_zone),
                                                        self.batter)
                        
                        # Announce that the pitcher is pitching
                        time.sleep(0.5)
                        print()
                        print("The wind up... ", end='', flush=True)
                        time.sleep(0.25)
                        print("and the pitch!", flush=True)
                        
                        # Get outcome from the batter
                        time.sleep(1)
                        pitch_outcome = self.batter.get_pitch_outcome(the_pitch)
                        print(f"\nPitch resulted in a {pitch_outcome}.")
                        
                        # Update the pitch and outcome histories
                        self.pitch_history.append(the_pitch)
                        self.pitch_outcome_history.append(pitch_outcome)

                        # Evaluate the outcome and update game status accordingly

                        # Case: Strike, Ball, or Foul Ball
                        if pitch_outcome in ["Called Strike", "Swinging Strike", "Ball", "Foul Ball"]:
                            # Update the strikezone
                            self.strikezone.update_strikezone(the_pitch, pitch_outcome)
                            

                            # Update the Count and then the PA_outcome if one is triggered:

                            # If it's a Ball
                            if pitch_outcome in ["Ball"]:
                                self.the_count[0] += 1
                                
                                # If this Ball results in a walk, set the PA_outcome and end PA
                                if self.the_count[0] == 4:
                                    self.PA_outcome = "Walk"
                                    break
                            
                            # If it's a true Strike
                            elif pitch_outcome in ["Called Strike", "Swinging Strike"]:
                                self.the_count[1] += 1

                                # If this Strike results in a strikeout, set the PA_outcome and end PA
                                if self.the_count[1] == 3:
                                    self.PA_outcome = "Strikeout"
                                    break

                            # If it's a Foul Ball
                            elif pitch_outcome in ["Foul Ball"]:
                                # Increment Strikes if there are less than 2
                                if self.the_count[1] < 2:
                                    self.the_count[1] += 1
                                else:
                                    # Foul Balls cannot result in a strikeout
                                    pass
                        
                        # Case: Base Hit
                        elif pitch_outcome in ["Single", "Double", "Triple", "Homerun", "Hit By Pitch"]:
                            # Base Hit results end the Plate Appearance.
                            # Set the PA_outcome and end the PA
                            self.PA_outcome = pitch_outcome
                            break
                        
                        # Case: In Play Out
                        elif pitch_outcome in ["In Play Out"]:
                            # An in play out ends the Plate Appearance.
                            # Set the PA_outcome and end the PA
                            self.PA_outcome = pitch_outcome
                            break
                    
                    except PitchTypeError:
                        print(f"{self.pitcher.first_name} {self.pitcher.last_name} does not have that pitch type.")
                        time.sleep(3)
                        continue
                    except Exception as err:
                        print(f"An error occurred during the At Bat: {type(err)} {err}")
                        time.sleep(3)
                        continue
                
                # Rest before presenting the updated strikezone
                time.sleep(2.5)


    def score_at_bat(self):
        """This method scores this PlateAppearance's outcome based on the global scoring dictionary.
        It returns a dictionary with the outcome and an integer score based on this object's PA_outcome."""
        try:
            self.player_score = PA_outcome_scoring_dict[self.PA_outcome]
            return {'outcome': self.PA_outcome, 'score': self.player_score}
        except:
            return {}
    
    def display_at_bat(self):
        """This method prints the common header during an at bat.
        The header reports the following information to the user:
         - Player Score
         - Pitch History
         - Outcome History
         - The Count
         - And a mini legend of the strike zone after the first pitch has been thrown"""
        

        # Game Information
        print("\n----------------- BASEBALL GAME INFO -----------------")
        print()

        # Report Player Score and Pitcher Info
        print(f"Player Score: {self.player_score}")
        print(f"Mound Visits Remaining: {self.mound_visits}")
        print()
        print(f"Pitching as: {self.pitcher}")
        print(f"Pitch Types Available:", ' '.join(self.pitcher.pitch_types))
        print()
        print(f"Batters Faced: {len(self.game_outcome_history)}")
        print(f"Game Outcome History: {self.game_outcome_history}")
        print()
        
        # Information for this At Bat
        print()
        print("-------------------- AT BAT INFO --------------------")
        print()
        print()
        print(f"Up to bat: {self.batter} - Bat Avg: {self.batter.bat_avg}")
        print()
        # Report recent pitches from end of Pitch History
        print("  Pitch History: ", self.pitch_history)

        # Report recent outcomes from end of Outcome History
        print("Outcome History: ", self.pitch_outcome_history)
        print("\n")

        # Report the Count
        print(f"Count: {self.the_count[0]} balls   (0's)")
        print(f"       {self.the_count[1]} strikes (X's)")

        # If a pitch has been thrown, display the strikezone and a small zone legend below
        if self.the_count[0] > 0 or self.the_count[1] > 0:
            print(self.strikezone)
            print(self.strikezone_small_legend)
        # If a pitch has not been thrown display a large zone legend
        elif self.the_count[0] == 0 and self.the_count[1] == 0:
            print()
            print("                     Zone Legend:", end='')
            print(self.strikezone_big_legend)
            print("\n-------------------- USER INPUTS --------------------")
            print('\n')

        # Show how inputs work
        print("Command format: [pitch][zone]")
        print("            ex: F2, B12")
        print()

        # Show pitch options to user
        print("Pitch codes:  ", end='')
        for k in self.pitch_decode:
            print(k + ': ' + self.pitch_decode[k], end=' ')
        print()
        print("      Zones:  1 - 14")
        print("\n")