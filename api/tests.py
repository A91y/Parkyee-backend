from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from .models import Parking, ParkingAvailability, ParkingSlot

class ParkingTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_parking(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)
        
        data = {
            'name': 'Test Parking',
            'address': 'Test Address',
            'latitude': '123.456',
            'longitude': '789.012',
            'max_capacity': 100,
        }

        response = self.client.post('/parking/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_parking(self):
        response = self.client.get('/parking/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_parking(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)

        parking = Parking.objects.create(
            name='Test Parking',
            address='Test Address',
            latitude='123.456',
            longitude='789.012',
            max_capacity=100,
        )

        data = {
            'name': 'Updated Parking',
            'address': 'Updated Address',
        }

        response = self.client.put(f'/parking/{parking.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_parking(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)

        parking = Parking.objects.create(
            name='Test Parking',
            address='Test Address',
            latitude='123.456',
            longitude='789.012',
            max_capacity=100,
        )

        response = self.client.delete(f'/parking/{parking.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class ParkingAvailabilityTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_parking_availability(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)
        
        parking = Parking.objects.create(
            name='Test Parking',
            address='Test Address',
            latitude='123.456',
            longitude='789.012',
            max_capacity=100,
        )

        data = {
            'parking': f'/parking/{parking.id}/',
            'available': 50,
        }

        response = self.client.post('/parkingavailability/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_parking_availability(self):
        response = self.client.get('/parkingavailability/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_parking_availability(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)

        parking = Parking.objects.create(
            name='Test Parking',
            address='Test Address',
            latitude='123.456',
            longitude='789.012',
            max_capacity=100,
        )

        availability = ParkingAvailability.objects.create(
            parking=parking,
            available=50,
        )

        data = {
            'available': 60,
        }

        response = self.client.put(f'/parkingavailability/{availability.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_parking_availability(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)

        parking = Parking.objects.create(
            name='Test Parking',
            address='Test Address',
            latitude='123.456',
            longitude='789.012',
            max_capacity=100,
        )

        availability = ParkingAvailability.objects.create(
            parking=parking,
            available=50,
        )

        response = self.client.delete(f'/parkingavailability/{availability.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

class ParkingSlotTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_parking_slot(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)
        
        parking = Parking.objects.create(
            name='Test Parking',
            address='Test Address',
            latitude='123.456',
            longitude='789.012',
            max_capacity=100,
        )

        data = {
            'parking': f'/parking/{parking.id}/',
            'is_available': True,
        }

        response = self.client.post('/parkingslot/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_parking_slot(self):
        response = self.client.get('/parkingslot/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_parking_slot(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)

        parking = Parking.objects.create(
            name='Test Parking',
            address='Test Address',
            latitude='123.456',
            longitude='789.012',
            max_capacity=100,
        )

        slot = ParkingSlot.objects.create(
            parking=parking,
            is_available=True,
        )

        data = {
            'is_available': False,
        }

        response = self.client.put(f'/parkingslot/{slot.id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_parking_slot(self):
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.force_authenticate(user=user)

        parking = Parking.objects.create(
            name='Test Parking',
            address='Test Address',
            latitude='123.456',
            longitude='789.012',
            max_capacity=100,
        )

        slot = ParkingSlot.objects.create(
            parking=parking,
            is_available=True,
        )

        response = self.client.delete(f'/parkingslot/{slot.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
