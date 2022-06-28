from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions


class ListUsers(APIView):
    """
    View to create an execution instance based on a robot cleaning job.
    """

    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def post(self, request, format=None):
        """
        Accept a cleaning job, and create and return an execution record.

        Expected request body items:
          - start: a dictionary holding x and y coordinates of the
            robot's starting position
          - commands: a list of commands to be executed, with each command
            specifying the direction to move in and the number of steps.
        """
        start = request.data.get('start')
        commands = request.data.get('commands')

        return Response()
