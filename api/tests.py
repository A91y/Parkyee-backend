from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Parking, ParkingAvailability, ParkingSlot
from .serializers import ParkingSerializer, ParkingAvailabilitySerializer, ParkingSlotSerializer
from django.contrib.auth.models import User


class ParkingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.parking_data = {
            'name': 'Test Parking',
            'address': '123 Test Street',
            'phone': '123-456-7890',
            'website': 'http://www.test.com',
            'price': '10.00',
            'description': 'Test parking description',
            'latitude': '123.456',
            'longitude': '789.012',
            'max_capacity': 100
        }
        self.response = self.client.post(
            reverse('parking-list'), self.parking_data, format='json')

    def test_create_parking(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_get_parking(self):
        parking = Parking.objects.get()
        response = self.client.get(
            reverse('parking-detail', kwargs={'pk': parking.id}), format='json')
        serializer = ParkingSerializer(parking)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_parking(self):
        parking = Parking.objects.get()
        updated_data = {
            'name': 'Updated Parking',
            'price': '15.00'
        }
        response = self.client.put(
            reverse('parking-detail', kwargs={'pk': parking.id}), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_parking(self):
        parking = Parking.objects.get()
        response = self.client.delete(
            reverse('parking-detail', kwargs={'pk': parking.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ParkingAvailabilityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.parking_data = {
            'name': 'Test Parking',
            'address': '123 Test Street',
            'phone': '123-456-7890',
            'website': 'http://www.test.com',
            'price': '10.00',
            'description': 'Test parking description',
            'latitude': '123.456',
            'longitude': '789.012',
            'max_capacity': 100
        }
        self.parking = Parking.objects.create(**self.parking_data)
        self.availability_data = {
            'parking': self.parking.id,
            'available': 50
        }
        self.response = self.client.post(
            reverse('parkingavailability-list'), self.availability_data, format='json')

    def test_create_parking_availability(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_get_parking_availability(self):
        availability = ParkingAvailability.objects.get()
        response = self.client.get(
            reverse('parkingavailability-detail', kwargs={'pk': availability.id}), format='json')
        serializer = ParkingAvailabilitySerializer(availability)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_parking_availability(self):
        availability = ParkingAvailability.objects.get()
        updated_data = {
            'available': 60
        }
        response = self.client.put(
            reverse('parkingavailability-detail', kwargs={'pk': availability.id}), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_parking_availability(self):
        availability = ParkingAvailability.objects.get()
        response = self.client.delete(
            reverse('parkingavailability-detail', kwargs={'pk': availability.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ParkingSlotTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.parking_data = {
            'name': 'Test Parking',
            'address': '123 Test Street',
            'phone': '123-456-7890',
            'website': 'http://www.test.com',
            'price': '10.00',
            'description': 'Test parking description',
            'latitude': '123.456',
            'longitude': '789.012',
            'max_capacity': 100
        }
        self.parking = Parking.objects.create(**self.parking_data)
        self.slot_data = {
            'parking': self.parking.id,
            'is_available': True
        }
        self.response = self.client.post(
            reverse('parkingslot-list'), self.slot_data, format='json')

    def test_create_parking_slot(self):
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_get_parking_slot(self):
        slot = ParkingSlot.objects.get()
        response = self.client.get(
            reverse('parkingslot-detail', kwargs={'pk': slot.id}), format='json')
        serializer = ParkingSlotSerializer(slot)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_parking_slot(self):
        slot = ParkingSlot.objects.get()
        updated_data = {
            'is_available': False
        }
        response = self.client.put(
            reverse('parkingslot-detail', kwargs={'pk': slot.id}), updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_parking_slot(self):
        slot = ParkingSlot.objects.get()
        response = self.client.delete(
            reverse('parkingslot-detail', kwargs={'pk': slot.id}), format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
