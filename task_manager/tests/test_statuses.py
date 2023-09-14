from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User
from task_manager.statuses.models import Status


class StatusCRUDTest(TestCase):

    def setUp(self):
        self.status1 = Status.objects.create(name='new')
        self.status2 = Status.objects.create(name='in work')
        self.status3 = Status.objects.create(name='in testing')
        self.status4 = Status.objects.create(name='finished')
        self.user = User.objects.create(
            first_name='Bruce',
            last_name='Lee',
            username='BruLee',
            password='kiaaa'
        )

    # CREATE

    def test_create_status(self):

        # unauthenticated user

        unauth_response = self.client.post(
            reverse('statuses_create'), {'name': 'test_status'})
        self.assertEqual(unauth_response.status_code, 302)
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(name='test_status')

        # authenticated user

        self.client.force_login(self.user)
        auth_response = self.client.post(
            reverse('statuses_create'), {'name': 'test_status'})
        self.assertEqual(auth_response.status_code, 302)
        self.assertRedirects(auth_response, reverse('statuses_list'))
        new_status = Status.objects.get(name='test_status')
        self.assertEqual(new_status.name, 'test_status')

    # UPDATE

    def test_update_status(self):

        # unauthenticated user

        unauth_response = self.client.post(
            reverse('statuses_update', kwargs={'pk': self.status2.id}),
            {'name': 'in progress'}
        )
        self.assertEqual(unauth_response.status_code, 302)
        self.assertEqual(self.status2.name, 'in work')
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(name='in progress')

        # authenticated user

        self.client.force_login(self.user)
        auth_response = self.client.post(
            reverse('statuses_update', kwargs={'pk': self.status2.id}),
            {'name': 'in progress'}
        )
        self.assertEqual(auth_response.status_code, 302)
        self.assertRedirects(auth_response, reverse('statuses_list'))
        updated_status = Status.objects.get(id=self.status2.id)
        self.assertEqual(updated_status.name, 'in progress')

    # DELETE

    def test_delete_status(self):

        # unauthenticated user

        unauth_response = self.client.post(
            reverse('statuses_delete', kwargs={'pk': self.status3.id})
        )
        self.assertEqual(unauth_response.status_code, 302)
        self.assertEqual(self.status3.name, 'in testing')

        # authenticated user

        self.client.force_login(self.user)
        auth_response = self.client.post(
            reverse('statuses_delete', kwargs={'pk': self.status3.id})
        )
        self.assertEqual(auth_response.status_code, 302)
        self.assertRedirects(auth_response, reverse('statuses_list'))
        with self.assertRaises(Status.DoesNotExist):
            Status.objects.get(id=self.status3.id)
