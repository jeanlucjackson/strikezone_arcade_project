#!/usr/bin/env python3

"""The Pitch module saves pitch-related information in a container,
making it easier to transfer information from the Pitcher to the Batter."""






# -------------------- Pitch Class -------------------- #

class Pitch:
    """This class represents a Pitch delivered by a Pitcher.
    It holds a dictionary of pitch outcomes with their probabilities
    as created by the Pitcher for use by the Batter."""

    def __init__(self, pitch_type, zone, zone_dict):
        self.pitch_type = pitch_type
        self.zone = zone
        self.zone_dict = zone_dict

    def get_zone_outcome_probs(self):
        return self.zone_dict

    def __str__(self):
        return f"{self.pitch_type[0]}{self.zone.strip('zone')}"

    def __repr__(self):
        return f"{self.pitch_type[0]}{self.zone.strip('zone')}"
