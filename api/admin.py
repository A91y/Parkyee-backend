from django.contrib import admin

# Register your models here.
from .models import Parking, ParkingAvailability, ParkingSlot

admin.site.register(Parking)
admin.site.register(ParkingAvailability)
admin.site.register(ParkingSlot)
