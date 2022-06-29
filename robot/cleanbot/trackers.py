"""
Tracker classes for robot cleaning jobs.
"""
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Vertex:
    """Represents a vertex in the 2D office grid."""
    x: int
    y: int


class CleanedRange:
    """Represents a range of vertices that have been cleaned."""
    def __int__(self, start: int, end: int):
        self.start = start
        self.end = end


class Office:
    """Represents the office space."""
    def __init__(self, robot_position: Optional[Vertex] = None):
        """
        self.robot_position: the robot's current position within the 2D grid

        self.rows: a dictionary with each key being the y coordinate of the
            row and its value being a list of CleanedRange objects

        self.num_unique_vertices: the number of unique vertices that have
            been cleaned so far
        """
        self.robot_position = robot_position or Vertex(0, 0)
        self.rows = defaultdict(list)
        self.num_unique_vertices = 0

    def move_robot(self, direction: str, steps: int) -> None:
        """Move the robot in the specified direction and number of steps."""
        pass


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
        office = Office()

        for command in commands:
            direction = command['direction']
            steps = command['steps']

            office.move_robot(direction, steps)

        return office.num_unique_vertices
