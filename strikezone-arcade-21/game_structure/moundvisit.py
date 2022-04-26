#!/usr/bin/env python3

"""The MoundVisit module creates an interaction with the Manager.
It presents different messages depending on how many MoundVisits
are left, and provides a reason if one is passed as an argument."""


# -------------------- Import Modules -------------------- #
import time






# -------------------- MoundVisit Class -------------------- #

class MoundVisit:
    """The MoundVisit class is initialized with a Pitcher object, 
    the player's score, the MoundVisits remaining, and an optional
    reason string. This information is used to present customized
    messages about why the manager is performing a mound visit."""
    
    def __init__(self, pitcher, player_score, visits_remaining, reason='your performance'):
        self.pitcher = pitcher
        self.player_score = player_score
        self.remaining = visits_remaining
        self.reason = reason

        if self.remaining == 3:
            self.manager_pep_talk(reason)
            input('Press enter to continue.')

        elif 3 > self.remaining > 0:
            self.manager_threat(reason)
            input('Press enter to continue.')

        elif self.remaining == 0:
            self.manager_pull(reason)
            input('Press enter to continue.')

        else:
            return False

    def manager_pep_talk(self, reason):
        """This method is called for the first mound visit.
        The manager gives the pitcher a pep talk to keep playing."""

        print()
        print("Your manager is approaching for a Mound Visit!")
        time.sleep(2)
        print("Manager:")
        time.sleep(0.5)
        print(f"    Alright, {self.pitcher.first_name}, looks like you're having a rough start.")
        print(f"    I'm here because of {reason}. You still have a chance to turn things around.")
        print()
        time.sleep(3)
        print(f"    You've got this. But keep in mind that I'll pull you from the game if you don't step it up.")
        print()
        print()
        print(f"You have lost a Mound Visit. You have {self.remaining - 1} visits remaining.")
        print("Resuming game!")
        print()
        time.sleep(2)

    def manager_threat(self, reason):
        """This method is called for intermediate mound visits.
        The manager gives the pitcher a threat that they should
        improve soon or else they'll be pulled from the game."""
        
        print()
        print("Your manager is approaching for a Mound Visit!")
        time.sleep(2)
        print("Manager:")
        time.sleep(0.5)
        print(f"    Listen up, {self.pitcher.last_name}. I don't like what I'm seeing.")
        print(f"    I'm running out of patience because of {reason}.")
        time.sleep(3)
        print(f"    Pick it up. Now. You hear me? Otherwise I'll put someone else in.")
        print()
        print()
        print(f"You have lost a Mound Visit. You have {self.remaining - 1} visits remaining.")
        print("Resuming game! Good luck!")
        print()
        time.sleep(2)

    def manager_pull(self, reason):
        """This method is called when the user has played poorly
        and the manager has decided to pull the pitcher from the game.
        This will be the last message the user receives before game over."""
        
        print()
        print("Your manager is approaching for a Mound Visit...")
        time.sleep(2)
        print("Manager:")
        time.sleep(0.5)
        if self.player_score > 10000:
            print(f"    Not bad, ace. You got {self.player_score} points.")
            print(f"    You've played your part, but because of {reason} it's time to hand it over to a reliever.")
            print()
            print(f"    I'm looking forward to putting you in again soon!")
        else:
            print(f"    Okay, not your best day, {self.pitcher.last_name}. Gimme that ball.")
            print(f"    Let's hope the relieving pitcher can undo the damage done from {reason}.")
            print()
            print(f"    Better luck next time!")
        
        time.sleep(3)
        print(f"You are out of Mound Visits.")
        print()
        time.sleep(2)


