from django.test import TestCase
from django.contrib import auth
from network.models import User
# Create your tests here.

class TestModel(TestCase):
    def test_should_create_user(self):
        user = User.objects.create_user(
            username='username',email='email@app/com'
        )
        user.set_password('123+789Asd')
        user.save()
        self.assertEqual(str(user),'username')