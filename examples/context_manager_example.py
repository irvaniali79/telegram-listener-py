"""
Example: Using ChatListener with context manager
"""

from telegram_listener import ChatListener
import time

def main():
    # Use context manager for automatic cleanup
    with ChatListener(chat_id=123456789) as listener:
        @listener.on_message
        def handle_message(event):
            print(f"Message: {event.text}")
            print(f"From: {event.sender_id}")
            print(f"Time: {event.datetime}")
        
        print(f"Listening to chat {listener.chat_id}")
        print("Will listen for 30 seconds...\n")
        
        time.sleep(30)
    
    # Listener automatically stopped here
    print("\nListener stopped (context manager exited)")


if __name__ == "__main__":
    main()
