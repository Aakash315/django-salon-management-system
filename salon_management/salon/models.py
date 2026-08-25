from django.db import models
from accounts.models import StaffProfile

# Create your models here.
class Service(models.Model):

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    default_price = models.DecimalField(max_digits=10, decimal_places=2)
    default_duration = models.PositiveIntegerField(help_text="Duration in minutes")
    image = models.ImageField(upload_to='services/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class StaffService(models.Model):
    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='staff_services')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration = models.PositiveIntegerField(help_text="Duration in minutes")
    is_available = models.BooleanField(default=True)

    class Meta:
        unique_together = ('staff', 'service')

    def __str__(self):
        return f"{self.staff.name} - {self.service.name}"

class StaffAvailability(models.Model):
    DAYS = (
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday'),
    )

    staff = models.ForeignKey(StaffProfile, on_delete=models.CASCADE, related_name='availability')
    day = models.IntegerField(choices=DAYS)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    is_available = models.BooleanField(default=False)

    class Meta:
        unique_together = ('staff', 'day')

    def __str__(self):
        return (f"{self.staff.name} - {self.get_day_display()}")
