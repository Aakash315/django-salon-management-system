from django.urls import path
from . import customer_views

urlpatterns = [

    path(
        "dashboard/",
        customer_views.customer_dashboard,
        name="customer_dashboard"
    ),

    path(
        "services/",
        customer_views.customer_services,
        name="customer_services"
    ),

    path(
        "bookings/",
        customer_views.customer_bookings,
        name="customer_bookings"
    ),

    path(
        "profile/",
        customer_views.customer_profile,
        name="customer_profile"
    ),

    path(
        "bookings/<int:booking_id>/cancel/",
        customer_views.cancel_booking,
        name="cancel_booking"
    ),
]