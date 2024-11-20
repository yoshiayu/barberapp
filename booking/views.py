from django.db import IntegrityError
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
from .models import (
    Reservation,
    User,
    Service,
    Appointment,
    Schedule,
    Service,
    Appointment,
)
from .serializers import UserSerializer, ServiceSerializer, AppointmentSerializer, ScheduleSerializer, ReservationSerializer  # type: ignore


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer


class ServiceListView(APIView):
    def get(self, request):
        services = Service.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data)


class AppointmentViewSet(viewsets.ModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer

    def create(self, request, *args, **kwargs):
        print("リクエストデータ:", request.data)  # 送信データをデバッグ
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            print("エラー詳細:", e)
            raise
        except IntegrityError:
            raise ValidationError({"error": "この日時とコースは既に予約されています。"})


class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer


class AvailableTimesView(APIView):
    def get(self, request):
        date = request.query_params.get("date")
        # 実際のロジック: 予約済みの時間を除外
        times = ["10:00", "11:00", "14:00"]  # 仮のデータ
        return Response(times)
