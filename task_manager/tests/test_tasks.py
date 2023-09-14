from django.test import TestCase
from django.urls import reverse
from task_manager.users.models import User
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TasksCRUDTest(TestCase):

    def setUp(self):
        self.user1 = User.objects.create(
            first_name='Bruce',
            last_name='Lee',
            username='BruLee',
            password='kiaaa'
        )
        self.user2 = User.objects.create(
            first_name='Chuck',
            last_name='Norris',
            username='ChuNor',
            password='dong'
        )
        self.status = Status.objects.create(
            name='Fight!'
        )
        self.task = Task.objects.create(
            name='test task',
            description='test task for Bruce Lee',
            author=self.user1,
            executor=self.user1,
            status=self.status
        )

    # CREATE

    def test_create_task(self):

        new_task = {
            'name': 'new task',
            'description': 'new task for Bruce',
            'author': 1,
            'status': 1
        }

        # unauthenticated user

        unauth_response = self.client.post(
            reverse('tasks_create'), new_task)
        self.assertEqual(unauth_response.status_code, 302)
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(name='new task')

        # authenticated user

        self.client.force_login(self.user1)
        auth_response = self.client.post(
            reverse('tasks_create'), new_task)
        self.assertEqual(auth_response.status_code, 302)
        self.assertRedirects(auth_response, reverse('tasks_list'))
        new_task_in_bd = Task.objects.get(id=2)
        self.assertEqual(new_task_in_bd.name, 'new task')

    # UPDATE

    def test_update_task(self):

        # unauthenticated user

        unauth_response = self.client.post(
            reverse('tasks_update', kwargs={'pk': self.task.id}),
            {'name': 'task for Bruce'}
        )
        self.assertEqual(unauth_response.status_code, 302)
        self.assertEqual(self.task.name, 'test task')
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(name='task for Bruce')

        # authenticated user

        self.client.force_login(self.user2)
        auth_response = self.client.post(
            reverse('tasks_update', kwargs={'pk': self.task.id}),
            {
                'name': 'task for Chuck',
                'description': 'task for Chuck',
                'author': 1,
                'executor': 2,
                'status': 1,
            }
        )
        self.assertEqual(auth_response.status_code, 302)
        self.assertRedirects(auth_response, reverse('tasks_list'))
        updated_task = Task.objects.get(id=self.task.id)
        self.assertEqual(updated_task.name, 'task for Chuck')

    # DELETE

    def test_delete_task(self):

        # unauthenticated user

        unauth_response = self.client.post(
            reverse('tasks_delete', kwargs={'pk': self.task.id})
        )
        self.assertEqual(unauth_response.status_code, 302)
        test_task = Task.objects.get(id=self.task.id)
        self.assertEqual(self.task.name, test_task.name)

        # authenticated user - owner

        self.client.force_login(self.user1)
        auth_response = self.client.post(
            reverse('tasks_delete', kwargs={'pk': self.task.id})
        )
        self.assertEqual(auth_response.status_code, 302)
        self.assertRedirects(auth_response, reverse('tasks_list'))
        with self.assertRaises(Task.DoesNotExist):
            Task.objects.get(id=self.task.id)
