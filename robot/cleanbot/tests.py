"""
Unit tests for the cleanbot package.
"""
import pytest
import random
import timeit

from .trackers import RobotTracker, SimpleRobotTracker


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
    pytest.param(
        [
            {'direction': 'east', 'steps': 10000},
            {'direction': 'west', 'steps': 10000}
        ] * 5000,
        10001,
        id='huge_east_west'
    ),
    pytest.param(
        [
            {'direction': 'north', 'steps': 10000},
            {'direction': 'south', 'steps': 10000}
        ] * 5000,
        10001,
        id='huge_north_south'
    ),
    pytest.param(
        [
            {'direction': 'north', 'steps': 3},
            {'direction': 'east', 'steps': 3},
            {'direction': 'south', 'steps': 2},
            {'direction': 'west', 'steps': 4},
            {'direction': 'east', 'steps': 2},
            {'direction': 'north', 'steps': 2},
            {'direction': 'east', 'steps': 3},
        ],
        14,
        id='complex'
    ),
    pytest.param(
        [
            {'direction': 'north', 'steps': 1},
            {'direction': 'east', 'steps': 1},
            {'direction': 'south', 'steps': 1},
            {'direction': 'west', 'steps': 1},
        ] * 10,
        4,
        id='circular'
    ),
    pytest.param(
        [
            {'direction': 'north', 'steps': 3},
            {'direction': 'east', 'steps': 1},
            {'direction': 'south', 'steps': 3},
        ],
        8,
        id='tight_snake'
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
        result = RobotTracker().get_num_of_cleaned_vertices(commands)
        assert result == expected

    @pytest.mark.skip
    def test_performance_for_large_problem(self):
        """The performance of the robot tracker is measured for a
        large problem. Just to play around and get a feeling.
        """
        DIRS = ['north', 'east', 'south', 'west']
        commands = [
            {
                'direction': random.choice(DIRS),
                'steps': random.randint(1, 10000)
            }
            for _ in range(5000)
        ]

        start_time = timeit.default_timer()
        result = RobotTracker().get_num_of_cleaned_vertices(commands)
        elapsed_time = timeit.default_timer() - start_time
        print(f'Unique vertices: {result}\nElapsed time: {elapsed_time}')
