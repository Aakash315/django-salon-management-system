from datetime import datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from accounts.models import User, StaffProfile, CustomerProfile
from bookings.models import Appointment
from salon.models import Service, StaffService, StaffAvailability

def admin_required(request):

    if not request.user.is_authenticated:
        return False

    return (
        request.user.role == "admin"
        or request.user.is_superuser
    )

@login_required
def admin_dashboard(request):

    if not (request.user.role == "admin" or request.user.is_superuser):
        return redirect("login")

    today = timezone.localdate()

    total_staff = StaffProfile.objects.count()

    total_customers = User.objects.filter(
        role="customer"
    ).count()

    today_appointments = Appointment.objects.filter(
        appointment_date=today
    ).count()

    today_revenue = Appointment.objects.filter(
        appointment_date=today,
        status="completed"
    ).aggregate(
        total=Sum("price")
    )["total"] or 0

    appointments = Appointment.objects.filter(
        appointment_date=today
    ).select_related(
        "customer",
        "staff",
        "service"
    ).order_by(
        "start_time"
    )

    context = {
        "total_staff": total_staff,
        "total_customers": total_customers,
        "today_appointments": today_appointments,
        "today_revenue": today_revenue,
        "appointments": appointments,
    }

    return render(
        request,
        "admin_dashboard/dashboard.html",
        context
    )

@login_required
def admin_staff(request):

    if not admin_required(request):
        return redirect("login")

    staff_members = StaffProfile.objects.select_related(
        "user"
    ).order_by(
        "name"
    )

    return render(
        request,
        "admin_dashboard/staff.html",
        {
            "staff_members": staff_members
        }
    )

@login_required
def add_staff(request):

    if not admin_required(request):
        return redirect("login")

    if request.method == "POST":

        name = request.POST.get("name")
        phone = request.POST.get("phone")
        email = request.POST.get("email")
        designation = request.POST.get(
            "designation"
        )
        password = request.POST.get(
            "password"
        )

        if User.objects.filter(
            phone=phone
        ).exists():

            messages.error(
                request,
                "A user with this phone number already exists."
            )

            return redirect(
                "admin_add_staff"
            )

        username = phone

        if User.objects.filter(
            username=username
        ).exists():

            messages.error(
                request,
                "Username already exists."
            )

            return redirect(
                "admin_add_staff"
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            phone=phone,
            email=email,
            role="staff"
        )

        staff = StaffProfile.objects.create(
            user=user,
            name=name,
            phone=phone,
            email=email,
            designation=designation
        )

        for day in range(7):
            StaffAvailability.objects.create(
                staff=staff,
                day=day,
                is_available=False
            )

        messages.success(
            request,
            "Staff member created successfully."
        )

        return redirect(
            "admin_staff"
        )

    return render(
        request,
        "admin_dashboard/staff_form.html"
    )


@login_required
def edit_staff(
    request,
    staff_id
):

    if not admin_required(request):
        return redirect("login")

    staff = get_object_or_404(
        StaffProfile,
        id=staff_id
    )

    if request.method == "POST":

        staff.name = request.POST.get(
            "name"
        )

        staff.phone = request.POST.get(
            "phone"
        )

        staff.email = request.POST.get(
            "email"
        )

        staff.designation = request.POST.get(
            "designation"
        )

        staff.is_available = (
            request.POST.get(
                "is_available"
            ) == "on"
        )

        staff.save()

        staff.user.phone = staff.phone
        staff.user.email = staff.email
        staff.user.save()

        messages.success(
            request,
            "Staff updated successfully."
        )

        return redirect(
            "admin_staff"
        )

    return render(
        request,
        "admin_dashboard/staff_edit.html",
        {
            "staff": staff
        }
    )

@login_required
def delete_staff(
    request,
    staff_id
):

    if not admin_required(request):
        return redirect("login")

    staff = get_object_or_404(
        StaffProfile,
        id=staff_id
    )

    staff.is_available = False
    staff.user.is_active = False

    staff.save()
    staff.user.save()

    messages.success(
        request,
        "Staff member deactivated."
    )

    return redirect(
        "admin_staff"
    )

@login_required
def admin_services(request):

    if not admin_required(request):
        return redirect("login")

    services = Service.objects.annotate(
        staff_count=Count(
            "staff_services"
        )
    ).order_by(
        "name"
    )

    return render(
        request,
        "admin_dashboard/services.html",
        {
            "services": services
        }
    )

@login_required
def add_service(request):

    if not admin_required(request):
        return redirect("login")

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get(
            "description"
        )
        price = request.POST.get(
            "default_price"
        )
        duration = request.POST.get(
            "default_duration"
        )

        Service.objects.create(
            name=name,
            description=description,
            default_price=price,
            default_duration=duration
        )

        messages.success(
            request,
            "Service created successfully."
        )

        return redirect(
            "admin_services"
        )

    return render(
        request,
        "admin_dashboard/service_form.html"
    )

@login_required
def edit_service(
    request,
    service_id
):

    if not admin_required(request):
        return redirect("login")

    service = get_object_or_404(
        Service,
        id=service_id
    )

    if request.method == "POST":

        service.name = request.POST.get(
            "name"
        )

        service.description = request.POST.get(
            "description"
        )

        service.default_price = request.POST.get(
            "default_price"
        )

        service.default_duration = request.POST.get(
            "default_duration"
        )

        service.is_active = (
            request.POST.get(
                "is_active"
            ) == "on"
        )

        service.save()

        messages.success(
            request,
            "Service updated successfully."
        )

        return redirect(
            "admin_services"
        )

    return render(
        request,
        "admin_dashboard/service_edit.html",
        {
            "service": service
        }
    )

@login_required
def delete_service(
    request,
    service_id
):

    if not admin_required(request):
        return redirect("login")

    service = get_object_or_404(
        Service,
        id=service_id
    )

    service.is_active = False
    service.save()

    messages.success(
        request,
        "Service disabled."
    )

    return redirect(
        "admin_services"
    )

@login_required
def admin_customers(request):

    if not admin_required(request):
        return redirect("login")

    customers = User.objects.filter(
        role="customer"
    ).order_by(
        "-date_joined"
    )

    return render(
        request,
        "admin_dashboard/customers.html",
        {
            "customers": customers
        }
    )

@login_required
def customer_detail(
    request,
    customer_id
):

    if not admin_required(request):
        return redirect("login")

    customer = get_object_or_404(
        User,
        id=customer_id,
        role="customer"
    )

    appointments = Appointment.objects.filter(
        customer=customer
    ).select_related(
        "staff",
        "service"
    ).order_by(
        "-appointment_date",
        "-start_time"
    )

    return render(
        request,
        "admin_dashboard/customer_detail.html",
        {
            "customer": customer,
            "appointments": appointments
        }
    )

@login_required
def admin_appointments(request):

    if not admin_required(request):
        return redirect("login")

    appointments = Appointment.objects.select_related(
        "customer",
        "staff",
        "service"
    ).order_by(
        "-appointment_date",
        "-start_time"
    )

    return render(
        request,
        "admin_dashboard/appointments.html",
        {
            "appointments": appointments
        }
    )

@login_required
def update_appointment_status(
    request,
    appointment_id
):

    if not admin_required(request):
        return redirect("login")

    appointment = get_object_or_404(
        Appointment,
        id=appointment_id
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
                "Appointment status updated."
            )

    return redirect(
        "admin_appointments"
    )

@login_required
def admin_reports(request):

    if not admin_required(request):
        return redirect("login")

    today = timezone.localdate()

    report_type = request.GET.get(
        "report",
        "daily"
    )

    # --------------------------------
    # Calculate date range
    # --------------------------------

    if report_type == "daily":

        start_date = today
        end_date = today

    elif report_type == "weekly":

        # Monday -> Sunday
        start_date = (
            today
            - timedelta(
                days=today.weekday()
            )
        )

        end_date = (
            start_date
            + timedelta(days=6)
        )

    elif report_type == "monthly":

        start_date = today.replace(
            day=1
        )

        # First day of next month
        if today.month == 12:

            next_month = today.replace(
                year=today.year + 1,
                month=1,
                day=1
            )

        else:

            next_month = today.replace(
                month=today.month + 1,
                day=1
            )

        end_date = (
            next_month
            - timedelta(days=1)
        )

    else:

        report_type = "daily"

        start_date = today
        end_date = today

    # --------------------------------
    # Filter appointments
    # --------------------------------

    appointments = Appointment.objects.filter(
        appointment_date__gte=start_date,
        appointment_date__lte=end_date
    )

    # --------------------------------
    # Revenue
    # --------------------------------

    total_revenue = (
        appointments
        .filter(
            status="completed"
        )
        .aggregate(
            total=Sum("price")
        )["total"] or 0
    )

    # --------------------------------
    # Booking counts
    # --------------------------------

    total_bookings = (
        appointments.count()
    )

    completed_bookings = (
        appointments
        .filter(
            status="completed"
        )
        .count()
    )

    pending_bookings = (
        appointments
        .filter(
            status="pending"
        )
        .count()
    )

    confirmed_bookings = (
        appointments
        .filter(
            status="confirmed"
        )
        .count()
    )

    cancelled_bookings = (
        appointments
        .filter(
            status="cancelled"
        )
        .count()
    )

    # --------------------------------
    # Popular services
    # --------------------------------

    popular_services = (
        Service.objects
        .filter(
            appointments__in=appointments
        )
        .annotate(
            booking_count=Count(
                "appointments",
                filter=Q(
                    appointments__in=appointments
                )
            )
        )
        .order_by(
            "-booking_count"
        )[:10]
    )

    # --------------------------------
    # Service revenue
    # --------------------------------

    service_revenue = (
        Service.objects
        .filter(
            appointments__in=appointments,
            appointments__status="completed"
        )
        .annotate(
            revenue=Sum(
                "appointments__price",
                filter=Q(
                    appointments__in=appointments,
                    appointments__status="completed"
                )
            ),
            booking_count=Count(
                "appointments",
                filter=Q(
                    appointments__in=appointments
                )
            )
        )
        .order_by(
            "-revenue"
        )
    )

    context = {

        "report_type": report_type,

        "start_date": start_date,
        "end_date": end_date,

        "total_revenue": total_revenue,

        "total_bookings": total_bookings,

        "completed_bookings":
            completed_bookings,

        "pending_bookings":
            pending_bookings,

        "confirmed_bookings":
            confirmed_bookings,

        "cancelled_bookings":
            cancelled_bookings,

        "popular_services":
            popular_services,

        "service_revenue":
            service_revenue,
    }

    return render(
        request,
        "admin_dashboard/reports.html",
        context
    )

@login_required
def admin_staff_reports(request):

    if not admin_required(request):
        return redirect("login")

    # --------------------------------
    # Get staff
    # --------------------------------

    staff_members = (
        StaffProfile.objects
        .filter(
            is_available=True
        )
        .order_by("name")
    )

    # --------------------------------
    # Selected staff
    # --------------------------------

    staff_id = request.GET.get("staff")

    selected_staff = None

    if staff_id:

        selected_staff = get_object_or_404(
            StaffProfile,
            id=staff_id
        )

    # --------------------------------
    # Report type
    # --------------------------------

    report_type = request.GET.get(
        "report",
        "daily"
    )

    today = timezone.localdate()

    # --------------------------------
    # Date range
    # --------------------------------

    if report_type == "daily":

        start_date = today
        end_date = today

    elif report_type == "weekly":

        start_date = (
            today
            - timedelta(
                days=today.weekday()
            )
        )

        end_date = (
            start_date
            + timedelta(days=6)
        )

    elif report_type == "monthly":

        start_date = today.replace(
            day=1
        )

        if today.month == 12:

            next_month = today.replace(
                year=today.year + 1,
                month=1,
                day=1
            )

        else:

            next_month = today.replace(
                month=today.month + 1,
                day=1
            )

        end_date = (
            next_month
            - timedelta(days=1)
        )

    else:

        report_type = "daily"

        start_date = today
        end_date = today

    # --------------------------------
    # Default values
    # --------------------------------

    total_revenue = 0
    total_bookings = 0
    completed_bookings = 0
    pending_bookings = 0
    confirmed_bookings = 0
    cancelled_bookings = 0

    appointments = Appointment.objects.none()

    service_report = []

    # --------------------------------
    # Generate report
    # --------------------------------

    if selected_staff:

        appointments = Appointment.objects.filter(
            staff=selected_staff,
            appointment_date__gte=start_date,
            appointment_date__lte=end_date
        )

        # Revenue

        total_revenue = (
            appointments
            .filter(
                status="completed"
            )
            .aggregate(
                total=Sum("price")
            )["total"] or 0
        )

        # Bookings

        total_bookings = (
            appointments.count()
        )

        # Completed

        completed_bookings = (
            appointments
            .filter(
                status="completed"
            )
            .count()
        )

        # Pending

        pending_bookings = (
            appointments
            .filter(
                status="pending"
            )
            .count()
        )

        # Confirmed

        confirmed_bookings = (
            appointments
            .filter(
                status="confirmed"
            )
            .count()
        )

        # Cancelled

        cancelled_bookings = (
            appointments
            .filter(
                status="cancelled"
            )
            .count()
        )

        # --------------------------------
        # Services performed
        # --------------------------------

        service_report = (
            Service.objects
            .filter(
                appointments__in=appointments
            )
            .annotate(
                booking_count=Count(
                    "appointments",
                    filter=Q(
                        appointments__in=appointments
                    )
                ),
                revenue=Sum(
                    "appointments__price",
                    filter=Q(
                        appointments__in=appointments,
                        appointments__status="completed"
                    )
                )
            )
            .order_by(
                "-booking_count"
            )
        )

    context = {

        "staff_members":
            staff_members,

        "selected_staff":
            selected_staff,

        "report_type":
            report_type,

        "start_date":
            start_date,

        "end_date":
            end_date,

        "total_revenue":
            total_revenue,

        "total_bookings":
            total_bookings,

        "completed_bookings":
            completed_bookings,

        "pending_bookings":
            pending_bookings,

        "confirmed_bookings":
            confirmed_bookings,

        "cancelled_bookings":
            cancelled_bookings,

        "service_report":
            service_report,

        "appointments":
            appointments,
    }

    return render(
        request,
        "admin_dashboard/staff_reports.html",
        context
    )

@login_required
def staff_services(request, staff_id):

    if not admin_required(request):
        return redirect("login")

    staff = get_object_or_404(
        StaffProfile,
        id=staff_id
    )

    services = Service.objects.filter(
        is_active=True
    ).order_by("name")

    assigned_services = StaffService.objects.filter(
        staff=staff
    ).select_related(
        "service"
    )

    assigned_ids = set(
        assigned_services.values_list(
            "service_id",
            flat=True
        )
    )

    if request.method == "POST":

        service_ids = request.POST.getlist(
            "services"
        )

        # Remove old assignments
        StaffService.objects.filter(
            staff=staff
        ).exclude(
            service_id__in=service_ids
        ).delete()

        # Create new assignments
        for service_id in service_ids:

            service = get_object_or_404(
                Service,
                id=service_id,
                is_active=True
            )

            StaffService.objects.get_or_create(
                staff=staff,
                service=service,
                defaults={
                    "price": service.default_price,
                    "duration": service.default_duration,
                    "is_available": True,
                }
            )

        messages.success(
            request,
            "Staff services updated successfully."
        )

        return redirect(
            "admin_staff_services",
            staff_id=staff.id
        )

    return render(
        request,
        "admin_dashboard/staff_services.html",
        {
            "staff": staff,
            "services": services,
            "assigned_services": assigned_services,
            "assigned_ids": assigned_ids,
        }
    )