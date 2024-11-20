from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from booking.views import (
    UserViewSet,
    ServiceViewSet,
    AppointmentViewSet,
    ScheduleViewSet,
    ReservationViewSet,
    ServiceListView,
    AvailableTimesView,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"services", ServiceViewSet)
router.register(r"appointments", AppointmentViewSet)
router.register(r"schedules", ScheduleViewSet)
router.register(r"reservations", ReservationViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
    path("api/services/", ServiceListView.as_view(), name="services"),
    path("api/available-times/", AvailableTimesView.as_view(), name="available-times"),
    path("api/", include(router.urls)),
]
