from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from booking.views import (
    UserViewSet,
    ServiceViewSet,
    AppointmentViewSet,
    ScheduleViewSet,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"services", ServiceViewSet)
router.register(r"appointments", AppointmentViewSet)
router.register(r"schedules", ScheduleViewSet)


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include(router.urls)),
]
