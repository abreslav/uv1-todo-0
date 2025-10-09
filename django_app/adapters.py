"""
Custom Django AllAuth adapters for handling social account signup.
"""
import uuid
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.contrib.auth.models import User


class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    """
    Custom adapter to handle username generation for social accounts.

    Since Django's User model requires a unique username but we're using
    email-based authentication, we need to generate unique usernames
    automatically.
    """

    def generate_unique_username(self, txts, regex=None):
        """
        Generate a unique username using UUID to avoid conflicts.
        """
        # Use a UUID-based username to ensure uniqueness
        base_username = f"user_{uuid.uuid4().hex[:8]}"

        # Ensure it's unique (though UUID collision is extremely unlikely)
        counter = 0
        username = base_username
        while User.objects.filter(username=username).exists():
            counter += 1
            username = f"{base_username}_{counter}"

        return username

    def populate_user(self, request, sociallogin, data):
        """
        Populate user data from social account information.
        """
        user = super().populate_user(request, sociallogin, data)

        # Ensure we have an email
        if not user.email and sociallogin.account.extra_data:
            # Try to get email from social account data
            user.email = sociallogin.account.extra_data.get('email', '')

        return user