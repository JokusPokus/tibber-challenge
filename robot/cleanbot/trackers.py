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

    def __init__(self, start: int, end: Optional[int] = None):
        self.start = start
        self.end = end if end is not None else start

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

    def add_cleaned_range(self, new_range: CleanedRange) -> None:
        """Update the row's cleaned ranges.

        If the given range overlaps with an existing range, the existing range
        is extended to include the new range.
        """
        # Find the insertion index for new_range such that
        # self.cleaned_ranges remains sorted
        index = bisect.bisect_left(self.c_ranges, new_range)

        # If the given range overlaps with an existing range, extend the
        # existing range to include the new range.
        left_merged = right_merged = False
        if index > 0:
            next_lower = self.c_ranges[index - 1]
            if new_range.overlaps_with(next_lower):
                next_lower.merge_with(new_range)
                left_merged = True

        if index < len(self.c_ranges):
            next_higher = self.c_ranges[index]
            if new_range.overlaps_with(next_higher):
                next_higher.merge_with(new_range)
                right_merged = True

        if right_merged and left_merged:
            self._merge_existing_ranges(index, next_higher, next_lower)

        elif not right_merged and not left_merged:
            self.c_ranges.insert(index, new_range)

    def get_num_of_cleaned_vertices(self) -> int:
        """Return the number of vertices in the row that have been cleaned."""
        return sum(c_range.total for c_range in self.c_ranges)

    def _merge_existing_ranges(self, index, next_higher, next_lower) -> None:
        next_lower.merge_with(next_higher)
        self.c_ranges.pop(index)


class Office:
    """Represents the office space."""

    def __init__(self, robot_position: Optional[Vertex] = None):
        """
        self.robot_position: the robot's current position within the 2D grid

        self.rows: a dictionary with each key being the y coordinate of the
            row and its value being a Row instance
        """
        self.robot_position = robot_position or Vertex(0, 0)
        self.rows = defaultdict(Row)

    def move_robot(self, direction: str, steps: int) -> None:
        """Move the robot in the specified direction and number of steps.

        Update the robot's position and record the cleaned vertices.
        """
        if direction in ['east', 'west']:
            self._add_range_to_single_row(direction, steps)
        else:
            self._add_single_vertices_to_rows(direction, steps)

        self.robot_position.update(direction, steps)

    def _add_range_to_single_row(self, direction: str, steps: int) -> None:
        if direction == 'east':
            c_range = CleanedRange(
                self.robot_position.x,
                self.robot_position.x + steps
            )
        else:
            c_range = CleanedRange(
                self.robot_position.x - steps,
                self.robot_position.x
            )
        self.rows[self.robot_position.y].add_cleaned_range(c_range)

    def _add_single_vertices_to_rows(self, direction: str, steps: int) -> None:
        if direction == 'north':
            y_indices = range(
                self.robot_position.y + 1,
                self.robot_position.y + steps + 1
            )
        else:
            y_indices = range(
                self.robot_position.y - steps,
                self.robot_position.y
            )
        for y_index in y_indices:
            self.rows[y_index].add_cleaned_range(
                CleanedRange(self.robot_position.x)
            )


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
