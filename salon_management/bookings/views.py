from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .models import Appointment
from accounts.models import StaffProfile
from salon.models import StaffService, Service, StaffAvailability

# Create your views here.
@login_required
def booking_page(request):
    if request.user.role != "customer":
        return redirect("login")

    services = Service.objects.filter(is_active=True)
    staff_members = StaffProfile.objects.filter(is_available=True)

    return render(request, "customer/booking.html", {
        "services": services,
        "staff_members": staff_members,
    })

@login_required
def staff_by_service(request):

    if request.user.role != "customer":

        return JsonResponse(
            {
                "error": "Unauthorized"
            },
            status=403
        )

    service_id = request.GET.get(
        "service"
    )

    if not service_id:

        return JsonResponse({
            "staff": []
        })

    staff_services = (
        StaffService.objects
        .filter(
            service_id=service_id,
            is_available=True,
            staff__is_available=True
        )
        .select_related(
            "staff",
            "service"
        )
        .order_by(
            "staff__name"
        )
    )

    staff = []

    for item in staff_services:

        staff.append({

            "id": item.staff.id,

            "name": item.staff.name,

            "price": str(item.price),

            "duration": item.duration,

            "designation":
                item.staff.designation,

        })

    return JsonResponse({
        "staff": staff
    })

@login_required
def available_slots(request):

    if request.user.role != "customer":

        return JsonResponse(
            {
                "error": "Unauthorized"
            },
            status=403
        )

    staff_id = request.GET.get("staff")
    service_id = request.GET.get("service")
    date_string = request.GET.get("date")

    # --------------------------------
    # Validate parameters
    # --------------------------------

    if not staff_id:
        return JsonResponse({
            "slots": [],
            "error": "Staff is required."
        })

    if not service_id:
        return JsonResponse({
            "slots": [],
            "error": "Service is required."
        })

    if not date_string:
        return JsonResponse({
            "slots": [],
            "error": "Date is required."
        })

    # --------------------------------
    # Parse date
    # --------------------------------

    try:

        selected_date = datetime.strptime(
            date_string,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        return JsonResponse({
            "slots": [],
            "error": "Invalid date."
        })

    # --------------------------------
    # Don't allow past dates
    # --------------------------------

    today = timezone.localdate()

    if selected_date < today:

        return JsonResponse({
            "slots": [],
            "error": "Cannot book a past date."
        })

    # --------------------------------
    # Get staff
    # --------------------------------

    staff = get_object_or_404(
        StaffProfile,
        id=staff_id,
        is_available=True
    )

    # --------------------------------
    # Get staff service
    # --------------------------------

    staff_service = get_object_or_404(
        StaffService,
        staff=staff,
        service_id=service_id,
        is_available=True
    )

    # --------------------------------
    # Get weekday
    # --------------------------------

    weekday = selected_date.weekday()

    # Monday = 0
    # Tuesday = 1
    # ...
    # Sunday = 6

    availability = (
        StaffAvailability.objects
        .filter(
            staff=staff,
            day=weekday,
            is_available=True
        )
        .first()
    )

    # --------------------------------
    # Staff is OFF
    # --------------------------------

    if not availability:

        return JsonResponse({
            "slots": [],
            "message": "Staff is not available on this day."
        })

    if not availability.start_time:
        return JsonResponse({
            "slots": [],
            "message": "Staff working hours are not configured."
        })

    if not availability.end_time:
        return JsonResponse({
            "slots": [],
            "message": "Staff working hours are not configured."
        })

    # --------------------------------
    # Generate slots
    # --------------------------------

    duration = staff_service.duration

    # slot_interval = duration

    current_datetime = datetime.combine(
        selected_date,
        availability.start_time
    )

    working_end_datetime = datetime.combine(
        selected_date,
        availability.end_time
    )

    slots = []

    while (current_datetime + timedelta(minutes=duration)) <= working_end_datetime:

        slot_start_datetime = current_datetime
        slot_end_datetime = (current_datetime + timedelta(minutes=duration))
        slot_start_time = slot_start_datetime.time()
        slot_end_time = slot_end_datetime.time()

        # Don't create a slot that goes
        # beyond staff working hours

        # if slot_end > availability.end_time:
        #     break

        # --------------------------------
        # Check if slot is in the past
        # --------------------------------

        if selected_date == today:

            now = timezone.localtime()

            slot_datetime = timezone.make_aware(
                slot_start_datetime
            )

            if slot_datetime <= now:

                current_datetime += timedelta(minutes=duration)
                continue

            # slot_datetime = timezone.make_aware(
            #     datetime.combine(
            #         selected_date,
            #         current_time
            #     )
            # )

            # if slot_datetime <= current_datetime:

            #     current_time = (
            #         datetime.combine(
            #             selected_date,
            #             current_time
            #         )
            #         + timedelta(minutes=slot_interval)
            #     ).time()

            #     continue

        # --------------------------------
        # Check existing appointment
        # --------------------------------

        overlapping = ( Appointment.objects.filter(
            staff=staff,
            appointment_date=selected_date,
            status__in=[
                "pending",
                "confirmed"
            ],
            start_time__lt=slot_end_time,
            end_time__gt=slot_start_time
        ).exists() )

        if not overlapping:

            slots.append({
                "time": slot_start_time.strftime(
                    "%H:%M"
                ),

                "display_time": slot_start_time.strftime(
                    "%I:%M %p"
                ),

                "end_time": slot_end_time.strftime(
                    "%H:%M"
                ),

                "display_end_time": slot_end_time.strftime(
                    "%I:%M %p"
                ),

                "price": str(
                    staff_service.price
                ),

                "duration": duration,
            })

        # --------------------------------
        # Next slot
        # --------------------------------

        current_datetime += timedelta(minutes=duration)
        # current_time = current_datetime.time()

    return JsonResponse({
        "slots": slots,
        "service": staff_service.service.name,
        "staff": staff.name,
        "date": date_string
    })

@login_required
def create_booking(request):

    if request.user.role != "customer":
        return redirect("login")

    if request.method != "POST":
        return redirect("booking")

    service_id = request.POST.get("service")
    staff_id = request.POST.get("staff")
    date_string = request.POST.get("date")
    start_time_string = request.POST.get("start_time")
    notes = request.POST.get("notes", "")

    # --------------------------------
    # Validate input
    # --------------------------------

    if not service_id or not staff_id:
        messages.error(
            request,
            "Please select service and staff."
        )
        return redirect("booking")

    if not date_string or not start_time_string:
        messages.error(
            request,
            "Please select date and time."
        )
        return redirect("booking")    

    # --------------------------------
    # Get service
    # --------------------------------

    service = get_object_or_404(
        Service,
        id=service_id,
        is_active=True
    )

    # --------------------------------
    # Get staff
    # --------------------------------

    staff = get_object_or_404(
        StaffProfile,
        id=staff_id,
        is_available=True
    )

    # --------------------------------
    # Get staff service
    # --------------------------------

    staff_service = get_object_or_404(
        StaffService,
        staff=staff,
        service=service,
        is_available=True
    )

    # --------------------------------
    # Parse date
    # --------------------------------

    try:

        appointment_date = datetime.strptime(
            date_string,
            "%Y-%m-%d"
        ).date()

    except ValueError:

        messages.error(
            request,
            "Invalid date or time format."
        )

        return redirect("booking")

    # --------------------------------
    # Don't allow past date
    # --------------------------------

    today = timezone.localdate()

    if appointment_date < today:

        messages.error(
            request,
            "You cannot book a past date."
        )

        return redirect("booking")

    # --------------------------------
    # Parse start time
    # --------------------------------

    try:

        start_time = datetime.strptime(
            start_time_string,
            "%H:%M"
        ).time()

    except ValueError:

        messages.error(
            request,
            "Invalid appointment time."
        )

        return redirect("booking")


    # --------------------------------
    # Calculate END TIME
    # using service duration
    # --------------------------------

    start_datetime = datetime.combine(
        appointment_date,
        start_time
    )

    end_datetime = (
        start_datetime +
        timedelta(
            minutes=staff_service.duration
        )
    )

    end_time = end_datetime.time()

    # --------------------------------
    # Check staff availability
    # --------------------------------

    weekday = appointment_date.weekday()

    availability = StaffAvailability.objects.filter(
        staff=staff,
        day=weekday,
        is_available=True
    ).first()

    if not availability:

        messages.error(
            request,
            "Staff is not available on this date."
        )

        return redirect("booking")

    # --------------------------------
    # Check working hours
    # --------------------------------

    if not availability.start_time:
        messages.error(
            request,
            "Staff working hours are not configured."
        )
        return redirect("booking")

    if not availability.end_time:
        messages.error(
            request,
            "Staff working hours are not configured."
        )
        return redirect("booking")

    if (
        start_time < availability.start_time
        or
        end_time > availability.end_time
    ):

        messages.error(
            request,
            "Selected time is outside staff working hours."
        )

        return redirect("booking")

    # --------------------------------
    # Check today's past time
    # --------------------------------

    if appointment_date == today:

        current_datetime = timezone.localtime()

        booking_datetime = timezone.make_aware(
            start_datetime
        )

        if booking_datetime <= current_datetime:

            messages.error(
                request,
                "You cannot book a past time."
            )

            return redirect("booking")

    # --------------------------------
    # Check overlapping appointments
    # --------------------------------

    conflict = Appointment.objects.filter(
        staff=staff,
        appointment_date=appointment_date,
        status__in=[
            "pending",
            "confirmed"
        ],
        start_time__lt=end_time,
        end_time__gt=start_time
    ).exists()

    if conflict:

        messages.error(
            request,
            "This slot has already been booked."
        )

        return redirect("booking")

    # --------------------------------
    # Create appointment
    # --------------------------------

    appointment = Appointment.objects.create(
        customer=request.user,
        staff=staff,
        service=service,
        appointment_date=appointment_date,
        start_time=start_time,
        end_time=end_time,
        price=staff_service.price,
        notes=notes,
        status="pending"
    )

    messages.success(
        request,
        "Appointment booked successfully!"
    )

    return redirect(
        "booking_success",
        booking_id=appointment.id
    )

@login_required
def booking_success(
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

    return render(
        request,
        "customer/booking_success.html",
        {
            "appointment": appointment
        }
    )