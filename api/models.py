from django.db import models
import os
from django.utils.deconstruct import deconstructible
from uuid import uuid4
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


@deconstructible
class UploadToPathAndRename(object):

    def __init__(self, path):
        self.sub_path = path

    def __call__(self, instance, filename):
        ext = filename.split('.')[-1]
        # get filename
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            # set filename as random string
            filename = '{}.{}'.format(uuid4().hex, ext)
        # return the whole path to the file
        return os.path.join(self.sub_path, filename)

# Create your models here.


class Parking(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, blank=True, null=True)
    website = models.CharField(max_length=100, blank=True, null=True)
    image = models.ImageField(upload_to=UploadToPathAndRename(
        'images/'), blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    description = models.CharField(max_length=100, blank=True, null=True)
    latitude = models.CharField(max_length=100)
    longitude = models.CharField(max_length=100)
    max_capacity = models.PositiveBigIntegerField(default=0, editable=False)
    availability_count = models.PositiveIntegerField(default=0, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    last_updated_at = models.DateTimeField(auto_now=True)

    def update_availability_count(self):
        try:
            availability = ParkingAvailability.objects.get(parking=self)
            self.availability_count = availability.available
        except ParkingAvailability.DoesNotExist:
            self.availability_count = 0
        self.save()

    def clean(self):
        super().clean()
        if self.max_capacity <= 0:
            raise ValidationError("Max capacity must be a positive integer.")

    def __str__(self):
        return self.name + ' - ' + self.address


class ParkingAvailability(models.Model):
    parking = models.OneToOneField(Parking, on_delete=models.CASCADE)
    available = models.IntegerField()

    def clean(self):
        super().clean()
        if self.available > self.parking.max_capacity:
            raise ValidationError(
                "Available spaces cannot exceed max capacity.")

    def __str__(self):
        return self.parking.name + ' - ' + str(self.available) + '/' + str(self.parking.max_capacity)


class ParkingSlot(models.Model):
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE)
    unique_id = models.IntegerField(
        auto_created=True, primary_key=True, serialize=True)
    is_available = models.BooleanField(default=True)

    def __str__(self) -> str:
        return str(self.unique_id) + ' - ' + str(self.parking.name) + ' - ' + str(self.is_available)
