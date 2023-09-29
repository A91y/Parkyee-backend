from django.shortcuts import render
from .serializers import ParkingSerializer, ParkingAvailabilitySerializer, ParkingSlotSerializer
from .models import Parking, ParkingAvailability, ParkingSlot
from rest_framework import viewsets, generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.
# @method_decorator(csrf_exempt, name='dispatch')


class ParkingViewSet(viewsets.ModelViewSet):
    queryset = Parking.objects.all()
    serializer_class = ParkingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
# @method_decorator(csrf_exempt, name='dispatch')


class ParkingAvailabilityViewSet(viewsets.ModelViewSet):
    queryset = ParkingAvailability.objects.all()
    serializer_class = ParkingAvailabilitySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ParkingSlotViewSet(viewsets.ModelViewSet):
    queryset = ParkingSlot.objects.all()
    serializer_class = ParkingSlotSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


# from rest_framework.views import APIView
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from .serializers import UserSerializer

# class MeView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         serializer = UserSerializer(request.user)
#         return Response(serializer.data)
