from rest_framework import serializers

from .models import Execution


class ExecutionSerializer(serializers.ModelSerializer):
    """Creates execution instances and serializes their data to JSON."""

    class Meta:
        model = Execution
        fields = ['timestamp', 'commands', 'result', 'duration']
        read_only_fields = ['timestamp']

    def to_representation(self, instance):
        """
        Override to_representation to display duration as a formatted string.
        """
        representation = super().to_representation(instance)
        representation['duration'] = format(representation['duration'], '.6f')
        return representation
