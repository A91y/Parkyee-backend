from django.shortcuts import render
from .serializers import (
    ParkingSerializer,
    ParkingAvailabilitySerializer,
    ParkingSlotSerializer,
)
from .models import Parking, ParkingAvailability, ParkingSlot
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication

# Disable CSRF for simplicity in testing, but consider enabling it for production
@method_decorator(csrf_exempt, name='dispatch')
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
class ParkingViewSet(viewsets.ModelViewSet):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer

@method_decorator(csrf_exempt, name='dispatch')
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
class ParkingAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = ParkingAvailability.objects.all()
    serializer_class = ParkingAvailabilitySerializer

@method_decorator(csrf_exempt, name='dispatch')
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
class ParkingSlotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSlot.objects.all()
    serializer_class = ParkingSlotSerializer
