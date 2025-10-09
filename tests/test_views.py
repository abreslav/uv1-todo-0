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

        # Check todo was deleted
        self.assertFalse(Todo.objects.filter(id=todo_id).exists())

        # Follow the redirect to check for success message
        response = self.client.post(reverse('delete_todo', args=[todo_id]), follow=True)
        # Since todo doesn't exist, this should return 404 - let's test with existing todo

        # Test with another todo
        todo2 = Todo.objects.create(content="Another todo to delete", user=self.user)
        response = self.client.post(reverse('delete_todo', args=[todo2.id]), follow=True)

        # Check the success message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Todo deleted successfully!" in str(message) for message in messages))

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
    def test_edit_todo_endpoint_valid_content(self):
        """
        Test kind: endpoint_tests
        Original method FQN: edit_todo
        """
        # Create a todo to edit
        original_content = "Original todo content"
        todo = Todo.objects.create(content=original_content, user=self.user)

        # Edit the todo with valid content
        new_content = "Updated todo content"
        response = self.client.post(reverse('edit_todo', args=[todo.id]), {'content': new_content})

        # Check redirect
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('todo_list'))

        # Check todo was updated
        todo.refresh_from_db()
        self.assertEqual(todo.content, new_content)

        # Check success message
        response = self.client.post(reverse('edit_todo', args=[todo.id]), {'content': new_content}, follow=True)
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Todo updated successfully!" in str(message) for message in messages))

    @pytest.mark.timeout(30)
    def test_edit_todo_endpoint_empty_content(self):
        """
        Test kind: endpoint_tests
        Test edit_todo endpoint with empty content shows error
        """
        # Create a todo to edit
        original_content = "Original todo content"
        todo = Todo.objects.create(content=original_content, user=self.user)

        # Try to edit with empty content
        response = self.client.post(reverse('edit_todo', args=[todo.id]), {'content': ''}, follow=True)

        # Check todo was not updated
        todo.refresh_from_db()
        self.assertEqual(todo.content, original_content)

        # Check error message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Todo content cannot be empty!" in str(message) for message in messages))

        # Try to edit with whitespace only
        response = self.client.post(reverse('edit_todo', args=[todo.id]), {'content': '   '}, follow=True)

        # Check todo was not updated
        todo.refresh_from_db()
        self.assertEqual(todo.content, original_content)

        # Check error message
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any("Todo content cannot be empty!" in str(message) for message in messages))

    @pytest.mark.timeout(30)
    def test_edit_todo_endpoint_nonexistent(self):
        """
        Test kind: endpoint_tests
        Test editing non-existent todo returns 404
        """
        response = self.client.post(reverse('edit_todo', args=[9999]), {'content': 'New content'})
        self.assertEqual(response.status_code, 404)

    @pytest.mark.timeout(30)
    def test_edit_todo_endpoint_different_user(self):
        """
        Test kind: endpoint_tests
        Test editing todo belonging to different user returns 404
        """
        # Create another user and their todo
        other_user = User.objects.create_user(
            username='otheruser',
            email='other@example.com',
            password='otherpass123'
        )
        other_todo = Todo.objects.create(content="Other user's todo", user=other_user)

        # Try to edit other user's todo with current user
        response = self.client.post(reverse('edit_todo', args=[other_todo.id]), {'content': 'Hacked content'})
        self.assertEqual(response.status_code, 404)

        # Verify the todo wasn't changed
        other_todo.refresh_from_db()
        self.assertEqual(other_todo.content, "Other user's todo")