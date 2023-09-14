from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User
from task_manager.labels.models import Label


class LabelsCRUDTest(TestCase):

    def setUp(self):
        self.user = User.objects.create(
            first_name='Bruce',
            last_name='Lee',
            username='BruLee',
            password='kiaaa'
        )
        self.label = Label.objects.create(
            name='new_label'
        )

    # CREATE

    def test_create_label(self):

        # unauthenticated user

        unauth_response = self.client.post(
            reverse('labels_create'), {'name': 'test_label'})
        self.assertEqual(unauth_response.status_code, 302)
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(name='test_label')

        # authenticated user

        self.client.force_login(self.user)
        auth_response = self.client.post(
            reverse('labels_create'), {'name': 'test_label'})
        self.assertEqual(auth_response.status_code, 302)
        self.assertRedirects(auth_response, reverse('labels_list'))
        test_label = Label.objects.get(name='test_label')
        self.assertEqual(test_label.name, 'test_label')

    # UPDATE

    def test_update_label(self):

        # unauthenticated user

        unauth_response = self.client.post(
            reverse('labels_update', kwargs={'pk': self.label.id}),
            {'name': 'updated label'}
        )
        self.assertEqual(unauth_response.status_code, 302)
        not_updated_label = Label.objects.get(id=self.label.id)
        self.assertEqual(not_updated_label.name, 'new_label')
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(name='updated label')

        # authenticated user

        self.client.force_login(self.user)
        auth_response = self.client.post(
            reverse('labels_update', kwargs={'pk': self.label.id}),
            {'name': 'updated label'}
        )
        self.assertEqual(auth_response.status_code, 302)
        self.assertRedirects(auth_response, reverse('labels_list'))
        updated_label = Label.objects.get(id=self.label.id)
        self.assertEqual(updated_label.name, 'updated label')

    # DELETE

    def test_delete_label(self):

        # unauthenticated user

        unauth_response = self.client.post(
            reverse('labels_delete', kwargs={'pk': self.label.id})
        )
        self.assertEqual(unauth_response.status_code, 302)
        not_deleted_label = Label.objects.get(id=self.label.id)
        self.assertEqual(not_deleted_label.name, 'new_label')

        # authenticated user

        self.client.force_login(self.user)
        auth_response = self.client.post(
            reverse('labels_delete', kwargs={'pk': self.label.id})
        )
        self.assertEqual(auth_response.status_code, 302)
        self.assertRedirects(auth_response, reverse('labels_list'))
        with self.assertRaises(Label.DoesNotExist):
            Label.objects.get(id=self.label.id)
