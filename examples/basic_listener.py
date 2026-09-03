"""
Basic example: Listen to a single chat
"""

from telegram_listener import ChatListener
import time

def main():
    # Create listener for a specific chat
    # Replace with your actual chat_id
    listener = ChatListener(chat_id=123456789)
    
    # Register callback for new messages
    @listener.on_message
    def handle_message(event):
        print(f"\n[New Message]")
        print(f"  Chat ID: {event.chat_id}")
        print(f"  Sender ID: {event.sender_id}")
        print(f"  Message ID: {event.message_id}")
        print(f"  Text: {event.text}")
        print(f"  Time: {event.datetime}")
        
        if event.media:
            print(f"  Media: {event.media.media_type}")
    
    print(f"Listening to chat {listener.chat_id}")
    print("Press Ctrl+C to stop...\n")
    
    # Keep listener running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping listener...")
        listener.stop()
        print("Stopped")


if __name__ == "__main__":
    main()
