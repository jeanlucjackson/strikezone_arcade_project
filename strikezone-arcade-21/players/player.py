#!/usr/bin/env python3

"""The Player module creates the base-level version of a
baseball player, modeled after a real-life athlete. They
have no built-in functionality but are built-upon by
other modules."""






# -------------------- Player Class -------------------- #

class Player:
    """A Player's attributes include their name, their team's
    city and name, their fielding position, and their batting
    average. A Player's only methods are string representations."""
    def __init__(self, 
                first_name = "?", 
                last_name = "?", 
                team_city = "?", 
                team_name = "?",
                position = "?", 
                bat_avg = 0.000
                ):

        self.first_name = first_name
        self.last_name = last_name
        self.team_city = team_city
        self.team_name = team_name
        self.position = position
        self.bat_avg = bat_avg

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.position} for the {self.team_city} {self.team_name}"

    def __repr__(self):
        return f"{self.first_name} {self.last_name}, {self.position} for the {self.team_city} {self.team_name}"

