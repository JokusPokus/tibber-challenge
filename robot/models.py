from django.db import models


class Execution(models.Model):
    """Represents the execution of a robot cleaning job."""

    timestamp = models.DateTimeField(auto_now_add=True)
    commands = models.PositiveIntegerField()
    result = models.PositiveIntegerField()
    duration = models.FloatField()

    class Meta:
        db_table = 'executions'
