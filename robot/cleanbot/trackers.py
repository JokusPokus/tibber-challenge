"""
Tracker and utility classes for robot cleaning jobs.
"""
from typing import Dict, List

from .offices import Office, TwoDimPosition


class RobotTracker:
    """Tracks robot cleaning jobs and returns the number
    of vertices cleaned.
    """

    def __init__(self, office: Office):
        self.office = office

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

        return self.office.num_cleaned_vertices


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
        robot_pos = TwoDimPosition(0, 0)

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
