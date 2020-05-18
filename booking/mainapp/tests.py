from django.test import TestCase
from authapp.models import User
from mainapp.models import Hotel, Room


class RoomsTestCase(TestCase):
    def setUp(self):
        self.superuser = User.objects.create_superuser(
            'django2@geekshop.local',
            'geekbrains')
        hotel = Hotel.objects.create(name="Test Hotel", user_id=1)
        self.room_1 = Room.objects.create(name="room 1",
                                          hotel=hotel,
                                          price=2000)

        self.room_2 = Room.objects.create(name="room 2",
                                          hotel=hotel,
                                          price=9999,
                                          is_active=False)

        self.room_3 = Room.objects.create(name="room 3",
                                          hotel=hotel,
                                          price=1000)

    def test_room_get(self):
        room_1 = Room.objects.get(name="room 1")
        room_2 = Room.objects.get(name="room 2")
        self.assertEqual(room_1, self.room_1)
        self.assertEqual(room_2, self.room_2)

    def test_room_print(self):
        room_1 = Room.objects.get(name="room 1")
        room_2 = Room.objects.get(name="room 2")
        self.assertEqual(str(room_1), 'room 1 (Test Hotel)')
        self.assertEqual(str(room_2), 'room 2 (Test Hotel)')
