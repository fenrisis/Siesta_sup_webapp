from django.contrib import admin
from .models import CustomUser, SUPBoard, RentalSlot
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(SUPBoard)
admin.site.register(RentalSlot)