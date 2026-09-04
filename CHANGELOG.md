# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Planned
- Bidirectional messaging support
- Direct message sending
- Message history queries
- Async/await API
- Plugin system
- Rich message formatting

## [0.1.0] - 2024-01-XX

### Added
- Initial public release
- `ChatListener` class for monitoring chats
- Message event callbacks (`on_message`, `on_message_edit`, `on_message_delete`)
- `MessageEvent` dataclass with full event data
- `MediaInfo` for media attachments
- IPC-based communication with Telegram Desktop
- Context manager support
- Comprehensive error handling
- Full test suite
- Example scripts
- Complete documentation

### Features
- Listen to messages in specific Telegram chats
- Track message edits (optional)
- Track message deletions (optional)
- Handle media information
- Support for reactions, forwarded messages, pinned messages
- Datetime conversion from Unix timestamps
- JSON serialization/deserialization
- Threading for non-blocking event handling
- Thread-safe operations
- Logging support

[Unreleased]: https://github.com/irvaniali79/telegram-listener-py/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/irvaniali79/telegram-listener-py/releases/tag/v0.1.0
