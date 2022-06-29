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
        return (self.start <= other.start <= self.end + 1) \
               or (self.start - 1 <= other.end <= self.end)

    def merge_with(self, other) -> None:
        self.start = min(self.start, other.start)
        self.end = max(self.end, other.end)


class Line:
    """Represents a row or column in the 2D office grid."""

    def __init__(self):
        self.c_ranges = []

    def __contains__(self, item) -> bool:
        for c_range in self.c_ranges:
            if c_range.start <= item <= c_range.end:
                return True
            if c_range.start > item:
                return False
        return False

    @property
    def members(self) -> List[int]:
        """Return a list of all cleaned coordinates within the line."""
        return [
            coord
            for c_range in self.c_ranges
            for coord in range(c_range.start, c_range.end + 1)
        ]

    def add_cleaned_range(self, new_range: CleanedRange) -> None:
        """Update the line's cleaned ranges.

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
        """Return the number of vertices in the line that have been cleaned."""
        return sum(c_range.total for c_range in self.c_ranges)

    def _merge_existing_ranges(self, index, next_higher, next_lower) -> None:
        next_lower.merge_with(next_higher)
        self.c_ranges.pop(index)


class Office:
    """Represents the office space."""

    def __init__(self):
        """
        self.robot_position: the robot's current position within the 2D grid

        self.rows: a dictionary with each key being the y coordinate of the
            row and its value being a Line instance
        self.cols: a dictionary with each key being the x coordinate of the
            col and its value being a Line instance
        """
        self.robot_position = Vertex(0, 0)
        self.rows = defaultdict(Line)
        self.cols = defaultdict(Line)

        self.rows[0].add_cleaned_range(CleanedRange(0))
        self.cols[0].add_cleaned_range(CleanedRange(0))

    def move_robot(self, direction: str, steps: int) -> None:
        """Move the robot in the specified direction and number of steps.

        Update the robot's position and record the cleaned vertices.
        """
        self._add_range_to_single_row(direction, steps)
        self.robot_position.update(direction, steps)

    def _add_range_to_single_row(self, direction: str, steps: int) -> None:
        c_range = self._get_range(direction, steps)

        if direction in ['east', 'west']:
            self.rows[self.robot_position.y].add_cleaned_range(c_range)
        else:
            self.cols[self.robot_position.x].add_cleaned_range(c_range)

    def _get_range(self, direction, steps) -> CleanedRange:
        if direction == 'east':
            c_range = CleanedRange(
                self.robot_position.x,
                self.robot_position.x + steps
            )
        elif direction == 'west':
            c_range = CleanedRange(
                self.robot_position.x - steps,
                self.robot_position.x
            )
        elif direction == 'north':
            c_range = CleanedRange(
                self.robot_position.y,
                self.robot_position.y + steps
            )
        else:
            c_range = CleanedRange(
                self.robot_position.y - steps,
                self.robot_position.y
            )
        return c_range


class RobotTracker:
    """Tracks robot cleaning jobs and calculates the number
    of vertices cleaned.
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
            office.move_robot(
                direction=command['direction'],
                steps=command['steps']
            )

        return RobotTracker._row_total_of(office) \
            + RobotTracker._col_total_of(office)

    @staticmethod
    def _row_total_of(office: Office) -> int:
        """Calculate the total number of cleaned vertices recorded in the
        office's rows."""
        return sum(
            row.get_num_of_cleaned_vertices()
            for row in office.rows.values()
        )

    @staticmethod
    def _col_total_of(office: Office) -> int:
        """Calculate the total number of cleaned vertices recorded in the
        office's columns, minus the ones that are also recorded in the
        office's rows.
        """
        total = 0
        for x, col in office.cols.items():
            total += RobotTracker._unique_vertices_in_column(col, office, x)

        return total

    @staticmethod
    def _unique_vertices_in_column(col, office, x):
        return sum(
            1 for y in col.members if x not in office.rows[y]
        )
