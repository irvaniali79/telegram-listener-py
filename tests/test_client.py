"""
Unit tests for ChatListener client.
"""

import pytest
import json
import socket
from unittest.mock import Mock, patch, MagicMock
from telegram_listener.client import ChatListener
from telegram_listener.events import MessageEvent, MediaInfo
from telegram_listener.exceptions import (
    InvalidConfigError,
    ConnectionError as TelegramConnectionError,
    RegistrationError,
)


class TestChatListener:
    """Test ChatListener initialization and configuration."""

    def test_init_valid(self):
        """Test valid initialization."""
        listener = ChatListener(chat_id=123456789)
        assert listener.chat_id == 123456789
        assert listener.host == "127.0.0.1"
        assert listener.port == 0
        assert not listener.enable_edits
        assert not listener.enable_deletes

    def test_init_invalid_chat_id(self):
        """Test initialization with invalid chat_id."""
        with pytest.raises(InvalidConfigError):
            ChatListener(chat_id=0)
        
        with pytest.raises(InvalidConfigError):
            ChatListener(chat_id=-1)

    def test_init_custom_config(self):
        """Test initialization with custom configuration."""
        listener = ChatListener(
            chat_id=123456789,
            host="192.168.1.1",
            port=5000,
            enable_edits=True,
            enable_deletes=True,
        )
        assert listener.chat_id == 123456789
        assert listener.host == "192.168.1.1"
        assert listener.port == 5000
        assert listener.enable_edits
        assert listener.enable_deletes

    def test_is_running_initial_state(self):
        """Test is_running returns False initially."""
        listener = ChatListener(chat_id=123456789)
        assert not listener.is_running()


class TestMessageEventHandling:
    """Test message event handling."""

    def test_on_message_decorator(self):
        """Test on_message decorator registration."""
        listener = ChatListener(chat_id=123456789)
        
        callback = Mock()
        
        with patch.object(listener, '_start_server'):
            with patch.object(listener, '_register_with_desktop'):
                result = listener.on_message(callback)
        
        assert result is callback
        assert 'message' in listener._callbacks

    def test_on_message_invalid_callback(self):
        """Test on_message with non-callable raises error."""
        listener = ChatListener(chat_id=123456789)
        
        with pytest.raises(ValueError, match="callback must be callable"):
            listener.on_message("not_callable")

    def test_on_message_edit_decorator(self):
        """Test on_message_edit decorator registration."""
        listener = ChatListener(chat_id=123456789, enable_edits=True)
        
        callback = Mock()
        
        with patch.object(listener, '_start_server'):
            with patch.object(listener, '_register_with_desktop'):
                result = listener.on_message_edit(callback)
        
        assert result is callback
        assert 'message_edit' in listener._callbacks

    def test_on_message_delete_decorator(self):
        """Test on_message_delete decorator registration."""
        listener = ChatListener(chat_id=123456789, enable_deletes=True)
        
        callback = Mock()
        
        with patch.object(listener, '_start_server'):
            with patch.object(listener, '_register_with_desktop'):
                result = listener.on_message_delete(callback)
        
        assert result is callback
        assert 'message_delete' in listener._callbacks


class TestEventHandling:
    """Test event processing."""

    def test_handle_message_event(self):
        """Test handling of message_event."""
        listener = ChatListener(chat_id=123456789)
        callback = Mock()
        listener._callbacks['message'] = callback
        
        event_data = {
            "type": "message_event",
            "message": {
                "chat_id": 123456789,
                "message_id": 1,
                "sender_id": 987654,
                "text": "Hello",
                "timestamp": 1693814400,
            }
        }
        
        listener._handle_event(event_data)
        
        callback.assert_called_once()
        args = callback.call_args[0]
        assert isinstance(args[0], MessageEvent)
        assert args[0].text == "Hello"

    def test_handle_message_edit_event(self):
        """Test handling of message_edit_event."""
        listener = ChatListener(chat_id=123456789, enable_edits=True)
        callback = Mock()
        listener._callbacks['message_edit'] = callback
        
        event_data = {
            "type": "message_edit_event",
            "message_edit": {
                "chat_id": 123456789,
                "message_id": 1,
                "sender_id": 987654,
                "text": "Edited message",
                "timestamp": 1693814400,
                "is_edited": True,
                "edit_timestamp": 1693814500,
            }
        }
        
        listener._handle_event(event_data)
        
        callback.assert_called_once()
        args = callback.call_args[0]
        assert isinstance(args[0], MessageEvent)
        assert args[0].is_edited

    def test_handle_message_delete_event(self):
        """Test handling of message_delete_event."""
        listener = ChatListener(chat_id=123456789, enable_deletes=True)
        callback = Mock()
        listener._callbacks['message_delete'] = callback
        
        event_data = {
            "type": "message_delete_event",
            "message_id": 42,
        }
        
        listener._handle_event(event_data)
        
        callback.assert_called_once_with(42)

    def test_handle_event_with_no_callback(self):
        """Test handling event when no callback is registered."""
        listener = ChatListener(chat_id=123456789)
        
        event_data = {
            "type": "message_event",
            "message": {
                "chat_id": 123456789,
                "message_id": 1,
                "sender_id": 987654,
                "text": "Hello",
                "timestamp": 1693814400,
            }
        }
        
        # Should not raise exception
        listener._handle_event(event_data)


class TestContextManager:
    """Test context manager functionality."""

    def test_context_manager(self):
        """Test ChatListener as context manager."""
        listener = ChatListener(chat_id=123456789)
        
        with patch.object(listener, 'stop') as mock_stop:
            with listener as ctx:
                assert ctx is listener
            
            mock_stop.assert_called_once()
