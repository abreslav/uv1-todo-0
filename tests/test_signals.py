import os
import pytest
from django.test import TestCase
from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from unittest.mock import patch, MagicMock, mock_open
from pathlib import Path
from django_app.signals import _read_config_parameter, configure_social_apps


class TestSignalsFunctions(TestCase):
    """Unit tests for signals module functions"""

    @pytest.mark.timeout(30)
    def test_read_config_parameter_from_env_local_file(self):
        """
        Test kind: unit_tests
        Original method FQN: _read_config_parameter
        """
        # Test reading from .env.local file
        mock_env_content = "TEST_PARAM=value_from_file\nANOTHER_PARAM=another_value"

        with patch('pathlib.Path.exists', return_value=True), \
             patch('django_app.signals.dotenv_values', return_value={'TEST_PARAM': 'value_from_file'}), \
             patch('os.getenv', return_value=None):

            result = _read_config_parameter('test_param')
            self.assertEqual(result, 'value_from_file')

    @pytest.mark.timeout(30)
    def test_read_config_parameter_from_environment_variables(self):
        """
        Test kind: unit_tests
        Original method FQN: _read_config_parameter
        """
        # Test reading from environment variables when .env.local doesn't exist
        with patch('pathlib.Path.exists', return_value=False), \
             patch('os.getenv', return_value='value_from_env'):

            result = _read_config_parameter('test_param')
            self.assertEqual(result, 'value_from_env')

    @pytest.mark.timeout(30)
    def test_read_config_parameter_env_local_takes_precedence(self):
        """
        Test kind: unit_tests
        Original method FQN: _read_config_parameter
        """
        # Test that .env.local takes precedence over environment variables
        with patch('pathlib.Path.exists', return_value=True), \
             patch('django_app.signals.dotenv_values', return_value={'TEST_PARAM': 'from_file'}), \
             patch('os.getenv', return_value='from_env'):

            result = _read_config_parameter('test_param')
            self.assertEqual(result, 'from_file')

    @pytest.mark.timeout(30)
    def test_read_config_parameter_fallback_to_env_when_not_in_file(self):
        """
        Test kind: unit_tests
        Original method FQN: _read_config_parameter
        """
        # Test fallback to environment variable when parameter is not in .env.local
        with patch('pathlib.Path.exists', return_value=True), \
             patch('django_app.signals.dotenv_values', return_value={'OTHER_PARAM': 'other_value'}), \
             patch('os.getenv', return_value='from_env'):

            result = _read_config_parameter('test_param')
            self.assertEqual(result, 'from_env')

    @pytest.mark.timeout(30)
    def test_read_config_parameter_case_insensitive(self):
        """
        Test kind: unit_tests
        Original method FQN: _read_config_parameter
        """
        # Test case insensitive parameter name handling
        with patch('pathlib.Path.exists', return_value=True), \
             patch('django_app.signals.dotenv_values', return_value={'TEST_PARAM': 'value_from_file'}), \
             patch('os.getenv') as mock_getenv:
            mock_getenv.side_effect = lambda param: 'value_from_env' if param == 'TEST_PARAM' else None

            # Test lowercase input
            result = _read_config_parameter('test_param')
            self.assertEqual(result, 'value_from_file')

            # Test uppercase input
            result = _read_config_parameter('TEST_PARAM')
            self.assertEqual(result, 'value_from_file')

            # Test mixed case input
            result = _read_config_parameter('Test_Param')
            self.assertEqual(result, 'value_from_file')

    @pytest.mark.timeout(30)
    def test_read_config_parameter_returns_none_when_not_found(self):
        """
        Test kind: unit_tests
        Original method FQN: _read_config_parameter
        """
        # Test returns None when parameter is not found anywhere
        with patch('pathlib.Path.exists', return_value=False), \
             patch('os.getenv', return_value=None):

            result = _read_config_parameter('nonexistent_param')
            self.assertIsNone(result)

    @pytest.mark.timeout(30)
    def test_configure_social_apps_wrong_sender(self):
        """
        Test kind: unit_tests
        Original method FQN: configure_social_apps
        """
        # Test that function returns early when sender is not django_app
        mock_sender = MagicMock()
        mock_sender.name = 'other_app'

        with patch('django.contrib.sites.models.Site.objects.get_or_create') as mock_site:
            configure_social_apps(sender=mock_sender)

            # Site.objects.get_or_create should not be called
            mock_site.assert_not_called()

    @pytest.mark.timeout(30)
    def test_configure_social_apps_creates_site(self):
        """
        Test kind: unit_tests
        Original method FQN: configure_social_apps
        """
        # Test that function creates/gets site correctly
        mock_sender = MagicMock()
        mock_sender.name = 'django_app'
        mock_site = MagicMock()

        with patch('django.contrib.sites.models.Site.objects.get_or_create', return_value=(mock_site, True)) as mock_site_create, \
             patch('os.getenv', return_value='1'), \
             patch('django_app.signals.SOCIAL_LOGIN_PROVIDERS', {}), \
             patch('builtins.print'):

            configure_social_apps(sender=mock_sender)

            # Verify site creation was called with correct parameters
            mock_site_create.assert_called_once_with(
                id='1',
                defaults={"domain": "localhost:8000", "name": "Todoer"}
            )

    @pytest.mark.timeout(30)
    def test_configure_social_apps_skips_missing_credentials(self):
        """
        Test kind: unit_tests
        Original method FQN: configure_social_apps
        """
        # Test that function skips providers with missing credentials
        mock_sender = MagicMock()
        mock_sender.name = 'django_app'
        mock_site = MagicMock()

        mock_providers = {
            'google': {
                'name': 'Google',
                'client_id': None,
                'client_secret': 'secret123'
            }
        }

        with patch('django.contrib.sites.models.Site.objects.get_or_create', return_value=(mock_site, True)), \
             patch('django_app.signals.SOCIAL_LOGIN_PROVIDERS', mock_providers), \
             patch('allauth.socialaccount.models.SocialApp.objects.get_or_create') as mock_social_create, \
             patch('builtins.print') as mock_print:

            configure_social_apps(sender=mock_sender)

            # SocialApp creation should not be called
            mock_social_create.assert_not_called()

            # Should print skip message
            mock_print.assert_any_call("Skipping Google - credentials not provided")

    @pytest.mark.timeout(30)
    def test_configure_social_apps_skips_placeholder_credentials(self):
        """
        Test kind: unit_tests
        Original method FQN: configure_social_apps
        """
        # Test that function skips providers with placeholder credentials
        mock_sender = MagicMock()
        mock_sender.name = 'django_app'
        mock_site = MagicMock()

        mock_providers = {
            'google': {
                'name': 'Google',
                'client_id': 'your_client_id',
                'client_secret': 'your_secret'
            }
        }

        with patch('django.contrib.sites.models.Site.objects.get_or_create', return_value=(mock_site, True)), \
             patch('django_app.signals.SOCIAL_LOGIN_PROVIDERS', mock_providers), \
             patch('allauth.socialaccount.models.SocialApp.objects.get_or_create') as mock_social_create, \
             patch('builtins.print') as mock_print:

            configure_social_apps(sender=mock_sender)

            # SocialApp creation should not be called
            mock_social_create.assert_not_called()

            # Should print skip message
            mock_print.assert_any_call("Skipping Google - placeholder credentials detected")

    @pytest.mark.timeout(30)
    def test_configure_social_apps_creates_new_social_app(self):
        """
        Test kind: unit_tests
        Original method FQN: configure_social_apps
        """
        # Test creating a new social app
        mock_sender = MagicMock()
        mock_sender.name = 'django_app'
        mock_site = MagicMock()
        mock_social_app = MagicMock()

        mock_providers = {
            'google': {
                'name': 'Google',
                'client_id': 'real_client_id',
                'client_secret': 'real_secret'
            }
        }

        with patch('django.contrib.sites.models.Site.objects.get_or_create', return_value=(mock_site, True)), \
             patch('django_app.signals.SOCIAL_LOGIN_PROVIDERS', mock_providers), \
             patch('allauth.socialaccount.models.SocialApp.objects.get_or_create', return_value=(mock_social_app, True)) as mock_social_create, \
             patch('builtins.print') as mock_print:

            configure_social_apps(sender=mock_sender)

            # Verify SocialApp creation was called with correct parameters
            mock_social_create.assert_called_once_with(
                provider='google',
                defaults={
                    'name': 'Google',
                    'client_id': 'real_client_id',
                    'secret': 'real_secret'
                }
            )

            # Verify site was added to social app
            mock_social_app.sites.add.assert_called_once_with(mock_site)

            # Verify success message
            mock_print.assert_any_call("Created Google SocialApp")

    @pytest.mark.timeout(30)
    def test_configure_social_apps_updates_existing_social_app(self):
        """
        Test kind: unit_tests
        Original method FQN: configure_social_apps
        """
        # Test updating an existing social app
        mock_sender = MagicMock()
        mock_sender.name = 'django_app'
        mock_site = MagicMock()
        mock_social_app = MagicMock()

        mock_providers = {
            'google': {
                'name': 'Google Updated',
                'client_id': 'updated_client_id',
                'client_secret': 'updated_secret'
            }
        }

        with patch('django.contrib.sites.models.Site.objects.get_or_create', return_value=(mock_site, True)), \
             patch('django_app.signals.SOCIAL_LOGIN_PROVIDERS', mock_providers), \
             patch('allauth.socialaccount.models.SocialApp.objects.get_or_create', return_value=(mock_social_app, False)) as mock_social_create, \
             patch('builtins.print') as mock_print:

            configure_social_apps(sender=mock_sender)

            # Verify SocialApp get_or_create was called
            mock_social_create.assert_called_once()

            # Verify social app was updated
            self.assertEqual(mock_social_app.name, 'Google Updated')
            self.assertEqual(mock_social_app.client_id, 'updated_client_id')
            self.assertEqual(mock_social_app.secret, 'updated_secret')
            mock_social_app.save.assert_called_once()

            # Verify site was added to social app
            mock_social_app.sites.add.assert_called_once_with(mock_site)

            # Verify success message
            mock_print.assert_any_call("Updated Google Updated SocialApp")