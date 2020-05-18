from django.contrib.auth.models import AnonymousUser, User
from django.test import RequestFactory, TestCase
from adminapp.views import hotels

class HotelsTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.get(email='t@t.ru')

    def test_details(self):
        # Create an instance of a GET request.
        request = self.factory.get('/management/hotels/')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Test my_view() as if it were deployed at /customer/details
        response = hotels(request)
        self.assertEqual(response.status_code, 200)