from django.test import TestCase
from core.models import User


class UserModelTest(TestCase):
    def setUp(self):
        User.objects.create(phone='09123456789')

    def test_str_representation(self):
        user = User.objects.get(phone='09123456789')
        expected_str = '09123456789'
        self.assertEqual(str(user), expected_str)

    def test_fullname_field(self):
        user = User.objects.get(phone='09123456789')
        self.assertIsNone(user.fullname)

    def test_email_field(self):
        user = User.objects.get(phone='09123456789')
        self.assertEqual(user.email, '')

    def test_phone_field(self):
        user = User.objects.get(phone='09123456789')
        expected_phone = '09123456789'
        self.assertEqual(user.phone, expected_phone)

    def test_is_staff_field(self):
        user = User.objects.get(phone='09123456789')
        self.assertFalse(user.is_staff)

    def test_is_active_field(self):
        user = User.objects.get(phone='09123456789')
        self.assertTrue(user.is_active)

    def test_date_joined_field(self):
        user = User.objects.get(phone='09123456789')
        self.assertIsNotNone(user.date_joined)

    def test_username_field(self):
        user = User.objects.get(phone='09123456789')
        expected_username = '09123456789'
        self.assertEqual(user.get_username(), expected_username)
