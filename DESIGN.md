# Python Event Listener System for Telegram Desktop

## Overview

This document describes the design for adding Python-based event listeners to Telegram Desktop, enabling external Python scripts to listen for messages in specific chats and trigger custom callbacks.

## Architecture

### 1. Core Components

```
Telegram/SourceFiles/
├── python/                      # New Python integration layer
│   ├── python_bindings.h
│   ├── python_bindings.cpp
│   ├── event_listener_manager.h
│   ├── event_listener_manager.cpp
│   ├── python_event_bridge.h
│   └── python_event_bridge.cpp
├── history/
│   ├── history_item.cpp         # Modified to trigger listeners
│   └── history_widget.cpp
└── core/
    ├── core_settings.cpp        # Store listener configs
    └── session.cpp              # Session-level listener management
```

### 2. Python API Structure

```python
# telegram_listener.py (user-facing API)
from telegram_listener import ChatListener, MessageEvent

# Installation pattern:
# pip install telegram-listener
# Then configure listeners in Telegram Desktop settings

class ChatListener:
    def __init__(self, chat_id: int):
        self.chat_id = chat_id
        self.callbacks = []
    
    def on_message(self, callback: Callable[[MessageEvent], None]):
        """Register callback for incoming messages"""
        self.callbacks.append(callback)
        self._register_with_desktop()
    
    def on_message_edit(self, callback: Callable[[MessageEvent], None]):
        """Register callback for message edits"""
        pass
    
    def on_message_delete(self, callback: Callable[[int], None]):
        """Register callback for message deletions"""
        pass

class MessageEvent:
    chat_id: int
    message_id: int
    sender_id: int
    text: str
    timestamp: datetime
    reply_to_id: Optional[int]
    media: Optional[MediaInfo]
```

### 3. Communication Protocol

**IPC Method**: Unix socket (Linux/Mac) + Named pipes (Windows)

**Message Format**:
```json
{
  "type": "listener_register",
  "chat_id": 123456789,
  "callback_id": "uuid",
  "host": "127.0.0.1",
  "port": 9999
}

{
  "type": "message_event",
  "chat_id": 123456789,
  "message_id": 1,
  "sender_id": 987654,
  "text": "Hello",
  "timestamp": 1693814400,
  "media": null
}
```

### 4. Data Flow

```
User Message in Chat
    ↓
HistoryWidget detects new message
    ↓
HistoryItem created/updated
    ↓
EventListenerManager::notifyMessage()
    ↓
Query registered listeners for this chat_id
    ↓
For each listener: serialize message → send via IPC
    ↓
Python process receives event
    ↓
User's callback function invoked
```

## Implementation Details

### Phase 1: C++ Core Infrastructure

**EventListenerManager** (header):
```cpp
class EventListenerManager : public QObject {
public:
    struct ListenerConfig {
        int64 chatId;
        QString processName;
        QString socketPath;  // or pipeName on Windows
        bool enableMessageEvents = true;
        bool enableEditEvents = false;
        bool enableDeleteEvents = false;
    };
    
    // Register a listener (called by Python via IPC)
    void registerListener(const ListenerConfig &config);
    void unregisterListener(int64 chatId, const QString &processName);
    
    // Called when messages arrive
    void notifyMessageReceived(not_null<HistoryItem*> item);
    void notifyMessageEdited(not_null<HistoryItem*> item);
    void notifyMessageDeleted(MsgId id, int64 chatId);

private:
    QMap<int64, QList<ListenerConfig>> _chatListeners;  // chat_id -> listeners
    void _sendEventToListener(const ListenerConfig &listener, 
                              const QJsonDocument &event);
    QJsonDocument _serializeMessage(not_null<HistoryItem*> item);
};
```

**PythonEventBridge** (IPC handler):
```cpp
class PythonEventBridge : public QObject {
public:
    // Listen for incoming Python registration requests
    void startIPCServer();
    
private slots:
    void _onPythonConnectionRequest();
    void _onIPCMessageReceived(const QJsonDocument &doc);
    
private:
    QLocalServer *_server;  // Unix socket on Linux/Mac
    // Or: QWindowsLocalServer for Windows named pipes
    QMap<QString, QLocalSocket*> _connections;
};
```

### Phase 2: Python Bindings

**telegram_listener.py**:
```python
import json
import socket
import threading
from typing import Callable, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MessageEvent:
    chat_id: int
    message_id: int
    sender_id: int
    text: str
    timestamp: int
    reply_to_id: Optional[int] = None
    media: Optional[dict] = None
    
    def __post_init__(self):
        self.timestamp = datetime.fromtimestamp(self.timestamp)

class ChatListener:
    def __init__(self, chat_id: int, host: str = "127.0.0.1", port: int = 0):
        self.chat_id = chat_id
        self.host = host
        self.port = port
        self._callbacks = {}
        self._socket = None
        self._server = None
        self._running = False
    
    def on_message(self, callback: Callable[[MessageEvent], None]):
        """Register callback for incoming messages"""
        if not self._running:
            self._start_server()
        
        self._callbacks['message'] = callback
        self._register_with_desktop('on_message')
        return callback
    
    def _start_server(self):
        """Start local IPC server to receive events from Telegram Desktop"""
        import socket
        self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server.bind((self.host, self.port))
        self._server.listen(1)
        
        # Get actual port if was 0 (let OS choose)
        self.port = self._server.getsockname()[1]
        
        # Start receiving thread
        self._running = True
        self._receiver_thread = threading.Thread(target=self._receive_loop, daemon=True)
        self._receiver_thread.start()
    
    def _receive_loop(self):
        """Receive events from Telegram Desktop"""
        while self._running:
            try:
                conn, _ = self._server.accept()
                data = conn.recv(4096).decode('utf-8')
                conn.close()
                
                if data:
                    event_data = json.loads(data)
                    self._handle_event(event_data)
            except Exception as e:
                print(f"Error receiving event: {e}")
    
    def _handle_event(self, event_data: dict):
        """Process received event and call registered callback"""
        event_type = event_data.get('type')
        
        if event_type == 'message_event' and 'message' in self._callbacks:
            msg = MessageEvent(**event_data['message'])
            self._callbacks['message'](msg)
    
    def _register_with_desktop(self, event_type: str):
        """Send registration request to Telegram Desktop"""
        import socket
        
        # Connect to Telegram Desktop's IPC server
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect(("127.0.0.1", 9000))  # Telegram's IPC port
            
            registration = {
                "type": "listener_register",
                "chat_id": self.chat_id,
                "event_type": event_type,
                "host": self.host,
                "port": self.port
            }
            
            sock.sendall(json.dumps(registration).encode('utf-8'))
            sock.close()
        except Exception as e:
            print(f"Failed to register listener with Telegram Desktop: {e}")
    
    def stop(self):
        """Stop listening for events"""
        self._running = False
        if self._server:
            self._server.close()

# Example usage:
if __name__ == "__main__":
    def on_new_message(event: MessageEvent):
        print(f"New message in chat {event.chat_id} from {event.sender_id}:")
        print(f"  {event.text}")
        print(f"  Timestamp: {event.timestamp}")
    
    # Listen to specific chat
    listener = ChatListener(chat_id=123456789)
    listener.on_message(on_new_message)
    
    print(f"Listening on {listener.host}:{listener.port}")
    
    # Keep running
    import time
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        listener.stop()
        print("Stopped listening")
```

### Phase 3: Integration Points

**In `history/history_widget.cpp`**:
```cpp
void HistoryWidget::messageReceived(not_null<HistoryItem*> item) {
    // Existing code...
    
    // NEW: Notify Python listeners
    if (auto manager = EventListenerManager::instance()) {
        manager->notifyMessageReceived(item);
    }
}
```

**In `core/session.cpp`**:
```cpp
Session::Session(...) {
    // Existing initialization...
    
    // NEW: Initialize event listener manager
    _eventListenerManager = std::make_unique<EventListenerManager>(this);
}
```

## Configuration Storage

Store listener registrations in session settings:

**Session Settings Format** (binary serialization via QDataStream):
```
[listener count: int32]
  For each listener:
    [chat_id: int64]
    [process_name: QString]
    [socket_path: QString]
    [enable_messages: bool]
    [enable_edits: bool]
    [enable_deletes: bool]
```

## Security Considerations

1. **Isolation**: Only communicate with Python processes on localhost (127.0.0.1)
2. **Authentication**: Process must send matching registration token
3. **Rate Limiting**: Throttle event notifications per chat/process
4. **Permissions**: User must explicitly enable Python listeners in settings
5. **Sandboxing**: Consider running Python callbacks in isolated thread pool

## Testing

**Unit Tests**:
- EventListenerManager registration/unregistration
- Message serialization correctness
- IPC socket lifecycle

**Integration Tests**:
- Python script registers listener → receives messages
- Multiple listeners on same chat
- Event type filtering (message/edit/delete)
- Listener crashes don't crash Telegram Desktop

**Test Scenario** (in `test/`):
```cpp
Runner::Stage{
    u"python listener receives message"_q,
    [this] { return setupChatWithMessage(); },
    [this] { return _messageDelivered; },
    [this] { checkListenerReceived(); }
}
```

## Deployment

1. **Build Phase**: Enable Python listener feature via CMake flag:
   ```cmake
   option(TDESKTOP_ENABLE_PYTHON_LISTENERS "Enable Python event listeners" ON)
   ```

2. **Python Package**:
   ```
   setup.py
   setup.cfg
   pyproject.toml
   telegram_listener/__init__.py
   telegram_listener/client.py
   telegram_listener/events.py
   telegram_listener/exceptions.py
   ```

3. **Installation**:
   ```bash
   pip install telegram-listener
   ```

## API Examples

### Basic Usage
```python
from telegram_listener import ChatListener, MessageEvent

listener = ChatListener(chat_id=123456789)

@listener.on_message
def handle_message(event: MessageEvent):
    print(f"{event.sender_id}: {event.text}")
```

### Multiple Chats
```python
chats = [123456789, 987654321, 555555555]
listeners = {chat_id: ChatListener(chat_id) for chat_id in chats}

for listener in listeners.values():
    @listener.on_message
    def on_msg(event):
        print(f"Chat {event.chat_id}: {event.text}")
```

### With Message Editing
```python
listener = ChatListener(chat_id=123456789)

@listener.on_message
def handle_new(event):
    print(f"New: {event.text}")

@listener.on_message_edit
def handle_edit(event):
    print(f"Edited: {event.text}")
```

## Future Enhancements

1. **Bidirectional Communication**: Send messages from Python back to Telegram
2. **Media Handling**: Full media metadata and local file paths
3. **Reaction Events**: React to emoji reactions
4. **Typing Indicators**: Detect when users are typing
5. **User Presence**: Track online/offline status
6. **Rich Message Formatting**: Markdown/HTML support in events
7. **Database Snapshot**: Query message history via Python API
8. **Plugin System**: Allow Python plugins to modify messages before display

## Dependencies

- Python 3.8+
- Qt 6.0+ (via Telegram Desktop)
- pybind11 (optional, for direct C++ binding)
- Boost.Python (optional alternative)

## Build Integration

Add to `CMakeLists.txt`:
```cmake
if (TDESKTOP_ENABLE_PYTHON_LISTENERS)
    target_sources(Telegram PRIVATE
        Telegram/SourceFiles/python/python_bindings.cpp
        Telegram/SourceFiles/python/event_listener_manager.cpp
        Telegram/SourceFiles/python/python_event_bridge.cpp
    )
    target_link_libraries(Telegram PRIVATE python3)
endif()
```

---

**Status**: Design Phase
**Priority**: Medium
**Effort**: 3-4 weeks (core C++ + Python bindings + testing)
**Risk**: Moderate (IPC security, Python interpreter embedding)
