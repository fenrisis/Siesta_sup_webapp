from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=15)
    
    def __str__(self):
        return self.username

class SUPBoard(models.Model):
    name = models.CharField(max_length=100)

class RentalSlot(models.Model):
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)  # Allow null values
    end_time = models.TimeField(null=True, blank=True)    # Allow null values
    capacity = models.IntegerField(default=1)
    sup_board = models.ForeignKey(SUPBoard, on_delete=models.CASCADE)
    renter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    selected_seats = models.IntegerField(default=0)

    def __str__(self):
        return f"Rental Slot: {self.id}, Date: {self.date}, SUP Board: {self.sup_board.name}"

    def is_available(self):
        return self.renter is None

    def is_full(self):
        return self.selected_seats >= self.capacity

class Order(models.Model):
    rental_slot = models.ForeignKey(RentalSlot, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order: {self.id}, User: {self.user.username}, Rental Slot: {self.rental_slot.id}"
