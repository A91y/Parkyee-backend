from django.shortcuts import render
from .serializers import (
    ParkingSerializer,
    ParkingAvailabilitySerializer,
    ParkingSlotSerializer
)
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404
from django.urls import reverse
from .models import Parking, ParkingAvailability, ParkingSlot
from rest_framework import viewsets, permissions
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from django.shortcuts import get_object_or_404
# Disable CSRF for simplicity in testing, but consider enabling it for production


@method_decorator(csrf_exempt, name='dispatch')
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
class ParkingViewSet(viewsets.ModelViewSet):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        # Create a URL for the parking slot details page
        parking_slots = reverse('parking-slots', args=[instance.id])

        # Add the parking slot URL to the response data
        data = serializer.data

        data['get_parking_slots'] = request._current_scheme_host + parking_slots
        data['get_parking_availability'] = request._current_scheme_host + \
            reverse('parkingavailability-detail', args=[instance.id])
        return Response(data)

@method_decorator(csrf_exempt, name='dispatch')
class ParkingAvailabilityViewSet(viewsets.ModelViewSet):
    http_method_names = ["get"]
    queryset = ParkingAvailability.objects.all()
    serializer_class = ParkingAvailabilitySerializer


@method_decorator(csrf_exempt, name='dispatch')
@authentication_classes([SessionAuthentication, BasicAuthentication, TokenAuthentication])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
class ParkingSlotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSlot.objects.all()
    serializer_class = ParkingSlotSerializer


    # def create(self, request, *args, **kwargs):
    #     # Get the parking ID and unique_id from the request data
    #     print(request.data)
    #     parking = request.data.get('parking')
    #     parking_id = parking.split('/')[-2]
    #     request_data = request.data.copy()
    #     request_data['parking_id'] = parking_id
    #     unique_id = request.data.get('unique_id')
    #     # Check if a parking slot with the same unique_id exists for the same parking
    #     existing_slot = ParkingSlot.objects.filter(parking=parking_id, unique_id=unique_id).first()
    #     print(parking_id, unique_id, existing_slot)
    #     if existing_slot:
    #         return Response(
    #             {"detail": "Parking slot with this unique id already exists for the same parking."},
    #             status=status.HTTP_400_BAD_REQUEST
    #         )
    #     serializer = self.get_serializer(data=request_data)
    #     if not serializer.is_valid():
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #     else:
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

        # return super().create(request, *args, **kwargs)
        

@method_decorator(csrf_exempt, name='dispatch')
class ParkingSlotListView(viewsets.ModelViewSet):
    # http_method_names = ["get"]
    serializer_class = ParkingSlotSerializer
    def get_queryset(self):
        # Retrieve the parking URL parameter from the URL
        parking_id = self.kwargs['parking_id']
        print(parking_id)

        # Filter parking slots based on the parking URL
        if Parking.objects.filter(id=parking_id).exists():
            return ParkingSlot.objects.filter(parking_id=parking_id)
        else:
            raise Http404

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

@method_decorator(csrf_exempt, name='dispatch')
class ParkingSlotDetailView(viewsets.ModelViewSet):
    queryset = ParkingSlot.objects.all()
    serializer_class = ParkingSlotSerializer

    def retrieve(self, request, parking_id=None, pk=None):
        try:
            parking_slot = ParkingSlot.objects.get(parking_id=parking_id, pk=pk)
        except ParkingSlot.DoesNotExist:
            raise Http404

        serializer = self.get_serializer(parking_slot)
        return Response(serializer.data)

    def update(self, request, parking_id=None, pk=None):
        parking_slot = get_object_or_404(ParkingSlot, parking_id=parking_id, pk=pk)
        serializer = self.get_serializer(parking_slot, data=request.data)

        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, parking_id=None, pk=None):
        parking_slot = get_object_or_404(ParkingSlot, parking_id=parking_id, pk=pk)
        parking_slot.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
