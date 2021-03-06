"""
Tracker and utility classes for robot cleaning jobs.
"""
import bisect
from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Position:
    """Represents a position on a vertex in the 2D office grid."""
    x: int
    y: int

    def update(self, direction: str, steps: int) -> None:
        """Update the position based on the given direction
        and number of steps.
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
    """Represents a range of x-coordinates within a row or y-coordinates
    within a column. Between the start and end coordinates (inclusive),
    all vertices are cleaned.
    """

    def __init__(self, start: int, end: Optional[int] = None):
        self.start = start
        self.end = start if end is None else end

    def __lt__(self, other) -> bool:
        """Make two ranges (lexicographically) comparable."""
        return (self.start, self.end) < (other.start, other.end)

    def __len__(self) -> int:
        """Return the total number of vertices within the range."""
        return self.end - self.start + 1

    def overlaps_with(self, other) -> bool:
        """Return True if this range overlaps with the other range.

        A direct adjacency (e.g., self ends at 4, other starts at 5)
        is also considered an overlap.
        """
        return (self.start <= other.start <= self.end + 1) \
            or (self.start - 1 <= other.end <= self.end)

    def merge_with(self, other) -> None:
        """Merge this range with the other range."""
        self.start = min(self.start, other.start)
        self.end = max(self.end, other.end)


class Line:
    """Represents a row or column in a 2D grid."""

    def __init__(self):
        self.c_ranges = []

    def __contains__(self, item) -> bool:
        """Return True if the given item is in any of the line's
        self.c_ranges.

        Takes advantage of the fact that self.c_ranges is sorted.
        """
        for c_range in self.c_ranges:
            if c_range.start <= item <= c_range.end:
                return True
            if c_range.start > item:
                return False
        return False

    @property
    def cleaned_coords(self) -> List[int]:
        """Return a list of the coordinates of all cleaned vertices
        within the line.

        If the line represents a row, the coordinates are the x-coordinates.
        If the line represents a column, the coordinates are the y-coordinates.
        """
        return [
            coord
            for c_range in self.c_ranges
            for coord in range(c_range.start, c_range.end + 1)
        ]

    def insert(self, new_range: CleanedRange) -> None:
        """Update the line's cleaned ranges.

        If the given range overlaps with an existing range, the existing range
        is extended to include the new range. Otherwise, the new range is
        added to the line.
        """
        # Find index for new_range to be inserted such that
        # self.cleaned_ranges remains sorted
        index = bisect.bisect_left(self.c_ranges, new_range)

        # If the given range overlaps with an existing range, extend the
        # existing range to include the new range.
        is_left_merged = is_right_merged = False
        if index > 0:
            next_lower = self.c_ranges[index - 1]
            if new_range.overlaps_with(next_lower):
                next_lower.merge_with(new_range)
                is_left_merged = True

        if index < len(self.c_ranges):
            next_higher = self.c_ranges[index]
            if new_range.overlaps_with(next_higher):
                next_higher.merge_with(new_range)
                is_right_merged = True

        if is_right_merged and is_left_merged:
            self._merge_existing_ranges(index, next_higher, next_lower)

        elif not is_right_merged and not is_left_merged:
            self.c_ranges.insert(index, new_range)

    def get_num_of_cleaned_vertices(self) -> int:
        """Return the number of vertices in the line that have been cleaned."""
        return sum(len(c_range) for c_range in self.c_ranges)

    def _merge_existing_ranges(self, index, next_higher, next_lower) -> None:
        """Merge two existing ranges and delete the larger one to prevent
        redundancies.
        """
        next_lower.merge_with(next_higher)
        self.c_ranges.pop(index)


class Office:
    """Represents the office space as a 2D grid of vertices through which
    the robot can be moved.
    """

    def __init__(self):
        """
        self.robot_position: the robot's current position within the 2D grid,
            initialized (w.l.o.g.) to the origin.
        self.rows: a dictionary with each key being the y coordinate of the
            row and its value being a Line instance
        self.cols: a dictionary with each key being the x coordinate of the
            col and its value being a Line instance
        """
        self.robot_position = Position(0, 0)
        self.rows = defaultdict(Line)
        self.cols = defaultdict(Line)

        # Add starting position
        self.rows[0].insert(CleanedRange(0))
        self.cols[0].insert(CleanedRange(0))

    def move_robot(self, direction: str, steps: int) -> None:
        """Move the robot in the specified direction and number of steps.

        Update the robot's position and record the cleaned vertices.
        """
        self._add_range_to_line(direction, steps)
        self.robot_position.update(direction, steps)

    def _add_range_to_line(self, direction: str, steps: int) -> None:
        """Calculate a CleanedRange instance based on the direction and
        add it to the appropriate line.
        """
        c_range = self._get_range_for(direction, steps)

        if direction in ['east', 'west']:
            self.rows[self.robot_position.y].insert(c_range)
        else:
            self.cols[self.robot_position.x].insert(c_range)

    def _get_range_for(self, direction: str, steps: int) -> CleanedRange:
        """Calculate a CleanedRange instance based on the direction and
        number of steps.
        """
        if direction == 'east':
            start = self.robot_position.x
            end = self.robot_position.x + steps
        elif direction == 'west':
            start = self.robot_position.x - steps
            end = self.robot_position.x
        elif direction == 'north':
            start = self.robot_position.y
            end = self.robot_position.y + steps
        else:
            start = self.robot_position.y - steps
            end = self.robot_position.y

        return CleanedRange(start, end)


class RobotTracker:
    """Tracks robot cleaning jobs and calculates the number
    of vertices cleaned.
    """

    def __init__(self):
        self.office = Office()

    def get_num_of_cleaned_vertices(self, commands: List[Dict]) -> int:
        """Calculate the number of unique vertices cleaned by the robot.

        Args:
          - commands: a list of commands to be executed, with each command
            specifying the direction to move in and the number of steps.
        """
        for command in commands:
            self.office.move_robot(
                direction=command['direction'],
                steps=command['steps']
            )

        return self._row_total + self._col_total

    @property
    def _row_total(self) -> int:
        """Calculate the total number of cleaned vertices recorded in the
        office's rows."""
        return sum(
            row.get_num_of_cleaned_vertices()
            for row in self.office.rows.values()
        )

    @property
    def _col_total(self) -> int:
        """Calculate the total number of cleaned vertices recorded in the
        office's columns, minus the ones that are also recorded in the
        office's rows.
        """
        return sum(
            self._unique_vertices_in_column(col, x)
            for x, col in self.office.cols.items()
        )

    def _unique_vertices_in_column(self, col: Line, x: int) -> int:
        return sum(
            1 for y in col.cleaned_coords if x not in self.office.rows[y]
        )


class SimpleRobotTracker:
    """Naive implementation of a RobotTracker. Will be very slow for large
    problems.
    """

    @staticmethod
    def get_num_of_cleaned_vertices(commands: List[Dict]) -> int:
        """Calculate the number of unique vertices cleaned by the robot.

        Save the coordinates of visited vertices in a set and add every
        single unique vertex the robot passes. The final result is the length
        of the set after the robot has finished.
        """
        robot_pos = Position(0, 0)

        visited = {(0, 0)}

        for command in commands:
            direction, steps = command['direction'], command['steps']

            if direction == 'east':
                places = {
                    (robot_pos.x + i, robot_pos.y)
                    for i in range(1, steps + 1)
                }
            elif direction == 'west':
                places = {
                    (robot_pos.x - i, robot_pos.y)
                    for i in range(1, steps + 1)
                }
            elif direction == 'north':
                places = {
                    (robot_pos.x, robot_pos.y + i)
                    for i in range(1, steps + 1)
                }
            else:
                places = {
                    (robot_pos.x, robot_pos.y - i)
                    for i in range(1, steps + 1)
                }

            visited |= places
            robot_pos.update(direction, steps)

        return len(visited)
