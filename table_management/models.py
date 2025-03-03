# table_management/models.py
from django.db import models
from django.conf import settings

class Table(models.Model):
    """Restaurant table model"""
    name = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    is_available = models.BooleanField(default=True)
    location = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} (Capacity: {self.capacity})"

class Reservation(models.Model):
    """Table reservation model"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reservations')
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='reservations')
    reservation_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    party_size = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-reservation_date', '-start_time']
        # Prevent double booking
        constraints = [
            models.UniqueConstraint(
                fields=['table', 'reservation_date', 'start_time'],
                name='unique_reservation'
            )
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.table.name} - {self.reservation_date} {self.start_time}"