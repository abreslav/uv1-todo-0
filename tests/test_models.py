import pytest
from django.test import TestCase
from django.utils import timezone
from django_app.models import Todo


class TestTodo(TestCase):
    """Unit tests for Todo model"""

    @pytest.mark.timeout(30)
    def test_todo_str_method(self):
        """
        Test kind: unit_tests
        Original method FQN: Todo.__str__
        """
        # Test with short content (less than 50 chars)
        short_content = "Buy milk"
        todo = Todo.objects.create(content=short_content)
        expected = f"{short_content}..."
        self.assertEqual(str(todo), expected)

        # Test with long content (more than 50 chars)
        long_content = "This is a very long todo item that has more than fifty characters in it"
        todo_long = Todo.objects.create(content=long_content)
        expected_long = f"{long_content[:50]}..."
        self.assertEqual(str(todo_long), expected_long)

        # Test with exactly 50 characters
        exactly_50_content = "12345678901234567890123456789012345678901234567890"  # exactly 50 chars
        todo_50 = Todo.objects.create(content=exactly_50_content)
        expected_50 = f"{exactly_50_content[:50]}..."
        self.assertEqual(str(todo_50), expected_50)

    @pytest.mark.timeout(30)
    def test_todo_is_done_property(self):
        """
        Test kind: unit_tests
        Original method FQN: Todo.is_done
        """
        # Test todo that is not done (marked_as_done_at is None)
        todo_not_done = Todo.objects.create(content="Test todo not done")
        self.assertFalse(todo_not_done.is_done)

        # Test todo that is done (marked_as_done_at is set)
        todo_done = Todo.objects.create(content="Test todo done", marked_as_done_at=timezone.now())
        self.assertTrue(todo_done.is_done)

        # Test todo that becomes done
        todo_becomes_done = Todo.objects.create(content="Test todo becomes done")
        self.assertFalse(todo_becomes_done.is_done)

        todo_becomes_done.marked_as_done_at = timezone.now()
        todo_becomes_done.save()
        self.assertTrue(todo_becomes_done.is_done)

        # Test todo that becomes not done again
        todo_becomes_done.marked_as_done_at = None
        todo_becomes_done.save()
        self.assertFalse(todo_becomes_done.is_done)