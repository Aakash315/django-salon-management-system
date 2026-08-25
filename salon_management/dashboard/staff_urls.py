from django.urls import path
from . import staff_views

urlpatterns = [

    path(
        "dashboard/",
        staff_views.staff_dashboard,
        name="staff_dashboard"
    ),

    path(
        "services/",
        staff_views.staff_services,
        name="staff_services"
    ),

    path(
        "services/<int:service_id>/edit/",
        staff_views.edit_staff_service,
        name="edit_staff_service"
    ),

    path(
        "availability/",
        staff_views.staff_availability,
        name="staff_availability"
    ),

    path(
        "availability/save/",
        staff_views.save_availability,
        name="save_availability"
    ),

    path(
        "appointments/",
        staff_views.staff_appointments,
        name="staff_appointments"
    ),

    path(
        "profile/",
        staff_views.staff_profile,
        name="staff_profile"
    ),

    path(
        "appointments/<int:appointment_id>/status/",
        staff_views.update_staff_appointment_status,
        name="update_staff_appointment_status"
    ),
]