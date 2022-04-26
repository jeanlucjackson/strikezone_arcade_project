#!/usr/bin/env python3

"""The BaseballGame class is modeled after a real-life baseball game
but is translated to arcade-style gameplay. It initializes the game's
objects such as baseball Players, the user's score, Mound Visits, etc.
Currently, the only method is to Play Ball, which creates a new
PlateAppearance for each batter, checks for when MoundVisits should
occur, and progresses through the game."""


# -------------------- Import Modules -------------------- #
import time

from players.batter import Batter
from game_structure.plateappearance import PlateAppearance
from game_structure.moundvisit import MoundVisit


# -------------------- BaseballGame Class -------------------- #

class BaseballGame:
    """This class manages the game progression and is modeled after a 
    real-life baseball game. After input is validated, the user's Pitcher
    is instantiated along with the opposing team's batters in their proper
    batting lineup order. Other game information such as the player's score
    and mound visits are set to starting values."""

    games_played = 0

    def __init__(self, pitcher = None, opponent = None):
        
        # Validate parameters
        if pitcher is None or opponent is None:
            print("Please provide a valid Pitcher and opposing team.")
            return None

        # Commence game
        else:
            # Initialize players
            self.pitcher = pitcher
            self.opponent = opponent
            self.batting_order = self.opponent.players
            self.batting_order_index = 0

            # Increment number of games played
            BaseballGame.games_played += 1

            # Initialize trackers
            self.outcome_history = []
            
            # Begin game with:
            # - 0 Player Points
            # - 3 Mound Visits (lives left)
            self.player_score = 0
            self.mound_visits = 3
            self.mound_visit_break = 3

            # Welcome the user to the game and bring in the game announcer
            # Begin game intro
            print()
            print('--------------------------------------------------------------------------------')
            print()
            print('"Welcome everyone to today\'s game!"')
            time.sleep(0.5)
            print(f'"Tonight we have {self.pitcher.first_name} {self.pitcher.last_name} pitching against the {self.opponent}!"\n')
            time.sleep(0.5)
            print(f'"{self.pitcher.last_name} is a real ace, we are expecting great things from him today."\n')
            print()
            print('--------------------------------------------------------------------------------')
            print()
            time.sleep(1)
            

    def play_ball(self):
        """This is the main method for the BaseballGame class. It continues the game
        until one of the end conditions is met, creating new PlateAppearances for each
        batter and keeping track of the user's points and mound visits left.
        It returns the player's score at the end of the game."""

        # Game continues until the player is out of mound visits or the user quits
        user_quit = False

        proceed = input('Press enter to continue (q to quit). ')
        # If the user quits, return False to the MainMenu so it knows how to handle
        if proceed.lower() in ['q', 'quit', 'exit']:
            user_quit = True

        # Main loop that creates new PlateAppearances for each batter
        # and updates game information like the player's score
        while True and not user_quit:
            print()
            if self.mound_visits == 0:
                print()
                print("You are out of Mound Visits")
                print("       GAME OVER!")
                print()
                print()
                print(f"Final score: {self.player_score}")
                time.sleep(3)
                print()
                print("Returning to Main Menu...")
                time.sleep(2)
                break
            else:
                
                # Loop through batting lineup
                # Batting order returns to the first batter after the last batter
                if self.batting_order_index  == len(self.batting_order):
                    self.batting_order_index = 0
                
                # Create Batter from player at this batting order index
                batter = Batter(self.batting_order[self.batting_order_index])
                self.batting_order_index += 1
                self.mound_visit_break -= 1
                print(f"Stepping up to bat: {batter.first_name} {batter.last_name}, Batting Avg: {batter.bat_avg}")
                time.sleep(2)

                # Create Plate Appearance
                this_PA = PlateAppearance(self.pitcher, batter, self.player_score, self.mound_visits, self.outcome_history)
                
                # Play through At Bat
                if this_PA.at_bat() == 'quit':
                    user_quit = True
                    break
                else:
                    # Once an outcome occurs, score it and add to player score
                    this_outcome = this_PA.score_at_bat()
                    if this_outcome != {}:
                        self.outcome_history.append(this_outcome['outcome'])
                        self.player_score += this_outcome['score']
                        print()
                        print(f"It's a {this_outcome['outcome']}! Points: {this_outcome['score']}")
                        print(f"New user score: {self.player_score}")
                        print()
                        for i in range(3,0,-1):
                            time.sleep(1)
                            print(i)
                        print("\nBatter Up!")

                # Get 4 most recent outcomes to evaluate if mound visit should occur
                recent_outcomes = self.outcome_history[-4:]
                # Count the number of base hits recently
                recent_basehits = 0
                for outcome in recent_outcomes:
                    if outcome in ['Single', 'Double', 'Triple', 'Homerun']:
                        recent_basehits += 1
                print(f"plateappearance count: {PlateAppearance.plate_app_count}")
                print(f"recent_outcomes: {recent_outcomes} - basehits: {recent_basehits}", flush=True)
                print(f"mound visit break: {self.mound_visit_break}")
                time.sleep(4)
                # --- Mound Visits
                # Once the user has seen 3 batters, begin checking for mound visits
                # "Reason" string in the form of "the base hits" or "your low score"
                if (self.mound_visit_break < 0 or 
                    recent_basehits > 2):

                    # If there have been too many base hits recently
                    if recent_basehits > 2:
                        reason = "these recent base hits"
                        mound_visit = MoundVisit(self.pitcher, self.player_score, self.mound_visits, reason)
                        self.mound_visits -= 1
                        self.mound_visit_break = 3

                    # If the user has a low score, execute mound visit
                    elif self.player_score <= 4000:
                        reason = "your low score"
                        mound_visit = MoundVisit(self.pitcher, self.player_score, self.mound_visits, reason)
                        self.mound_visits -= 1
                        self.mound_visit_break = 3
                    
                    # If the pitcher keeps hitting batters
                    elif recent_outcomes.count('Hit By Pitch') > 1:
                        reason = 'you hitting batters'
                        mound_visit = MoundVisit(self.pitcher, self.player_score, self.mound_visits, reason)
                        self.mound_visits -= 1
                        self.mound_visit_break = 3

                # After 10 batters, applaud the user
                elif PlateAppearance.plate_app_count == 10:
                    print()
                    print("Well done! You've encountered 10 batters and you're still going! Keep it up!")
                    time.sleep(3)
                    print()

                # After 20 batters, applaud the user
                elif PlateAppearance.plate_app_count == 20:
                    print()
                    print("Wow, 20 batters! How's the arm? Keep going!")
                    time.sleep(3)
                    print()

                # After 30 batters, applaud the user
                elif PlateAppearance.plate_app_count == 30:
                    print()
                    print("Woah. 30 batters. Buy me some peanuts and cracker jacks!")
                    time.sleep(3)
                    print()

        
        # If user has quit the game, let them know and return the player score to the main menu
        if user_quit:
            print()
            print("You quit the game.")
            print()
            time.sleep(1)
            print(f"Final score: {self.player_score}")
            time.sleep(3)
            print()
            print("Returning to Main Menu...")
            time.sleep(2)

        # Return player score
        return self.player_score



