from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from .models import Parking, ParkingSlot, ParkingAvailability
from django.contrib.auth.models import User


class ParkingTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.client.login(username='testuser', password='testpassword')
    def test_create_parking(self):
        # Create a new parking using API
        response = self.client.post(
            reverse('parking-list'),
            {
                'name': 'Test Parking',
                'address': 'Test Address',
                'latitude': '12.3456',
                'longitude': '78.9101',
                'max_capacity': 100,
            },
            format='json'
        )

        # Check if the request was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Parking.objects.count(), 1)
        self.assertEqual(Parking.objects.get().name, 'Test Parking')

    def test_get_parking_list(self):
        # Create some parking objects
        Parking.objects.create(name='Parking 1', address='Address 1',
                               latitude='12.3456', longitude='78.9101', max_capacity=50)
        Parking.objects.create(name='Parking 2', address='Address 2',
                               latitude='12.3456', longitude='78.9101', max_capacity=75)

        # Retrieve the list of parking using API
        response = self.client.get(reverse('parking-list'))

        # Check if the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_parking_detail(self):
        # Create a parking object
        parking = Parking.objects.create(
            name='Test Parking', address='Test Address', latitude='12.3456', longitude='78.9101', max_capacity=100)

        # Retrieve the detail of the parking using API
        response = self.client.get(reverse('parking-detail', args=[parking.id]))

        # Check if the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Parking')

    def test_update_parking(self):
        # Create a parking object
        parking = Parking.objects.create(
            name='Test Parking', address='Test Address', latitude='12.3456', longitude='78.9101', max_capacity=100)

        # Update the parking using API
        response = self.client.put(
            reverse('parking-detail', args=[parking.id]),
            {
                'name': 'Updated Parking',
                'address': 'Updated Address',
                'latitude': '12.3456',
                'longitude': '78.9101',
                'max_capacity': 75,
            },
            format='json'
        )

        # Check if the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh the parking instance from the database
        parking.refresh_from_db()

        # Check if the parking details are updated
        self.assertEqual(parking.name, 'Updated Parking')
        self.assertEqual(parking.address, 'Updated Address')

    def test_delete_parking(self):
        # Create a parking object
        parking = Parking.objects.create(
            name='Test Parking', address='Test Address', latitude='12.3456', longitude='78.9101', max_capacity=100)

        # Delete the parking using API
        response = self.client.delete(reverse('parking-detail', args=[parking.id]))

        # Check if the request was successful
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Parking.objects.count(), 0)

    def test_create_parking_availability(self):
        # Create a parking object
        parking = Parking.objects.create(
            name='Test Parking', address='Test Address', latitude='12.3456', longitude='78.9101', max_capacity=100)

        # Create parking availability using API
        response = self.client.post(
            reverse('parkingavailability-list'),
            {
                'parking': parking.id,
                'available': 50,
            },
            format='json'
        )

        # Check if the request was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ParkingAvailability.objects.count(), 1)
        self.assertEqual(ParkingAvailability.objects.get().available, 50)

    def test_create_parking_slot(self):
        # Create a parking object
        parking = Parking.objects.create(
            name='Test Parking', address='Test Address', latitude='12.3456', longitude='78.9101', max_capacity=100)

        # Create a new parking slot using API
        response = self.client.post(
            reverse('parkingslot-list'),
            {
                'parking': parking.id,
                'is_available': True,
            },
            format='json'
        )

        # Check if the request was successful
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ParkingSlot.objects.count(), 1)
        self.assertTrue(ParkingSlot.objects.get().is_available)

    # Add more tests as needed

# class ParkingSlotTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#     def test_create_parking_slot(self):
#         # Create a parking object
#         parking = Parking.objects.create(
#             name='Test Parking', address='Test Address', latitude='12.3456', longitude='78.9101', max_capacity=100)

#         # Create a new parking slot using API
#         response = self.client.post(
#             reverse('parkingslot-list'),
#             {
#                 'parking': parking.id,
#                 'is_available': True,
#             },
#             format='json'
#         )

#         # Check if the request was successful
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(ParkingSlot.objects.count(), 1)
#         self.assertTrue(ParkingSlot.objects.get().is_available)

#     def test_update_parking_slot(self):
#         # Create a parking object
#         parking = Parking.objects.create(
#             name='Test Parking', address='Test Address', latitude='12.3456', longitude='78.9101', max_capacity=100)

#         # Create a parking slot
#         slot = ParkingSlot.objects.create(
#             parking=parking, is_available=True)

#         # Update the parking slot using API
#         response = self.client.put(
#             reverse('parkingslot-detail', args=[slot.id]),
#             {
#                 'is_available': False,
#             },
#             format='json'
#         )

#         # Check if the request was successful
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Refresh the parking slot instance from the database
#         slot.refresh_from_db()

#         # Check if the parking slot details are updated
#         self.assertFalse(slot.is_available)

#     def test_get_parking_slot_list(self):
#         # Create a parking object
#         parking = Parking.objects.create(
#             name='Test Parking', address='Test Address', latitude='12.3456', longitude='78.9101', max_capacity=100)

#         # Create multiple parking slots
#         slots_data = [
#             {'parking': parking.id, 'is_available': True},
#             {'parking': parking.id, 'is_available': True},
#             {'parking': parking.id, 'is_available': False},
#         ]
#         for slot_data in slots_data:
#             ParkingSlot.objects.create(**slot_data)

#         # Retrieve the list of parking slots using API
#         response = self.client.get(reverse('parkingslot-list'))

#         # Check if the request was successful
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), len(slots_data))

#     def test_get_parking_slot_detail(self):
#         # Create a parking object
#         parking = Parking.objects.create(
#             name='Test Parking', address='Test Address', latitude='12.3456', longitude='78.9101', max_capacity=100)

#         # Create a parking slot
#         slot = ParkingSlot.objects.create(
#             parking=parking, is_available=True)

#         # Retrieve the detail of the parking slot using API
#         response = self.client.get(reverse('parkingslot-detail', args=[slot.id]))

#         # Check if the request was successful
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(response.data['is_available'])

#     def test_delete_parking_slot(self):
#         # Create a parking object
#         parking = Parking.objects.create(
#             name='Test Parking', address='Test Address', latitude='12.3456', longitude='78.9101', max_capacity=100)

#         # Create a parking slot
#         slot = ParkingSlot.objects.create(
#             parking=parking, is_available=True)

#         # Delete the parking slot using API
#         response = self.client.delete(
#             reverse('parkingslot-detail', args=[slot.id]))

#         # Check if the request was successful
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(ParkingSlot.objects.count(), 0)

#     # Add more tests as needed


# class ParkingAvailabilityTests(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#     def test_create_parking_availability(self):
#         # Create a parking object
#         parking = Parking.objects.create(
#             name='Test Parking', address='Test Address', latitude='12.3456', longitude='78.9101', max_capacity=100)

#         # Create a new parking availability using API
#         response = self.client.post(
#             reverse('parkingavailability-list'),
#             {
#                 'parking': parking.id,
#                 'available': 50,
#             },
#             format='json'
#         )

#         # Check if the request was successful
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)
#         self.assertEqual(ParkingAvailability.objects.count(), 1)
#         self.assertEqual(ParkingAvailability.objects.get().available, 50)

#     def test_update_parking_availability(self):
#         # Create a parking object
#         parking = Parking.objects.create(
#             name='Test Parking', address='Test Address', latitude='12.3456', longitude='78.9101', max_capacity=100)

#         # Create a parking availability
#         availability = ParkingAvailability.objects.create(
#             parking=parking, available=30)

#         # Update the parking availability using API
#         response = self.client.put(
#             reverse('parkingavailability-detail', args=[availability.id]),
#             {
#                 'available': 40,
#             },
#             format='json'
#         )

#         # Check if the request was successful
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#         # Refresh the parking availability instance from the database
#         availability.refresh_from_db()

#         # Check if the parking availability details are updated
#         self.assertEqual(availability.available, 40)

#     def test_get_parking_availability_list(self):
#         # Create a parking object
#         parking = Parking.objects.create(
#             name='Test Parking', address='Test Address', latitude='12.3456', longitude='78.9101', max_capacity=100)

#         # Create multiple parking availabilities
#         availabilities_data = [
#             {'parking': parking.id, 'available': 10},
#             {'parking': parking.id, 'available': 20},
#             {'parking': parking.id, 'available': 30},
#         ]
#         for availability_data in availabilities_data:
#             ParkingAvailability.objects.create(**availability_data)

#         # Retrieve the list of parking availabilities using API
#         response = self.client.get(reverse('parkingavailability-list'))

#         # Check if the request was successful
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), len(availabilities_data))

#     def test_get_parking_availability_detail(self):
#         # Create a parking object
#         parking = Parking.objects.create(
#             name='Test Parking', address='Test Address', latitude='12.3456', longitude='78.9101', max_capacity=100)

#         # Create a parking availability
#         availability = ParkingAvailability.objects.create(
#             parking=parking, available=25)

#         # Retrieve the detail of the parking availability using API
#         response = self.client.get(
#             reverse('parkingavailability-detail', args=[availability.id]))

#         # Check if the request was successful
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data['available'], 25)

#     def test_delete_parking_availability(self):
#         # Create a parking object
#         parking = Parking.objects.create(
#             name='Test Parking', address='Test Address', latitude='12.3456', longitude='78.9101', max_capacity=100)

#         # Create a parking availability
#         availability = ParkingAvailability.objects.create(
#             parking=parking, available=50)

#         # Delete the parking availability using API
#         response = self.client.delete(
#             reverse('parkingavailability-detail', args=[availability.id]))

#         # Check if the request was successful
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
#         self.assertEqual(ParkingAvailability.objects.count(), 0)

#     # Add more tests as needed


