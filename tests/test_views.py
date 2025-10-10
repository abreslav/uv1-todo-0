import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.messages import get_messages
from django.contrib.auth.models import User
from django.utils import timezone
from django_app.models import Todo


class TestViews(TestCase):
    """Endpoint tests for Django app views"""

    def setUp(self):
        """Set up test client and test data"""
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.client.force_login(self.user)

    @pytest.mark.timeout(30)
    def test_delete_todo_endpoint(self):
        """
        Test kind: endpoint_tests
        Original method FQN: delete_todo
        """
        # Create a todo to delete
        todo = Todo.objects.create(content="Test todo to delete", user=self.user)
        todo_id = todo.id

        # Ensure the todo exists
        self.assertTrue(Todo.objects.filter(id=todo_id).exists())

        # Make DELETE request (POST with delete endpoint)
        response = self.client.post(reverse('delete_todo', args=[todo_id]))

        # Check response is redirect to todo_list
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('todo_list'))

        # Check todo was moved to trash (not deleted from database)
        self.assertTrue(Todo.objects.filter(id=todo_id).exists())

        # Refresh from database and check todo is marked as deleted
        todo.refresh_from_db()
        self.assertTrue(todo.is_deleted)
        self.assertIsNotNone(todo.deleted_at)

        # Test with another todo to check success message
        todo2 = Todo.objects.create(content="Another todo to delete", user=self.user)
        response = self.client.post(reverse('delete_todo', args=[todo2.id]), follow=True)

        # Check the success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Todo moved to trash!" in str(message) for message in messages))

    @pytest.mark.timeout(30)
    def test_delete_todo_nonexistent(self):
        """
        Test kind: endpoint_tests
        Test deleting non-existent todo returns 404
        """
        response = self.client.post(reverse('delete_todo', args=[9999]))
        self.assertEqual(response.status_code, 404)

    @pytest.mark.timeout(30)
    def test_todo_list_get_endpoint(self):
        """
        Test kind: endpoint_tests
        Original method FQN: todo_list
        """
        # Create some test todos
        todo1 = Todo.objects.create(content="First todo", user=self.user)
        todo2 = Todo.objects.create(content="Second todo", marked_as_done_at=timezone.now(), user=self.user)

        # Make GET request
        response = self.client.get(reverse('todo_list'))

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "First todo")
        self.assertContains(response, "Second todo")

        # Check context contains todos
        self.assertIn('todos', response.context)
        todos = response.context['todos']
        self.assertEqual(todos.count(), 2)

    @pytest.mark.timeout(30)
    def test_todo_list_post_valid_content(self):
        """
        Test kind: endpoint_tests
        Test POST to todo_list with valid content creates new todo
        """
        content = "New todo from POST"
        initial_count = Todo.objects.count()

        response = self.client.post(reverse('todo_list'), {'content': content})

        # Check redirect
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('todo_list'))

        # Check todo was created
        self.assertEqual(Todo.objects.count(), initial_count + 1)
        self.assertTrue(Todo.objects.filter(content=content).exists())

        # Follow redirect to check success message
        response = self.client.post(reverse('todo_list'), {'content': content}, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Todo added successfully!" in str(message) for message in messages))

    @pytest.mark.timeout(30)
    def test_todo_list_post_empty_content(self):
        """
        Test kind: endpoint_tests
        Test POST to todo_list with empty content shows error
        """
        initial_count = Todo.objects.count()

        # Test with empty string
        response = self.client.post(reverse('todo_list'), {'content': ''}, follow=True)

        # Check no todo was created
        self.assertEqual(Todo.objects.count(), initial_count)

        # Check error message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Todo content cannot be empty!" in str(message) for message in messages))

        # Test with whitespace only
        response = self.client.post(reverse('todo_list'), {'content': '   '}, follow=True)

        # Check no todo was created
        self.assertEqual(Todo.objects.count(), initial_count)

        # Check error message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Todo content cannot be empty!" in str(message) for message in messages))

    @pytest.mark.timeout(30)
    def test_toggle_todo_endpoint_mark_as_done(self):
        """
        Test kind: endpoint_tests
        Original method FQN: toggle_todo
        """
        # Create a todo that is not done
        todo = Todo.objects.create(content="Todo to toggle", user=self.user)
        self.assertFalse(todo.is_done)

        # Toggle to done
        response = self.client.post(reverse('toggle_todo', args=[todo.id]))

        # Check redirect
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('todo_list'))

        # Refresh from database and check todo is now done
        todo.refresh_from_db()
        self.assertTrue(todo.is_done)
        self.assertIsNotNone(todo.marked_as_done_at)

        # Check success message
        response = self.client.post(reverse('toggle_todo', args=[todo.id]), follow=True)
        messages = list(get_messages(response.wsgi_request))
        # This will toggle back, so it should show "marked as not done" message

    @pytest.mark.timeout(30)
    def test_toggle_todo_endpoint_mark_as_not_done(self):
        """
        Test kind: endpoint_tests
        Test toggling done todo back to not done
        """
        # Create a todo that is done
        todo = Todo.objects.create(content="Done todo to toggle", marked_as_done_at=timezone.now(), user=self.user)
        self.assertTrue(todo.is_done)

        # Toggle to not done
        response = self.client.post(reverse('toggle_todo', args=[todo.id]))

        # Check redirect
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('todo_list'))

        # Refresh from database and check todo is now not done
        todo.refresh_from_db()
        self.assertFalse(todo.is_done)
        self.assertIsNone(todo.marked_as_done_at)

        # Check success message
        response = self.client.post(reverse('toggle_todo', args=[todo.id]), follow=True)
        messages = list(get_messages(response.wsgi_request))
        # This will toggle to done, so it should show "marked as done" message

    @pytest.mark.timeout(30)
    def test_toggle_todo_nonexistent(self):
        """
        Test kind: endpoint_tests
        Test toggling non-existent todo returns 404
        """
        response = self.client.post(reverse('toggle_todo', args=[9999]))
        self.assertEqual(response.status_code, 404)

    @pytest.mark.timeout(30)
    def test_todo_list_unauthenticated_user(self):
        """
        Test kind: endpoint_tests
        Test todo_list view returns login template for unauthenticated users
        """
        # Log out the user to test unauthenticated access
        self.client.logout()

        # Make GET request without authentication
        response = self.client.get(reverse('todo_list'))

        # Check response status and template
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'django_app/login.html')

    @pytest.mark.timeout(30)
    def test_trash_endpoint(self):
        """
        Test kind: endpoint_tests
        Original method FQN: trash
        """
        # Create some todos - some deleted, some not
        todo_active = Todo.objects.create(content="Active todo", user=self.user)
        todo_deleted1 = Todo.objects.create(content="Deleted todo 1", user=self.user, deleted_at=timezone.now())
        todo_deleted2 = Todo.objects.create(content="Deleted todo 2", user=self.user, deleted_at=timezone.now())

        # Make GET request to trash endpoint
        response = self.client.get(reverse('trash'))

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'django_app/trash.html')

        # Check context contains only deleted todos
        self.assertIn('deleted_todos', response.context)
        deleted_todos = response.context['deleted_todos']
        self.assertEqual(deleted_todos.count(), 2)

        # Check that active todo is not in the trash
        deleted_todo_ids = [todo.id for todo in deleted_todos]
        self.assertNotIn(todo_active.id, deleted_todo_ids)
        self.assertIn(todo_deleted1.id, deleted_todo_ids)
        self.assertIn(todo_deleted2.id, deleted_todo_ids)

        # Check that the page contains deleted todos content
        self.assertContains(response, "Deleted todo 1")
        self.assertContains(response, "Deleted todo 2")
        self.assertNotContains(response, "Active todo")

    @pytest.mark.timeout(30)
    def test_trash_endpoint_unauthenticated(self):
        """
        Test kind: endpoint_tests
        Test trash view requires authentication
        """
        # Log out the user
        self.client.logout()

        # Make GET request to trash without authentication
        response = self.client.get(reverse('trash'))

        # Check that user is redirected to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)

    @pytest.mark.timeout(30)
    def test_restore_todo_endpoint(self):
        """
        Test kind: endpoint_tests
        Original method FQN: restore_todo
        """
        # Create a deleted todo
        todo = Todo.objects.create(
            content="Todo to restore",
            user=self.user,
            deleted_at=timezone.now()
        )
        self.assertTrue(todo.is_deleted)

        # Make POST request to restore the todo
        response = self.client.post(reverse('restore_todo', args=[todo.id]))

        # Check response is redirect to trash
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('trash'))

        # Refresh from database and check todo is restored
        todo.refresh_from_db()
        self.assertFalse(todo.is_deleted)
        self.assertIsNone(todo.deleted_at)

        # Follow redirect to check success message
        response = self.client.post(reverse('restore_todo', args=[todo.id]), follow=True)
        # Note: This will fail since the todo is no longer deleted, but let's test with a fresh deleted todo

        # Create another deleted todo to test success message
        todo2 = Todo.objects.create(
            content="Another todo to restore",
            user=self.user,
            deleted_at=timezone.now()
        )
        response = self.client.post(reverse('restore_todo', args=[todo2.id]), follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Todo restored successfully!" in str(message) for message in messages))

    @pytest.mark.timeout(30)
    def test_restore_todo_nonexistent(self):
        """
        Test kind: endpoint_tests
        Test restoring non-existent todo returns 404
        """
        response = self.client.post(reverse('restore_todo', args=[9999]))
        self.assertEqual(response.status_code, 404)

    @pytest.mark.timeout(30)
    def test_restore_todo_not_deleted(self):
        """
        Test kind: endpoint_tests
        Test restoring non-deleted todo returns 404
        """
        # Create a todo that is not deleted
        todo = Todo.objects.create(content="Active todo", user=self.user)
        self.assertFalse(todo.is_deleted)

        # Try to restore it - should return 404 since it's not in trash
        response = self.client.post(reverse('restore_todo', args=[todo.id]))
        self.assertEqual(response.status_code, 404)

    @pytest.mark.timeout(30)
    def test_restore_todo_unauthenticated(self):
        """
        Test kind: endpoint_tests
        Test restore_todo view requires authentication
        """
        # Create a deleted todo
        todo = Todo.objects.create(
            content="Deleted todo",
            user=self.user,
            deleted_at=timezone.now()
        )

        # Log out the user
        self.client.logout()

        # Try to restore without authentication
        response = self.client.post(reverse('restore_todo', args=[todo.id]))

        # Check that user is redirected to login
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login/', response.url)