from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from accounts.models import User, CustomerProfile
from bookings.models import Appointment
from salon.models import Service
from django.contrib import messages


@login_required
def customer_dashboard(request):

    if request.user.role != "customer":
        return redirect("login")

    upcoming_count = Appointment.objects.filter(
        customer=request.user,
        status__in=[
            "pending",
            "confirmed"
        ]
    ).count()

    completed_count = Appointment.objects.filter(
        customer=request.user,
        status="completed"
    ).count()

    total_bookings = Appointment.objects.filter(
        customer=request.user
    ).count()

    upcoming_appointment = Appointment.objects.filter(
        customer=request.user,
        status__in=[
            "pending",
            "confirmed"
        ]
    ).order_by(
        "appointment_date",
        "start_time"
    ).first()

    context = {
        "upcoming_count": upcoming_count,
        "completed_count": completed_count,
        "total_bookings": total_bookings,
        "upcoming_appointment": upcoming_appointment,
    }

    return render(
        request,
        "customer/dashboard.html",
        context
    )


@login_required
def customer_services(request):

    if request.user.role != "customer":
        return redirect("login")

    services = Service.objects.filter(
        is_active=True
    )

    return render(
        request,
        "customer/services.html",
        {
            "services": services
        }
    )


@login_required
def customer_bookings(request):

    if request.user.role != "customer":
        return redirect("login")

    bookings = Appointment.objects.filter(
        customer=request.user
    ).order_by(
        "-appointment_date",
        "-start_time"
    )

    return render(
        request,
        "customer/bookings.html",
        {
            "bookings": bookings
        }
    )


@login_required
def customer_profile(request):

    if request.user.role != "customer":
        return redirect("login")

    profile = get_object_or_404(
        CustomerProfile,
        user=request.user
    )

    if request.method == "POST":

        name = request.POST.get(
            "name",
            ""
        ).strip()

        email = request.POST.get(
            "email",
            ""
        ).strip()

        if not name:

            messages.error(
                request,
                "Name is required."
            )

            return redirect(
                "customer_profile"
            )

        profile.name = name
        profile.email = email

        profile.save()

        request.user.email = email
        request.user.save(
            update_fields=[
                "email"
            ]
        )

        messages.success(
            request,
            "Profile updated successfully."
        )

        return redirect(
            "customer_profile"
        )

    return render(
        request,
        "customer/profile.html",
        {
            "profile": profile
        }
    )

@login_required
def cancel_booking(
    request,
    booking_id
):

    if request.user.role != "customer":
        return redirect("login")

    appointment = get_object_or_404(
        Appointment,
        id=booking_id,
        customer=request.user
    )

    if appointment.status not in [
        "pending",
        "confirmed"
    ]:

        messages.error(
            request,
            "This appointment cannot be cancelled."
        )

        return redirect(
            "customer_bookings"
        )

    appointment.status = "cancelled"
    appointment.save()

    messages.success(
        request,
        "Appointment cancelled successfully."
    )

    return redirect(
        "customer_bookings"
    )