from django.contrib import admin
from .models import Service, StaffService, StaffAvailability
# Register your models here.
admin.site.register(Service)
admin.site.register(StaffService)
admin.site.register(StaffAvailability)
