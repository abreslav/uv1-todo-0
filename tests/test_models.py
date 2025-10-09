import pytest
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth.models import User
from django_app.models import Todo


class TestTodo(TestCase):
    """Unit tests for Todo model"""

    def setUp(self):
        """Set up test user for Todo model tests"""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    @pytest.mark.timeout(30)
    def test_todo_str_method(self):
        """
        Test kind: unit_tests
        Original method FQN: Todo.__str__
        """
        # Test with short content (less than 50 chars)
        short_content = "Buy milk"
        todo = Todo.objects.create(content=short_content, user=self.user)
        expected = f"{short_content}..."
        self.assertEqual(str(todo), expected)

        # Test with long content (more than 50 chars)
        long_content = "This is a very long todo item that has more than fifty characters in it"
        todo_long = Todo.objects.create(content=long_content, user=self.user)
        expected_long = f"{long_content[:50]}..."
        self.assertEqual(str(todo_long), expected_long)

        # Test with exactly 50 characters
        exactly_50_content = "12345678901234567890123456789012345678901234567890"  # exactly 50 chars
        todo_50 = Todo.objects.create(content=exactly_50_content, user=self.user)
        expected_50 = f"{exactly_50_content[:50]}..."
        self.assertEqual(str(todo_50), expected_50)

    @pytest.mark.timeout(30)
    def test_todo_is_done_property(self):
        """
        Test kind: unit_tests
        Original method FQN: Todo.is_done
        """
        # Test todo that is not done (marked_as_done_at is None)
        todo_not_done = Todo.objects.create(content="Test todo not done", user=self.user)
        self.assertFalse(todo_not_done.is_done)

        # Test todo that is done (marked_as_done_at is set)
        todo_done = Todo.objects.create(content="Test todo done", marked_as_done_at=timezone.now(), user=self.user)
        self.assertTrue(todo_done.is_done)

        # Test todo that becomes done
        todo_becomes_done = Todo.objects.create(content="Test todo becomes done", user=self.user)
        self.assertFalse(todo_becomes_done.is_done)

        todo_becomes_done.marked_as_done_at = timezone.now()
        todo_becomes_done.save()
        self.assertTrue(todo_becomes_done.is_done)

        # Test todo that becomes not done again
        todo_becomes_done.marked_as_done_at = None
        todo_becomes_done.save()
        self.assertFalse(todo_becomes_done.is_done)

    @pytest.mark.timeout(30)
    def test_todo_content_html_property(self):
        """
        Test kind: unit_tests
        Original method FQN: Todo.content_html
        """
        # Test basic markdown conversion
        content = "This is **bold** and *italic* text"
        todo = Todo.objects.create(content=content, user=self.user)
        html_output = todo.content_html

        # Check that markdown is converted to HTML
        self.assertIn('<strong>bold</strong>', html_output)
        self.assertIn('<em>italic</em>', html_output)

        # Test newline to br conversion (nl2br extension)
        content_with_newlines = "Line 1\nLine 2\nLine 3"
        todo_newlines = Todo.objects.create(content=content_with_newlines, user=self.user)
        html_with_br = todo_newlines.content_html

        # Check that newlines are converted to <br> tags
        self.assertIn('<br', html_with_br)

        # Test fenced code blocks
        content_with_code = "```python\nprint('hello world')\n```"
        todo_code = Todo.objects.create(content=content_with_code, user=self.user)
        html_with_code = todo_code.content_html

        # Check that code blocks are converted properly
        self.assertIn('<code>', html_with_code)
        self.assertIn('print(', html_with_code)

        # Test plain text (no markdown)
        plain_content = "Just plain text with no markdown"
        todo_plain = Todo.objects.create(content=plain_content, user=self.user)
        plain_html = todo_plain.content_html

        # Plain text should be wrapped in <p> tags by markdown
        self.assertIn('<p>', plain_html)
        self.assertIn(plain_content, plain_html)

        # Test empty content
        empty_todo = Todo.objects.create(content="", user=self.user)
        empty_html = empty_todo.content_html

        # Empty content should still return valid HTML (empty or minimal tags)
        self.assertIsNotNone(empty_html)