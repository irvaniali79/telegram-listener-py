"""
Unit tests for event data structures.
"""

import pytest
from datetime import datetime
from telegram_listener.events import MessageEvent, MediaInfo


class TestMediaInfo:
    """Test MediaInfo dataclass."""

    def test_create_minimal(self):
        """Test creating MediaInfo with minimal fields."""
        media = MediaInfo(
            media_type="photo",
            file_id="file123"
        )
        
        assert media.media_type == "photo"
        assert media.file_id == "file123"
        assert media.file_size == 0
        assert media.duration is None

    def test_create_full(self):
        """Test creating MediaInfo with all fields."""
        media = MediaInfo(
            media_type="video",
            file_id="file123",
            file_size=1024000,
            mime_type="video/mp4",
            duration=120,
            width=1920,
            height=1080,
            file_name="video.mp4",
            local_path="/path/to/video.mp4",
        )
        
        assert media.media_type == "video"
        assert media.file_id == "file123"
        assert media.file_size == 1024000
        assert media.mime_type == "video/mp4"
        assert media.duration == 120
        assert media.width == 1920
        assert media.height == 1080
        assert media.file_name == "video.mp4"
        assert media.local_path == "/path/to/video.mp4"


class TestMessageEvent:
    """Test MessageEvent dataclass."""

    def test_create_minimal(self):
        """Test creating MessageEvent with minimal fields."""
        event = MessageEvent(
            chat_id=123456789,
            message_id=1,
            sender_id=987654,
            text="Hello",
            timestamp=1693814400,
        )
        
        assert event.chat_id == 123456789
        assert event.message_id == 1
        assert event.sender_id == 987654
        assert event.text == "Hello"
        assert event.timestamp == 1693814400
        assert event.reply_to_id is None
        assert event.media is None
        assert not event.is_edited

    def test_datetime_property(self):
        """Test datetime property conversion."""
        event = MessageEvent(
            chat_id=123456789,
            message_id=1,
            sender_id=987654,
            text="Hello",
            timestamp=1693814400,
        )
        
        dt = event.datetime
        assert isinstance(dt, datetime)
        assert dt.timestamp() == 1693814400

    def test_edit_datetime_property_none(self):
        """Test edit_datetime property when not edited."""
        event = MessageEvent(
            chat_id=123456789,
            message_id=1,
            sender_id=987654,
            text="Hello",
            timestamp=1693814400,
            is_edited=False,
        )
        
        assert event.edit_datetime is None

    def test_edit_datetime_property_set(self):
        """Test edit_datetime property when edited."""
        event = MessageEvent(
            chat_id=123456789,
            message_id=1,
            sender_id=987654,
            text="Edited",
            timestamp=1693814400,
            is_edited=True,
            edit_timestamp=1693814500,
        )
        
        dt = event.edit_datetime
        assert isinstance(dt, datetime)
        assert dt.timestamp() == 1693814500

    def test_create_with_media(self):
        """Test creating MessageEvent with media."""
        media = MediaInfo(
            media_type="photo",
            file_id="file123",
            file_size=1024,
        )
        
        event = MessageEvent(
            chat_id=123456789,
            message_id=1,
            sender_id=987654,
            text="Photo",
            timestamp=1693814400,
            media=media,
        )
        
        assert event.media is not None
        assert event.media.media_type == "photo"
        assert event.media.file_id == "file123"

    def test_to_dict(self):
        """Test converting MessageEvent to dictionary."""
        event = MessageEvent(
            chat_id=123456789,
            message_id=1,
            sender_id=987654,
            text="Hello",
            timestamp=1693814400,
        )
        
        data = event.to_dict()
        
        assert isinstance(data, dict)
        assert data['chat_id'] == 123456789
        assert data['message_id'] == 1
        assert data['sender_id'] == 987654
        assert data['text'] == "Hello"
        assert data['timestamp'] == 1693814400

    def test_from_dict(self):
        """Test creating MessageEvent from dictionary."""
        data = {
            'chat_id': 123456789,
            'message_id': 1,
            'sender_id': 987654,
            'text': "Hello",
            'timestamp': 1693814400,
        }
        
        event = MessageEvent.from_dict(data)
        
        assert event.chat_id == 123456789
        assert event.message_id == 1
        assert event.sender_id == 987654
        assert event.text == "Hello"
        assert event.timestamp == 1693814400

    def test_from_dict_with_media(self):
        """Test creating MessageEvent from dictionary with media."""
        data = {
            'chat_id': 123456789,
            'message_id': 1,
            'sender_id': 987654,
            'text': "Photo",
            'timestamp': 1693814400,
            'media': {
                'media_type': 'photo',
                'file_id': 'file123',
                'file_size': 1024,
            }
        }
        
        event = MessageEvent.from_dict(data)
        
        assert event.media is not None
        assert event.media.media_type == 'photo'
        assert event.media.file_id == 'file123'
        assert event.media.file_size == 1024

    def test_round_trip_serialization(self):
        """Test to_dict and from_dict are consistent."""
        original = MessageEvent(
            chat_id=123456789,
            message_id=1,
            sender_id=987654,
            text="Hello",
            timestamp=1693814400,
            reply_to_id=0,
            is_edited=False,
        )
        
        data = original.to_dict()
        restored = MessageEvent.from_dict(data)
        
        assert original.chat_id == restored.chat_id
        assert original.message_id == restored.message_id
        assert original.sender_id == restored.sender_id
        assert original.text == restored.text
        assert original.timestamp == restored.timestamp
