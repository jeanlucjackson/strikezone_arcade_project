#!/usr/bin/env python3

"""This module holds the Exceptions used in the StrikeZone game."""

class PitchTypeError(Exception):
    """Indicates that this Pitch Type is not in this Pitcher's repertoire."""
    def __init__(self):
        self.message = f"Pitch Type not in this Pitcher's repertoire."

    def __str__(self):
        return self.message