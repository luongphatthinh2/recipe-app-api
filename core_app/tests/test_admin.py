from django.test import TestCase,Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email = 'thinh_superuser@gmail.com',
            password = '123456789',
        )
        self.client.force_login(self.admin_user)

        self.user = get_user_model().objects.create_user(
            email = 'thinh_user@gmail.com',
            password = '123456789',
            name = 'Test user full name',
        )

    def test_users_listed(self):
        """ Test that users are listed on user page at admin site """
        url = reverse('admin:core_app_user_changelist')
        response = self.client.get(url)
        self.assertContains(response,self.user.name)
        self.assertContains(response,self.user.email)

    def test_user_change_page(self):
        """Test that user edit page works"""
        url = reverse('admin:core_app_user_change', args=[self.user.id])
        # url : /admin/core_app/user/1
        response = self.client.get(url)
        self.assertEqual(response.status_code,200)

    def test_user_create_page(self):
        """ Test that the create user page works  """
        url = reverse('admin:core_app_user_add')
        response= self.client.get(url) # client will make a HTTP GET to this url

        self.assertEqual(response.status_code,200)
