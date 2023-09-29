from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import ParkingAvailability, ParkingSlot, Parking


@receiver(post_save, sender=ParkingAvailability)
def update_parking_availability_count(sender, instance, **kwargs):
    instance.parking.update_availability_count()


@receiver([post_save, post_delete], sender=ParkingSlot)
def update_max_capacity(sender, instance, **kwargs):
    """
    Signal handler to update max_capacity in Parking model based on the count of available parking slots.
    """
    parking = instance.parking
    available_slots_count = ParkingSlot.objects.filter(parking=parking).count()
    parking.max_capacity = available_slots_count
    parking.save()


@receiver([post_save, post_delete], sender=ParkingSlot)
def update_parking_availability(sender, instance, **kwargs):
    parking = instance.parking
    availability, created = ParkingAvailability.objects.get_or_create(
        parking=parking)
    slots = ParkingSlot.objects.filter(
        parking=parking, is_available=True).count()
    availability.available = slots
    availability.save()

@receiver(post_save, sender=Parking)
def create_parking_availability(sender, instance, created, **kwargs):
    if created:
        if not ParkingAvailability.objects.filter(parking=instance).exists():
            ParkingAvailability.objects.create(parking=instance, available=0)