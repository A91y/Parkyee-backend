from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Parking, ParkingSlot, ParkingAvailability
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

User = get_user_model()

class ParkingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def create_parking(self):
        return Parking.objects.create(name='Test Parking', address='Test Address')

    def test_create_parking(self):
        response = self.client.post(
            reverse('parking-list'),
            {
                'name': 'Test Parking',
                'address': 'Test Address',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_parking_list(self):
        self.create_parking()
        self.create_parking()
        response = self.client.get(reverse('parking-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_parking_detail(self):
        parking = self.create_parking()
        response = self.client.get(reverse('parking-detail', args=[parking.id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Parking')

    def test_update_parking(self):
        parking = self.create_parking()
        response = self.client.put(
            reverse('parking-detail', args=[parking.id]),
            {
                'name': 'Updated Parking',
                'address': 'Updated Address',
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parking.refresh_from_db()
        self.assertEqual(parking.name, 'Updated Parking')
        self.assertEqual(parking.address, 'Updated Address')

    def test_delete_parking(self):
        parking = self.create_parking()
        response = self.client.delete(reverse('parking-detail', args=[parking.id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Parking.objects.count(), 0)

    def test_delete_nonexistent_parking(self):
        response = self.client.delete(reverse('parking-detail', args=[999]))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

class ParkingSlotTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')

    def create_parking_slot(self):
        parking = Parking.objects.create(name="Test Parking", address="Test Address")
        availability = ParkingAvailability.objects.create(parking=parking, available=0)
        return ParkingSlot.objects.create(parking=parking, is_available=True)

    def test_create_parking_slot(self):
        parking_slot = self.create_parking_slot()
        parking_url = reverse('parking-detail', args=[parking_slot.parking.id])  # Generate the parking URL
        response = self.client.post(
            reverse('parkingslot-list'),
            {
                'parking': parking_url,
                'is_available': True,
            },
            format='json'
        )
        # print(response.status_code)
        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_delete_parking_slot(self):
        parking_slot = self.create_parking_slot()
        print("Parking Slot unique_id:", parking_slot.unique_id)
        response = self.client.delete(reverse('parkingslot-detail', args=[parking_slot.unique_id]))
        print(response.data)
        print(reverse('parkingslot-detail', args=[parking_slot.unique_id]))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ParkingSlot.objects.count(), 0)

    def test_update_parking_slot(self):
        parking_slot = self.create_parking_slot()
        response = self.client.put(
            reverse('parkingslot-detail', args=[parking_slot.unique_id]),
            {
                'is_available': False,
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        parking_slot.refresh_from_db()
        self.assertFalse(parking_slot.is_available)

    def test_get_parking_slot_list(self):
        parking_slot1 = self.create_parking_slot()
        parking_slot2 = self.create_parking_slot()
        response = self.client.get(reverse('parkingslot-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_parking_slot_detail(self):
        parking_slot = self.create_parking_slot()
        response = self.client.get(reverse('parkingslot-detail', args=[parking_slot.unique_id]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['is_available'], True)
