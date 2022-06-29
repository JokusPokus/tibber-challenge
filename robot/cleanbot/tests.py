"""
Unit tests for the cleanbot package.
"""
import pytest

from .trackers import RobotTracker


COMMANDS = [
    pytest.param(
        [
            {'direction': 'north', 'steps': 1}
        ],
        2,
        id='basic'
    ),
    pytest.param(
        [
            {'direction': 'north', 'steps': 1},
            {'direction': 'south', 'steps': 1}
        ],
        2,
        id='basic_overlap'
    ),
    pytest.param(
        [
            {'direction': 'north', 'steps': 1},
            {'direction': 'west', 'steps': 1},
            {'direction': 'south', 'steps': 1},
            {'direction': 'south', 'steps': 1},
        ],
        5,
        id='suite'
    ),
    pytest.param(
        [
            {'direction': 'north', 'steps': 1},
            {'direction': 'west', 'steps': 1},
            {'direction': 'south', 'steps': 1},
            {'direction': 'east', 'steps': 1},
            {'direction': 'north', 'steps': 1},
        ],
        4,
        id='suite_overlap'
    ),
    pytest.param(
        [],
        1,
        id='empty'
    ),
    pytest.param(
        [
            {'direction': 'north', 'steps': 5},
        ],
        6,
        id='long_basic'
    ),
    pytest.param(
        [
            {'direction': 'north', 'steps': 5},
            {'direction': 'south', 'steps': 5}
        ],
        6,
        id='long_overlap'
    ),
    pytest.param(
        [
            {'direction': 'north', 'steps': 3},
            {'direction': 'south', 'steps': 6}
        ],
        7,
        id='partial_overlap'
    ),
]


class TestRobotTracker:
    @pytest.mark.parametrize(
        'commands, expected',
        COMMANDS
    )
    def test_num_of_vertices_visited_is_calculated_correctly(
            self,
            commands,
            expected
    ):
        """The number of vertices visited by the robot is calculated correctly
        with fixed (arbitrary) starting point (without loss of generality).
        """
        result = RobotTracker.get_num_of_cleaned_vertices(
            {'x': 0, 'y': 0},
            commands
        )
        assert result == expected
