from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User


class UsersCRUDTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            first_name='Bruce',
            last_name='Lee',
            username='BruLee',
            password='kiaaa'
        )

        self.other_user = User.objects.create(
            first_name='Chuck',
            last_name='Norris',
            username='ChuNor',
            password='dong'
        )

    # CREATE

    def test_create_user(self):
        response = self.client.post(
            reverse('users_create'),
            {
                'first_name': 'Testuser',
                'last_name': 'Usertest',
                'username': 'TUS',
                'password1': 'tester',
                'password2': 'tester'
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        new_user = User.objects.get(username='TUS')
        self.assertEqual(new_user.first_name, 'Testuser')

    # UPDATE

    def test_update_unauthenticated_user(self):
        response = self.client.post(
            reverse('users_update', kwargs={'pk': self.user.id}),
            {
                'first_name': 'Vasya'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_update_other_user(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users_update', kwargs={'pk': self.other_user.id}),
            {
                'first_name': 'Ivan'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(self.other_user.first_name, 'Chuck')

    def test_update_own_user(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users_update', kwargs={'pk': self.user.id}),
            {
                'first_name': 'John',
                'last_name': 'Smith',
                'username': 'JSmith',
                'password1': 'kukareku',
                'password2': 'kukareku'
            }
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        updated_user = User.objects.get(id=self.user.id)
        self.assertEqual(updated_user.username, 'JSmith')
        self.assertEqual(updated_user.first_name, 'John')

    # DELETE

    def test_delete_unauthenticated_user(self):
        response = self.client.post(
            reverse('users_delete', kwargs={'pk': self.user.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))

    def test_delete_other_user(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users_delete', kwargs={'pk': self.other_user.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        self.assertEqual(self.other_user.first_name, 'Chuck')

    def test_delete_own_user(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('users_delete', kwargs={'pk': self.user.id})
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('users_list'))
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(id=self.user.id)
