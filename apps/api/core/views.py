from rest_framework import viewsets

from .models import Event, Task
from .serializers import EventSerializer, TaskSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by("-created_at")
    serializer_class = TaskSerializer


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all().order_by("start")
    serializer_class = EventSerializer
