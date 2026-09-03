"""
Unit tests for exceptions.
"""

import pytest
from telegram_listener.exceptions import (
    TelegramListenerError,
    ConnectionError,
    RegistrationError,
    TimeoutError,
    InvalidConfigError,
)


class TestExceptions:
    """Test exception hierarchy."""

    def test_base_exception(self):
        """Test TelegramListenerError is base."""
        exc = TelegramListenerError("Test error")
        assert isinstance(exc, Exception)

    def test_connection_error_inheritance(self):
        """Test ConnectionError inherits from base."""
        exc = ConnectionError("Connection failed")
        assert isinstance(exc, TelegramListenerError)
        assert isinstance(exc, Exception)

    def test_registration_error_inheritance(self):
        """Test RegistrationError inherits from base."""
        exc = RegistrationError("Registration failed")
        assert isinstance(exc, TelegramListenerError)
        assert isinstance(exc, Exception)

    def test_timeout_error_inheritance(self):
        """Test TimeoutError inherits from base."""
        exc = TimeoutError("Operation timed out")
        assert isinstance(exc, TelegramListenerError)
        assert isinstance(exc, Exception)

    def test_invalid_config_error_inheritance(self):
        """Test InvalidConfigError inherits from base."""
        exc = InvalidConfigError("Invalid config")
        assert isinstance(exc, TelegramListenerError)
        assert isinstance(exc, Exception)

    def test_exception_message(self):
        """Test exception message is preserved."""
        msg = "Test error message"
        exc = TelegramListenerError(msg)
        assert str(exc) == msg
