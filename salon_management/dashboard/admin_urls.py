from django.urls import path

from . import admin_views


urlpatterns = [

    path(
        "dashboard/",
        admin_views.admin_dashboard,
        name="admin_dashboard"
    ),

    # Staff
    path(
        "staff/",
        admin_views.admin_staff,
        name="admin_staff"
    ),

    path(
        "staff/add/",
        admin_views.add_staff,
        name="admin_add_staff"
    ),

    path(
        "staff/<int:staff_id>/edit/",
        admin_views.edit_staff,
        name="admin_edit_staff"
    ),

    path(
        "staff/<int:staff_id>/delete/",
        admin_views.delete_staff,
        name="admin_delete_staff"
    ),

    path(
        "staff/<int:staff_id>/services/",
        admin_views.staff_services,
        name="admin_staff_services"
    ),

    # Customers
    path(
        "customers/",
        admin_views.admin_customers,
        name="admin_customers"
    ),

    path(
        "customers/<int:customer_id>/",
        admin_views.customer_detail,
        name="admin_customer_detail"
    ),

    # Services
    path(
        "services/",
        admin_views.admin_services,
        name="admin_services"
    ),

    path(
        "services/add/",
        admin_views.add_service,
        name="admin_add_service"
    ),

    path(
        "services/<int:service_id>/edit/",
        admin_views.edit_service,
        name="admin_edit_service"
    ),

    path(
        "services/<int:service_id>/delete/",
        admin_views.delete_service,
        name="admin_delete_service"
    ),

    # Appointments
    path(
        "appointments/",
        admin_views.admin_appointments,
        name="admin_appointments"
    ),

    path(
        "appointments/<int:appointment_id>/status/",
        admin_views.update_appointment_status,
        name="update_appointment_status"
    ),

    # Reports
    path(
        "reports/",
        admin_views.admin_reports,
        name="admin_reports"
    ),
    path(
        "staff-reports/",
        admin_views.admin_staff_reports,
        name="admin_staff_reports"
    ),
]