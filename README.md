# 💇 Salon Management System

A full-stack **Salon Management System** built with **Python and Django**.

The system provides separate dashboards for **Admin, Staff, and Customers**, allowing a salon to manage staff, services, appointments, working hours, pricing, availability, reports, and customer bookings.

---

## 📌 Features

### 👨‍💼 Admin Dashboard

The admin can manage the complete salon system.

* 🔐 Admin authentication
* 📊 Admin dashboard
* 👥 Manage staff

  * Add staff
  * Edit staff
  * Remove staff
* 💇 Manage salon services
* 💰 Manage service prices
* ⏱️ Manage service duration
* 👨‍🔧 Manage staff services
* 📅 Manage staff availability
* 📋 Manage appointments
* 📈 View salon reports
* 📅 Daily reports
* 📆 Weekly reports
* 🗓️ Monthly reports
* 👨‍🔧 Staff-wise reports
* 📅 Staff daily reports
* 📆 Staff weekly reports
* 🗓️ Staff monthly reports
* ⭐ View popular services
* 💵 View revenue
* ✅ View completed bookings
* ⏳ View pending bookings
* ✔️ View confirmed bookings
* ❌ View cancelled bookings
* 📋 View appointment details

---

### 💇 Staff Dashboard

Staff members have their own dashboard to manage their profile, services, availability, and appointments.

Staff can:

* 🔐 Login using their account
* 📊 View staff dashboard
* 👤 Manage their profile
* 📅 View appointments
* 💇 View assigned services
* 💰 Change service price
* ⏱️ Change service duration
* ✅ Enable/disable services
* 📆 Manage availability
* 📅 Set working days
* 🕐 Set working hours
* 👥 View customer appointments
* 📋 View appointment status

---

### 👤 Customer Dashboard

Customers can create and manage salon appointments.

Customers can:

* 🔐 Login using phone number and password
* 📊 View customer dashboard
* 💇 Browse available services
* 👨‍🔧 Select staff
* 📅 Select appointment date
* 🕐 View available time slots
* ⏰ Select appointment time
* 💰 View service price
* ⏱️ View service duration
* 📝 Add appointment notes
* 📌 Book appointments
* ✅ View booking confirmation
* 📋 View their appointments
* ❌ Cancel appointments

---

## 📅 Smart Appointment Booking

The booking system dynamically generates available appointment slots based on multiple conditions.

### Booking Flow

```text
Select Service
      ↓
Select Staff
      ↓
Select Date
      ↓
Check Staff Availability
      ↓
Check Working Days
      ↓
Check Working Hours
      ↓
Calculate Service Duration
      ↓
Check Existing Appointments
      ↓
Check Appointment Status
      ↓
Generate Available Time Slots
      ↓
Select Available Slot
      ↓
Book Appointment
```

The system considers:

* Selected service
* Selected staff
* Staff working days
* Staff working hours
* Service duration
* Existing appointments
* Appointment status
* Selected date
* Current time
* Double-booking prevention

---

## 🔐 Authentication & User Roles

The application supports three different user roles.

```text
                         Login
                           │
             ┌─────────────┼─────────────┐
             ↓             ↓             ↓
           Admin          Staff       Customer
             │             │             │
             ↓             ↓             ↓
       Admin Dashboard  Staff Dashboard  Customer Dashboard
```

### 👤 Customer Login

Customers can log in using:

* Phone number
* Password

### 💇 Staff Login

Staff members can log in using their configured account credentials.

### 👨‍💼 Admin Login

Admin/superuser accounts are redirected to the Admin Dashboard.

---

# 🛠️ Technologies Used

## Backend

* Python
* Django
* Django ORM
* Django Authentication
* Django Templates

## Frontend

* HTML5
* CSS3
* JavaScript
* Bootstrap

## Database

* SQLite — Development
* PostgreSQL — Production

## Development Tools

* Visual Studio Code
* Git
* GitHub

---

# 📂 Project Structure

```text
salon-management-system/
│
├── salon_management/
│   │
│   ├── salon_management/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   ├── accounts/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── salon/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   └── ...
│   │
│   ├── dashboard/
│   │   ├── admin_views.py
│   │   ├── admin_urls.py
│   │   ├── staff_views.py
│   │   ├── staff_urls.py
│   │   ├── customer_views.py
│   │   ├── customer_urls.py
│   │   └── ...
│   │
│   ├── appointments/
│   │   ├── migrations/
│   │   ├── models.py
│   │   ├── views.py
│   │   └── ...
│   │
│   ├── templates/
│   │   ├── base.html
│   │   │
│   │   ├── accounts/
│   │   │   └── login.html
│   │   │
│   │   ├── admin_dashboard/
│   │   │   ├── dashboard.html
│   │   │   ├── reports.html
│   │   │   ├── staff_reports.html
│   │   │   └── sidebar.html
│   │   │
│   │   ├── staff/
│   │   │   ├── dashboard.html
│   │   │   ├── profile.html
│   │   │   └── sidebar.html
│   │   │
│   │   └── customer/
│   │       ├── dashboard.html
│   │       ├── booking.html
│   │       ├── booking_success.html
│   │       └── sidebar.html
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   ├── manage.py
│   ├── requirements.txt
│   ├── .gitignore
│   └── README.md
```

> **Note:** `db.sqlite3` is intentionally excluded from the GitHub repository. A new database is created locally when migrations are run.

---

# ⚙️ Installation & Setup

Follow these steps to run the project locally.

## 1. Clone the Repository

```bash
git clone https://github.com/Aakash315/django-salon-management-system.git
```

## 2. Enter the Project Directory

```bash
cd django-salon-management-system
```

---

## 3. Create a Virtual Environment

### Windows

```bash
python -m venv env
```

Activate the environment:

```powershell
env\Scripts\activate
```

### macOS / Linux

```bash
python3 -m venv env
```

Activate:

```bash
source env/bin/activate
```

---

## 📦 4. Install Dependencies

Install all required Python packages:

```bash
pip install -r requirements.txt
```

If `requirements.txt` does not exist, create it using:

```bash
pip freeze > requirements.txt
```

---

## 🗄️ 5. Configure Environment Variables

If the project uses environment variables, create a `.env` file in the project root.

Example:

```env
SECRET_KEY=your-secret-key
DEBUG=True
```

> ⚠️ Do not upload `.env` to GitHub. Add `.env` to `.gitignore`.

---

## 🗄️ 6. Run Database Migrations

Create migrations if required:

```bash
python manage.py makemigrations
```

Apply migrations:

```bash
python manage.py migrate
```

This will create a new local `db.sqlite3` database.

---

## 👨‍💼 7. Create Admin Account

Create a Django superuser:

```bash
python manage.py createsuperuser
```

Enter the requested details:

```text
Username:
Email:
Password:
Password confirmation:
```

---

## ▶️ 8. Start the Development Server

Run:

```bash
python manage.py runserver
```

Open the application in your browser:

```text
http://127.0.0.1:8000/
```

---

# 🔒 Security

The application uses several Django security features:

* CSRF protection
* Django authentication
* Login-required decorators
* Role-based access control
* Server-side booking validation
* Double-booking protection
* Environment variables for sensitive settings
* Password-protected user accounts

### ⚠️ Sensitive Files

The following files should not be committed to GitHub:

```text
db.sqlite3
.env
env/
venv/
__pycache__/
*.pyc
```

---

# 📊 Reports

The Admin Dashboard includes reporting functionality.

### Salon Reports

* Daily revenue report
* Weekly revenue report
* Monthly revenue report
* Completed bookings
* Pending bookings
* Confirmed bookings
* Cancelled bookings
* Popular services

### Staff Reports

Admin can select a specific staff member and view:

* Staff daily report
* Staff weekly report
* Staff monthly report
* Staff appointments
* Staff revenue
* Staff completed bookings

---

# 🚀 Future Improvements

Possible future features include:

* 💳 Online payment integration
* 💰 Razorpay / Stripe integration
* 📧 Email notifications
* 💬 WhatsApp notifications
* 📱 SMS OTP login
* 🔐 Customer OTP registration
* 🔔 Appointment reminders
* 👥 Staff attendance management
* 💵 Staff salary management
* 📊 Staff commission calculation
* 📦 Product inventory management
* 💸 Expense management
* ⭐ Customer reviews
* 🎁 Loyalty points
* 🏷️ Coupon system
* 🎫 Gift cards
* 📈 Advanced analytics
* 📄 PDF reports
* 📊 Excel report export
* 📊 Dashboard charts
* 🏢 Multi-branch salon support

---

# 🧪 Development

To check the Django project for common issues:

```bash
python manage.py check
```

To run tests:

```bash
python manage.py test
```

---

# 🌐 Production Deployment

For production deployment, PostgreSQL is recommended instead of SQLite.

Possible deployment platforms include:

* Render
* Railway
* PythonAnywhere
* AWS
* DigitalOcean

Before production deployment, configure:

* `DEBUG=False`
* Production `SECRET_KEY`
* Allowed hosts
* PostgreSQL database
* Static files
* Media files
* HTTPS
* Environment variables

---

# 👨‍💻 Author

**Aakash Jaiswal**

Full Stack Python Developer

* GitHub: [@Aakash315](https://github.com/Aakash315)

---

# ⭐ Support

If you find this project useful, please consider giving the repository a ⭐ on GitHub.

---

## 📄 License

This project is available for educational and development purposes.

---
