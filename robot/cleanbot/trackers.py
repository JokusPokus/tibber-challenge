"""
Tracker classes for robot cleaning jobs.
"""
import bisect
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Vertex:
    """Represents a vertex in the 2D office grid."""
    x: int
    y: int

    def update(self, direction: str, steps: int) -> None:
        """Update the vertex based on the given direction and number of steps.
        """
        if direction == 'north':
            self.y += steps
        elif direction == 'south':
            self.y -= steps
        elif direction == 'east':
            self.x += steps
        elif direction == 'west':
            self.x -= steps
        else:
            raise ValueError(f'Invalid direction: {direction}')


class CleanedRange:
    """Represents a range of a row's x coordinates that have been cleaned."""
    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    @property
    def total(self) -> int:
        return self.end - self.start + 1

    def __lt__(self, other) -> bool:
        return (self.start, self.end) < (other.start, other.end)

    def overlaps_with(self, other) -> bool:
        return (self.start <= other.start <= self.end) \
               or (self.start <= other.end <= self.end)

    def merge_with(self, other) -> None:
        self.start = min(self.start, other.start)
        self.end = max(self.end, other.end)


class Row:
    """Represents a row in the 2D office grid."""
    def __init__(self):
        self.c_ranges = []

    def add_cleaned_range(self, start: int, end: int) -> None:
        """Update the row's cleaned ranges.

        If the given range overlaps with an existing range, the existing range
        is extended to include the new range.
        """
        new_c_range = CleanedRange(start, end)

        # Find the insertion index for new_c_range such that
        # self.cleaned_ranges remains sorted
        index = bisect.bisect_left(self.c_ranges, new_c_range)

        # If the given range overlaps with an existing range, extend the
        # existing range to include the new range.
        left_merged = right_merged = False
        if index > 0:
            next_lower = self.c_ranges[index - 1]
            if new_c_range.overlaps_with(next_lower):
                next_lower.merge_with(new_c_range)
                left_merged = True

        if index < len(self.c_ranges):
            next_higher = self.c_ranges[index]
            if new_c_range.overlaps_with(next_higher):
                next_higher.merge_with(new_c_range)
                right_merged = True

        if right_merged and left_merged:
            # Two pre-existing ranges now overlap and need to be merged
            next_lower.merge_with(next_higher)
            self.c_ranges.pop(index)

        elif not right_merged and not left_merged:
            self.c_ranges.insert(index, new_c_range)

    def get_num_of_cleaned_vertices(self) -> int:
        """Return the number of vertices in the row that have been cleaned."""
        return sum(c_range.total for c_range in self.c_ranges)


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
        """Move the robot in the specified direction and number of steps.

        Update the robot's position and record the cleaned vertices. Increment
        the number of unique vertices that have been cleaned.
        """

        self.robot_position.update(direction, steps)


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
