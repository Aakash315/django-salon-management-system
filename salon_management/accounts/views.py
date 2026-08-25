from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import User, PhoneOTP, CustomerProfile
from .utils import normalize_phone, generate_otp

# Create your views here.
def home(request):

    if request.user.is_authenticated:
        if request.user.role ==  "admin":
            return redirect("admin_dashboard")
        if request.user.role == "staff":
            return redirect("staff_dashboard")

        return redirect("customer_dashboard")
    return redirect("login")

def login_view(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        identifier = request.POST.get("identifier")
        password = request.POST.get("password")

        user = None

        user = authenticate(request, username=identifier, password=password)


        if user is None:
            try:
                phone_user = User.objects.get(phone=identifier)
                user = authenticate(request, username=phone_user.username, password=password)
            except User.DoesNotExist:
                pass

        if user is None:
            messages.error(request, "Invalid phone number or password.")
            return render(request, "accounts/login.html")

        login(request, user)
        if user.role == "admin" or user.is_superuser:
            return redirect("admin_dashboard")

        if user.role == "staff":
            return redirect("staff_dashboard")

        if user.role == "customer":
            return redirect("customer_dashboard")

        logout(request)
        messages.error(request, "Your account has an invalid role.")
        return redirect("login")
    
    return render(request, "accounts/login.html")

def phone_login(request):

    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":

        phone = normalize_phone(
            request.POST.get("phone")
        )

        if not phone:

            messages.error(
                request,
                "Please enter a valid phone number."
            )

            return render(
                request,
                "accounts/phone_login.html"
            )

        otp_code = generate_otp()

        PhoneOTP.objects.filter(
            phone=phone,
            is_verified=False
        ).delete()

        PhoneOTP.objects.create(
            phone=phone,
            otp=otp_code
        )

        request.session[
            "otp_phone"
        ] = phone

        # DEVELOPMENT ONLY
        print(
            f"OTP for {phone}: {otp_code}"
        )

        messages.success(
            request,
            "OTP sent successfully."
        )

        return redirect(
            "verify_otp"
        )

    return render(
        request,
        "accounts/phone_login.html"
    )

def verify_otp(request):

    phone = request.session.get(
        "otp_phone"
    )

    if not phone:
        return redirect("phone_login")

    if request.method == "POST":

        entered_otp = request.POST.get(
            "otp"
        )

        otp_record = (
            PhoneOTP.objects
            .filter(
                phone=phone,
                is_verified=False
            )
            .order_by(
                "-created_at"
            )
            .first()
        )

        if not otp_record:

            messages.error(
                request,
                "OTP not found. Request a new OTP."
            )

            return redirect(
                "phone_login"
            )

        if otp_record.is_expired():

            messages.error(
                request,
                "OTP has expired."
            )

            return redirect(
                "verify_otp"
            )

        if otp_record.attempts >= 5:

            messages.error(
                request,
                "Too many incorrect attempts. Request a new OTP."
            )

            return redirect(
                "phone_login"
            )

        if otp_record.otp != entered_otp:

            otp_record.attempts += 1

            otp_record.save(
                update_fields=[
                    "attempts"
                ]
            )

            messages.error(
                request,
                "Invalid OTP."
            )

            return redirect(
                "verify_otp"
            )

        otp_record.is_verified = True

        otp_record.save(
            update_fields=[
                "is_verified"
            ]
        )

        user = User.objects.filter(
            phone=phone,
            role="customer"
        ).first()

        if user:

            login(
                request,
                user,
                backend=(
                    "django.contrib.auth.backends."
                    "ModelBackend"
                )
            )

            request.session.pop(
                "otp_phone",
                None
            )

            return redirect(
                "customer_dashboard"
            )

        request.session[
            "verified_phone"
        ] = phone

        request.session.pop(
            "otp_phone",
            None
        )

        return redirect(
            "complete_profile"
        )

    return render(
        request,
        "accounts/verify_otp.html",
        {
            "phone": phone
        }
    )

def resend_otp(request):

    if request.method != "POST":
        return redirect("phone_login")

    phone = request.session.get(
        "otp_phone"
    )

    if not phone:
        return redirect("phone_login")

    otp_code = generate_otp()

    PhoneOTP.objects.filter(
        phone=phone,
        is_verified=False
    ).delete()

    PhoneOTP.objects.create(
        phone=phone,
        otp=otp_code
    )

    # DEVELOPMENT ONLY
    print(
        f"New OTP for {phone}: {otp_code}"
    )

    messages.success(
        request,
        "A new OTP has been sent."
    )

    return redirect(
        "verify_otp"
    )

def complete_profile(request):

    phone = request.session.get(
        "verified_phone"
    )

    if not phone:
        return redirect(
            "phone_login"
        )

    if User.objects.filter(
        phone=phone
    ).exists():

        request.session.pop(
            "verified_phone",
            None
        )

        return redirect(
            "phone_login"
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
                "Please enter your name."
            )

            return redirect(
                "complete_profile"
            )

        user = User.objects.create_user(
            username=phone,
            phone=phone,
            email=email,
            role="customer"
        )

        # OTP customers don't need a password.
        user.set_unusable_password()
        user.save()

        CustomerProfile.objects.create(
            user=user,
            name=name,
            phone=phone,
            email=email
        )

        login(
            request,
            user,
            backend=(
                "django.contrib.auth.backends."
                "ModelBackend"
            )
        )

        request.session.pop(
            "verified_phone",
            None
        )

        messages.success(
            request,
            "Welcome to Salon!"
        )

        return redirect(
            "customer_dashboard"
        )

    return render(
        request,
        "accounts/complete_profile.html",
        {
            "phone": phone
        }
    )

def logout_view(request):
    logout(request)
    return redirect("login")
