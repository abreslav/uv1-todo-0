"""
Tests for authentication and social account functionality.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount, SocialApp
from django.contrib.sites.models import Site


class SocialAuthTest(TestCase):
    """Test social authentication functionality."""

    def setUp(self):
        """Set up test data."""
        self.site = Site.objects.get(pk=1)

        # Create a Google SocialApp for testing
        self.google_app = SocialApp.objects.create(
            provider='google',
            name='Google Test',
            client_id='test_client_id',
            secret='test_secret'
        )
        self.google_app.sites.add(self.site)

    def test_username_uniqueness(self):
        """Test that our custom adapter generates unique usernames."""
        from django_app.adapters import CustomSocialAccountAdapter

        adapter = CustomSocialAccountAdapter()

        # Generate multiple usernames
        username1 = adapter.generate_unique_username([])
        username2 = adapter.generate_unique_username([])
        username3 = adapter.generate_unique_username([])

        # Verify they're all different
        usernames = [username1, username2, username3]
        self.assertEqual(len(set(usernames)), 3, "All usernames should be unique")

        # Verify format
        for username in usernames:
            self.assertTrue(username.startswith('user_'))
            self.assertEqual(len(username), 13)  # "user_" + 8 hex chars

    def test_adapter_creates_users_with_unique_usernames(self):
        """Test that the adapter can create multiple users without username conflicts."""
        from django_app.adapters import CustomSocialAccountAdapter

        adapter = CustomSocialAccountAdapter()

        # Create first user
        user1 = User()
        user1.email = 'user1@example.com'
        user1.username = adapter.generate_unique_username([])
        user1.save()

        # Create social account for first user
        social_account1 = SocialAccount.objects.create(
            user=user1,
            provider='google',
            uid='12345',
            extra_data={'email': 'user1@example.com'}
        )

        # Create second user - this should not fail due to username conflicts
        user2 = User()
        user2.email = 'user2@example.com'
        user2.username = adapter.generate_unique_username([])
        user2.save()

        # Create social account for second user
        social_account2 = SocialAccount.objects.create(
            user=user2,
            provider='google',
            uid='67890',
            extra_data={'email': 'user2@example.com'}
        )

        # Verify both users exist and have different usernames
        self.assertNotEqual(user1.username, user2.username)
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(SocialAccount.objects.count(), 2)