import timeit

from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .cleanbot import RobotTracker
from .serializers import ExecutionSerializer


class PostCleaningJob(APIView):
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
        commands = request.data.get('commands')

        start_time = timeit.default_timer()
        result = RobotTracker().get_num_of_cleaned_vertices(commands)
        end_time = timeit.default_timer()

        serializer = ExecutionSerializer(data={
            'commands': len(commands),
            'result': result,
            'duration': end_time - start_time
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)

        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)
