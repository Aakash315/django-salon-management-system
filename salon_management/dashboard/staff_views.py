from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render
)
from django.utils import timezone

from accounts.models import StaffProfile
from bookings.models import Appointment
from salon.models import StaffService, StaffAvailability
from datetime import datetime
from django.contrib import messages



def get_staff(request):

    if request.user.role != "staff":
        return None

    return get_object_or_404(
        StaffProfile,
        user=request.user
    )


@login_required
def staff_dashboard(request):

    staff = get_staff(request)

    if staff is None:
        return redirect("login")

    today = timezone.localdate()

    appointments = Appointment.objects.filter(
        staff=staff,
        appointment_date=today
    ).order_by(
        "start_time"
    )

    today_count = appointments.count()

    pending_count = appointments.filter(
        status="pending"
    ).count()

    completed_count = appointments.filter(
        status="completed"
    ).count()

    today_revenue = appointments.filter(
        status="completed"
    ).aggregate(
        total=Sum("price")
    )["total"] or 0

    context = {
        "staff": staff,
        "appointments": appointments,
        "today_count": today_count,
        "pending_count": pending_count,
        "completed_count": completed_count,
        "today_revenue": today_revenue,
    }

    return render(
        request,
        "staff/dashboard.html",
        context
    )


@login_required
def staff_services(request):

    staff = get_staff(request)

    if staff is None:
        return redirect("login")

    services = StaffService.objects.filter(
        staff=staff
    ).select_related(
        "service"
    )

    return render(
        request,
        "staff/services.html",
        {
            "staff": staff,
            "services": services
        }
    )


@login_required
def edit_staff_service(
    request,
    service_id
):

    staff = get_staff(request)

    if staff is None:
        return redirect("login")

    staff_service = get_object_or_404(
        StaffService,
        id=service_id,
        staff=staff
    )

    if request.method == "POST":

        price = request.POST.get("price")
        duration = request.POST.get("duration")

        staff_service.price = price
        staff_service.duration = duration

        staff_service.is_available = (
            request.POST.get("is_available")
            == "on"
        )

        staff_service.save()

        return redirect(
            "staff_services"
        )

    return render(
        request,
        "staff/service_edit.html",
        {
            "staff": staff,
            "staff_service": staff_service
        }
    )


@login_required
def staff_availability(request):

    staff = get_staff(request)

    if staff is None:
        return redirect("login")

    availability = StaffAvailability.objects.filter(
        staff=staff
    ).order_by("day")

    return render(
        request,
        "staff/availability.html",
        {
            "staff": staff,
            "availability": availability,
        }
    )

@login_required
def save_availability(request):

    staff = get_staff(request)

    if staff is None:
        return redirect("login")

    if request.method != "POST":
        return redirect("staff_availability")

    days = [
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    ]

    for day_number, day_name in enumerate(days):

        is_available = request.POST.get(
            f"{day_name}_available"
        ) == "on"

        start_time = request.POST.get(
            f"{day_name}_start"
        )

        end_time = request.POST.get(
            f"{day_name}_end"
        )

        availability, created = (
            StaffAvailability.objects.get_or_create(
                staff=staff,
                day=day_number
            )
        )

        availability.is_available = is_available

        if start_time:
            availability.start_time = start_time

        if end_time:
            availability.end_time = end_time

        availability.save()

    messages.success(
        request,
        "Availability updated successfully."
    )

    return redirect(
        "staff_availability"
    )


@login_required
def staff_appointments(request):

    staff = get_staff(request)

    if staff is None:
        return redirect("login")

    appointments = Appointment.objects.filter(
        staff=staff
    ).order_by(
        "-appointment_date",
        "-start_time"
    )

    return render(
        request,
        "staff/appointments.html",
        {
            "staff": staff,
            "appointments": appointments
        }
    )


@login_required
def staff_profile(request):

    if request.user.role != "staff":
        return redirect("login")

    staff = StaffProfile.objects.get(
        user=request.user)

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        phone = request.POST.get(
            "phone",
            ""
        ).strip()

        designation = request.POST.get(
            "designation",
            ""
        ).strip()

        staff.name = name
        staff.email = email
        staff.phone = phone
        staff.designation = designation

        staff.save()

        request.user.email = email
        request.user.save(
            update_fields=["email"]
        )

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect("staff_profile")

    return render(
        request,
        "staff/profile.html",
        {
            "staff": staff
        }
    )

@login_required
def update_staff_appointment_status(
    request,
    appointment_id
):

    staff = get_staff(request)

    if staff is None:
        return redirect("login")

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        staff=staff
    )

    if request.method == "POST":

        status = request.POST.get(
            "status"
        )

        valid_statuses = {
            "pending",
            "confirmed",
            "completed",
            "cancelled"
        }

        if status in valid_statuses:

            appointment.status = status
            appointment.save()

            messages.success(
                request,
                "Appointment updated."
            )

    return redirect(
        "staff_appointments"
    )