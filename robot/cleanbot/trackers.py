"""
Tracker classes for robot cleaning jobs.
"""
from collections import defaultdict
from typing import Dict, List


class CleanedRange:
    """Represents a range of vertices that have been cleaned."""
    def __int__(self, start: int, end: int):
        self.start = start
        self.end = end


class Office:
    """Represents the office space."""
    def __init__(self):
        """
        self.rows: a dictionary with each key being the y coordinate of the
            row and its value being a list of CleanedRange objects
        self.cols: a dictionary with each key being the x coordinate of the
            column and its value being a list of CleanedRange objects
        """
        self.rows = defaultdict(list)
        self.cols = defaultdict(list)


class RobotTracker:
    """
    Tracks robot cleaning job and calculates the number of vertices cleaned.
    """
    @staticmethod
    def get_num_of_cleaned_vertices(commands: List[Dict]) -> int:
        """Calculate the number of unique vertices cleaned by the robot.

        Args:
          - commands: a list of commands to be executed, with each command
            specifying the direction to move in and the number of steps.
        """
        x, y = 0, 0

        for command in commands:
            direction = command['direction']
            steps = command['steps']


