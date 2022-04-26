#!/usr/bin/env python3

"""The StrikeZone module handles the visual displaying of a
strike zone (modeled after a real-life strike zone with zones
per Statcast). An empty StrikeZone is loaded from a text file,
as are the two legend representations."""


# -------------------- Import Modules -------------------- #
import os.path


# -------------------- Initialize Global Variables -------------------- #

strikezone_dir = 'data/strikezone/'
strikezone_filepath = os.path.join( os.path.split(os.path.dirname(__file__))[0] , strikezone_dir )





# -------------------- StrikeZone Class -------------------- #

class StrikeZone:
    """The StrikeZone class handles the string representation of
    the strike zone for this plate appearance/at bat. A blank string
    is loaded from a txt file in the data/strikezone folder and then
    converted to a list of strings from there on. This class can
    return a string or a list of strings, see get_a_strikezone() below."""

    def __init__(self):
        # Saving coordinates for updating the string representation
        # Padding is the blank lines / blank spaces before each row / col in the strikezone txt files
        self.row_pad = 0
        self.col_pad = 8
        self.O_rows = {'zone1': self.row_pad + 5, 'zone2': self.row_pad + 5, 'zone3': self.row_pad + 5,
                        'zone4': self.row_pad + 8, 'zone5': self.row_pad + 8, 'zone6': self.row_pad + 8,
                        'zone7': self.row_pad + 11, 'zone8': self.row_pad + 11, 'zone9': self.row_pad + 11,
                        'zone11': self.row_pad + 2, 'zone12': self.row_pad + 2,
                        'zone13': self.row_pad + 14, 'zone14': self.row_pad + 14
                        }
        self.O_cols = {'zone1': self.col_pad + 11, 'zone4': self.col_pad + 11, 'zone7': self.col_pad + 11,
                        'zone2': self.col_pad + 18, 'zone5': self.col_pad + 18, 'zone8': self.col_pad + 18,
                        'zone3': self.col_pad + 25, 'zone6': self.col_pad + 25, 'zone9': self.col_pad + 25,
                        'zone11': self.col_pad + 3, 'zone13': self.col_pad + 3,
                        'zone12': self.col_pad + 33, 'zone14': self.col_pad + 33}
        self.X_rows = {zone: self.O_rows[zone] + 1 for zone in self.O_rows}
        self.X_cols = {zone: self.O_cols[zone] for zone in self.O_cols}

        # Dictionary that holds count of balls and strikes in each zone
        self.zone_OXs = {'zone' + str(i) : {'balls': 0, 'strikes': 0}
                        for i in [1,2,3,4,5,6,7,8,9,11,12,13,14]}

        # Initialize with blank strike zone
        self.strikezone = self.get_a_strikezone('blank')

    @classmethod
    def get_a_strikezone(self, version='blank', style='list'):
        """This is a class method that loads a version of the strike zone string from a text file.
        The version parameter can be: 'blank', 'zones', legend' 
        and is 'blank' by default.
        It can return either a single 'string' or a 'list' of strings depending on the 'style' parameter."""

        if style.lower() == 'string':
            strikezone = ''
        elif style.lower() == 'list':
            strikezone = []

        try:
            strikezone_txt_filename = strikezone_filepath + 'strikezone_' + str(version) + '.txt'
            with open(strikezone_txt_filename, 'rt') as infile:
                for line in infile:
                    if style.lower() == 'string':
                        strikezone += line
                    elif style.lower() == 'list':
                        strikezone.append(line)

            return strikezone

        except FileNotFoundError:
            print(f'File {strikezone_txt_filename} not found.')
        except Exception as err:
            print(f'An error occured while loading {version} strikezone: {type(err)} {err}')

    def update_strikezone(self, pitch, pitch_outcome):
        """This method updates the strike zone based on the pitch that was just pitched
        as well as the outcome that occurred based on the Batter handling the pitch.
        pitch = Pitch object
        pitch_outcome = string representation of outcome, e.g. "Called Strike", "Homerun" """

        # Fetch the zone where the ball was pitched from the passed Pitch object
        zone_pitched = pitch.zone.lower()

        # Case: Strike
        if pitch_outcome in ['Called Strike', 'Swinging Strike', 'Foul Ball']:
            self.zone_OXs[zone_pitched]['strikes'] = self.zone_OXs[zone_pitched].get('strikes') + 1
            
            # Update string representation to report how many STRIKES have been thrown in that zone
            row_str = self.strikezone[self.X_rows[zone_pitched]]
            row_str = row_str[:self.X_cols[zone_pitched]] \
                        + 'X' \
                        + str(self.zone_OXs[zone_pitched]['strikes']) \
                        + row_str[(self.X_cols[zone_pitched] + 2):]
            self.strikezone[self.X_rows[zone_pitched]] = row_str
        
        # Case: Ball
        elif pitch_outcome in ['Ball', 'Hit By Pitch']:
            self.zone_OXs[zone_pitched]['balls'] = self.zone_OXs[zone_pitched].get('balls') + 1

            # Update string representation to report how many BALLS have been thrown in that zone
            row_str = self.strikezone[self.O_rows[zone_pitched]]
            row_str = row_str[:self.O_cols[zone_pitched]] \
                        + 'O' \
                        + str(self.zone_OXs[zone_pitched]['balls']) \
                        + row_str[(self.O_cols[zone_pitched] + 2):]
            self.strikezone[self.O_rows[zone_pitched]] = row_str

        # Case: something else happened that doesn't affect the strikezone, like a base hit
        else:
            pass

    def __str__(self):
        s = ''
        for line in self.strikezone:
            s += line
        return s

    def __repr__(self):
        s = ''
        for line in self.strikezone:
            s += line
        return s

