from django.contrib import admin
from .models import Appointment, Service, User

admin.site.register(Appointment)
admin.site.register(Service)
admin.site.register(User)
