"""
Tracker classes for robot cleaning jobs.
"""
from typing import Dict, List


class RobotTracker:
    """
    Tracks robot cleaning job and calculates the number of vertices cleaned.
    """
    @staticmethod
    def get_num_of_cleaned_vertices(start: Dict, commands: List[Dict]) -> int:
        """Calculate the number of unique vertices cleaned by the robot.

        Args:
          - start: a dictionary holding x and y coordinates of the
            robot's starting position
          - commands: a list of commands to be executed, with each command
            specifying the direction to move in and the number of steps.
        """
        x, y = start['x'], start['y']

        return 0
