"""
End-to-end tests for the cleaning robot API.
"""
import pytest
import json

from django.urls import reverse

from .models import Execution


@pytest.mark.django_db
class TestRobotAPI:
    def test_execution_is_created(self, client):
        """An execution instance is created when a valid request is made."""
        num_executions = Execution.objects.count()

        payload = {
            'start': {'x': 0, 'y': 0},
            'commands': [{'direction': 'north', 'steps': 1}]
        }
        client.post(
            reverse('robot:clean'),
            data=json.dumps(payload),
            content_type='application/json'
        )

        assert Execution.objects.count() == num_executions + 1

    def test_execution_data_is_returned(self, client):
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