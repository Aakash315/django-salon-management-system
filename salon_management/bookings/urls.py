from django.urls import path
from . import views

urlpatterns = [
    path("", views.booking_page, name="booking"),
    path("staff-by-service/", views.staff_by_service, name="staff_by_service"),
    path("available-slots/", views.available_slots, name="available_slots"),
    path("create/", views.create_booking, name="create_booking"),
    path("success/<int:booking_id>/", views.booking_success, name="booking_success"),
]