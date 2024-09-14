from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserModelTest(TestCase):
    def test_create_user(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            nickname='testnick',
            name='Test User',
            phone_number='01012345678'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('testpassword123'))
        self.assertEqual(user.nickname, 'testnick')
        self.assertEqual(user.name, 'Test User')
        self.assertEqual(user.phone_number, '01012345678')
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_admin)
        self.assertTrue(user.is_active)

    def test_create_superuser(self):
        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword123',
            nickname='adminnick',
            name='Admin User',
            phone_number='01087654321'
        )
        self.assertEqual(admin_user.email, 'admin@example.com')
        self.assertTrue(admin_user.check_password('adminpassword123'))
        self.assertEqual(admin_user.nickname, 'adminnick')
        self.assertEqual(admin_user.name, 'Admin User')
        self.assertEqual(admin_user.phone_number, '01087654321')
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_admin)
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_superuser)



    def test_create_user_without_email(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='',
                password='testpassword123',
                nickname='testnick',
                name='Test User',
                phone_number='01012345678'
            )

    def test_create_user_without_nickname_or_name(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='test@example.com',
                password='testpassword123',
                nickname='',
                name='Test User',
                phone_number='01012345678'
            )
        with self.assertRaises(ValueError):
            User.objects.create_user(
                email='test@example.com',
                password='testpassword123',
                nickname='testnick',
                name='',
                phone_number='01012345678'
            )

    def test_create_superuser_without_required_fields(self):
        with self.assertRaises(ValidationError):
            User.objects.create_superuser(
                email='admin@example.com',
                password='adminpassword123',
                nickname='adminnick',
                name='Admin User'
            )

    def test_user_str_method(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            nickname='testnick',
            name='Test User',
            phone_number='01012345678'
        )
        self.assertEqual(str(user), 'test@example.com')

    def test_user_permissions(self):
        user = User.objects.create_user(
            email='test@example.com',
            password='testpassword123',
            nickname='testnick',
            name='Test User',
            phone_number='01012345678'
        )
        self.assertFalse(user.has_perm('some_app.some_permission'))
        self.assertFalse(user.has_module_perms('some_app'))

        admin_user = User.objects.create_superuser(
            email='admin@example.com',
            password='adminpassword123',
            nickname='adminnick',
            name='Admin User',
            phone_number='01087654321'
        )
        self.assertTrue(admin_user.has_perm('some_app.some_permission'))
        self.assertTrue(admin_user.has_module_perms('some_app'))