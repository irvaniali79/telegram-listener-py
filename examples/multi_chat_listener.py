"""
Advanced example: Monitor multiple chats and handle edits/deletes
"""

from telegram_listener import ChatListener
import time
from typing import Dict

def main():
    # Chats to monitor
    chat_ids = [123456789, 987654321, 555555555]
    listeners: Dict[int, ChatListener] = {}
    
    print("Starting multi-chat listener...\n")
    
    for chat_id in chat_ids:
        # Create listener with edit and delete tracking enabled
        listener = ChatListener(
            chat_id=chat_id,
            enable_edits=True,
            enable_deletes=True,
        )
        listeners[chat_id] = listener
        
        # Register callback for new messages
        @listener.on_message
        def on_message(event):
            print(f"[NEW] Chat {event.chat_id}: {event.sender_id} -> {event.text[:50]}")
        
        # Register callback for edits
        @listener.on_message_edit
        def on_edit(event):
            print(f"[EDIT] Chat {event.chat_id}: Message {event.message_id} -> {event.text[:50]}")
        
        # Register callback for deletes
        @listener.on_message_delete
        def on_delete(message_id: int):
            print(f"[DELETE] Message {message_id}")
    
    print(f"Monitoring {len(listeners)} chats")
    print("Press Ctrl+C to stop...\n")
    
    # Keep listeners running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping listeners...")
        for listener in listeners.values():
            listener.stop()
        print("All listeners stopped")


if __name__ == "__main__":
    main()
