#!/usr/bin/env python3

"""The BaseballTeam module stores baseball Player objects
and the team's city & name for easy, containerized access."""






# -------------------- BaseballTeam Class -------------------- #

class BaseballTeam:
    """The BaseballTeam class holds baseball Players in their
    batting order. Initialization requires a City, Team Name, 
    and a list of Player objects."""
    
    num_of_teams = 0

    def __init__(self, team_city='?', team_name='?', players=[]):
        # Increment number of teams
        BaseballTeam.num_of_teams += 1
        self.team_city = team_city
        self.team_name = team_name
        self.players = players

    def __str__(self):
        return f"{self.team_city} {self.team_name}"

    def __repr__(self):
        return f"{self.team_city} {self.team_name}"
