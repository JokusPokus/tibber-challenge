"""
End-to-end tests for the cleaning robot API.
"""
import pytest
import json

from django.urls import reverse


@pytest.mark.django_db
class TestRobotAPI:
    def test_create_execution(self, client):
        """The expected JSON response with execution data is returned when
        a valid request is made.
        """
        payload = {
            'start': {'x': 0, 'y': 0},
            'commands': [{'direction': 'north', 'steps': 1}]
        }
        response = client.post(
            reverse('robot:clean'),
            data=json.dumps(payload),
            content_type='application/json'
        )
        assert response.status_code == 201

        for attr in ['timestamp', 'commands', 'result', 'duration']:
            assert attr in response.json()
