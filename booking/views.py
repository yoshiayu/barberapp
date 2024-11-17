from rest_framework import viewsets
from .models import User, Service, Appointment, Schedule
from .serializers import UserSerializer, ServiceSerializer, AppointmentSerializer, ScheduleSerializer  # type: ignore


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    filterset_fields = ["user", "service", "date", "time", "status"]
    ordering_fields = ["date", "time"]
    search_fields = ["user__name", "service__name"]
    paginate_by = 10


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer
