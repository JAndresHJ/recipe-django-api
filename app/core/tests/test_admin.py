from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTests(TestCase):

    # This setup function runs before every test run
    def setUp(self):
        # Create a test client
        self.client = Client()

        # Add a new user that will be used to test
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@test.com',
            password='password123'
        )

        # Login admin user into the client using a helper function
        self.client.force_login(self.admin_user)

        # Create a regular user that is not authenticated
        self.user = get_user_model().objects.create_user(
            email='user@test.com',
            password='password123',
            name='Test user full name'
        )

    def test_users_listed(self):
        """Test that users are listed on user page"""
        url = reverse('admin:core_user_changelist')

        # HTTP GET to the defined URL
        res = self.client.get(url)

        # Assert a 200 status
        # Assert that the response contains a certain item
        self.assertContains(res, self.user.name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""

        # Example URL: /admin/core/user/{id}
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""

        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
