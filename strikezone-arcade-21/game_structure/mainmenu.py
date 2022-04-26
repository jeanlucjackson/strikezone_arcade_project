#!/usr/bin/env python3

"""The MainMenu class creates and displays a menu for the game
so that the user may select from different options. Currently,
the Main Menu let's the user [1] Play the game and [2] Learn
how the game's engine works."""


# -------------------- Import Modules -------------------- #
from os import system

from game_structure.loadgame import create_pitchers
from game_structure.loadgame import create_baseball_teams
from game_structure.baseballgame import BaseballGame
from game_structure.plateappearance import PA_outcome_scoring_dict
from players.batter import Batter






# -------------------- MainMenu Class -------------------- #

class MainMenu:
    """This class creates and displays a Main Menu for the game."""

    def __init__(self):

        # Enter user input loop
        menu_options = ['1', '2']
        recent_score = 0

        while True:
            # Clear console for prettier printing
            system('clear')
            
            # Print Main Menu header
            print()
            print()
            print("------------------- STRIKEZONE: ARCADE '21 -------------------")
            print()
            print()
            print("------ Game Menu ------")
            print()
            print("1: Take the Mound (Play Game)")
            print()
            print("2: Game Information")
            print()
            print()
            print('Press q to quit the game.')
            print()
            print()
            if recent_score != 0:
                print(f"Last Player Score: {recent_score}")
                print()
                print()

            # Ask user for input command
            command = input("Input a menu option: ")
            print()

            # Case: User quits
            if command.lower() in ['q', 'quit', 'exit']:
                print()
                print("Thank you for playing!")
                print()
                quit()

            # Case: User provides invalid input
            elif not command.lower() in menu_options:
                print("Please provide a valid command.")
                print()

            # Case: User provides menu option
            else:
                # 1 Case: Begin game
                if command.lower() == '1':
                    
                    # Select a pitcher to use
                    pitchers = create_pitchers()
                    print()
                    print("Pick a pitcher to pitch as:")
                    for pitcher in pitchers:
                        print(pitcher)
                    print()

                    # Validating Loop
                    while True:
                        print()
                        command = input("Input pitcher name (e.g. Clayton Kershaw) (q to quit): ")
                        
                        # Case: User quits to main menu
                        if command.lower() in ['q', 'quit', 'exit']:
                            # Break to return to main menu
                            print()
                            break
                        
                        # Case: Game setup continues
                        elif command.strip().lower().title() in pitchers.keys():
                            player_pitcher = pitchers[command.strip().lower().title()]

                            # Load baseball teams to pitch against
                            teams = create_baseball_teams()
                            print()
                            print("Pick a team to pitch against:")
                            for team in teams:
                                print(team)
                            print()
                            
                            # Validating loop
                            while True:
                                print()
                                command = input("Input team city and name (e.g. Seattle Mariners) (q to quit): " )
                                
                                # Case: User quits to main menu
                                if command.lower() in ['q', 'quit', 'exit']:
                                    # Break to return to main menu
                                    print()
                                    break

                                # Case: Game setup continues
                                elif command.strip().lower().title() in teams.keys():
                                    player_opponent = teams[command.strip().lower().title()]
                                    print()
                                    # !!! Pitcher and Team is setup, so let's begin our game!
                                    # Tell the user:
                                    print(f'Beginning game as {player_pitcher.first_name} {player_pitcher.last_name} against {player_opponent}!')
                                    
                                    # Begin BaseballGame!
                                    baseballgame = BaseballGame(player_pitcher, player_opponent)
                                    # BaseballGame returns 'quit' if user quits before begins
                                    if baseballgame == 'quit':
                                        break
                                    else:
                                        recent_score = baseballgame.play_ball()
                                        # Return to Main Menu when game is over
                                        break

                                # Case: User provides invalid input
                                else:
                                    print("Press enter to continue.")

                            # Break if we've reached this point
                            break

                        # Case: User provides invalid input
                        else:
                            print("Please provide a valid command.")


                # 2 Case: Show information about this game
                elif command.lower() == '2':
                    print()
                    print("StrikeZone: Arcade '21")
                    print()
                    print("""
                    This game lets the player pitch as a major league pitcher. Players input the pitch type and
                    which zone in the strikezone to place the pitch, then the program probabilistically determines the
                    outcome of the pitch. The program uses Statcast data to determine the outcome probabilities. Statcast
                    data is saved in a matrix composed of dictionaries, holding probabilies of different outcomes
                    per pitch type and pitch zone for each pitcher.
                    
                    Pitch outcomes include:
                    - Called Strike
                    - Swinging Strike
                    - Ball
                    - Foul Ball
                    - In Play Out
                    - Single
                    - Double
                    - Triple
                    - Homerun
                    - Hit By Pitch
                    
                    The batter's batting average is compared against the league average, then batter-friendly outcomes
                    such as base hits are adjusted accordingly. Good batters have their chances increased of getting these
                    batter-friendly outcomes.""")
                    print()

                    # User input to continue
                    input("Press enter to continue.")

                    print()
                    print("""
                    Let's play out an example to demonstrate.
                    You're pitching as Clayton Kershaw, facing batter Kyle Seager:""")
                    
                    # Create Kershaw as a pitcher
                    pitchers = create_pitchers()
                    pitcher = pitchers['Clayton Kershaw']
                    # Create Seager as a batter
                    batter = Batter(None, 'Kyle', 'Seager', 'Seatte', 'Mariners', '3B', 0.212)
                    print(f"""
                    Pitcher: {pitcher}
                    Batter:  {batter}""")

                    print("""
                    You want to pitch a Fastball in Zone 3, so you input: F3

                    Clayton Kershaw takes this command and returns the following dictionary holding
                    probabilities of different outcomes due to a Fastball in Zone 3:""")
                    print()
                    # Have Kershaw create a Pitch object
                    pitch_example = pitcher.pitch('Fastball', 'zone3', batter)
                    for out,prob in pitch_example.zone_dict.items():
                        print(f"""
                        {out}: {prob:.2f}""")

                    # User input to continue
                    print()
                    input("Press enter to continue.")

                    # Present an explanation of ranges and then the outcome scores
                    print("""
                    A random number is then selected and, if this number falls into one of these probability ranges,
                    that outcome is selected. The program also includes a visualization of the strikezone,
                    Player Scoring, and Mound Visits, among other game features.""")
                    print("""
                    Outcomes are scored as such:""")
                    print()
                    for outcome in PA_outcome_scoring_dict:
                        print(f"""
                        {outcome}: {PA_outcome_scoring_dict[outcome]}""")
                    print()
                    print("""
                    Thank you for playing!""")
                    print()
                    print()
                    input("Press enter to return to Main Menu.")

                else:
                    break