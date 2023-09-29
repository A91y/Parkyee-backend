from rest_framework import serializers
from .models import Parking, ParkingAvailability, ParkingSlot
from django.contrib.auth import get_user_model

User = get_user_model()


class ParkingSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Parking
        fields = '__all__'


class ParkingAvailabilitySerializer(serializers.HyperlinkedModelSerializer):
    unique_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = ParkingAvailability
        fields = '__all__'

class ParkingSlotSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = ParkingSlot
        fields = '__all__'
