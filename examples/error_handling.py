"""
Example: Error handling and logging
"""

import logging
from telegram_listener import ChatListener
from telegram_listener.exceptions import (
    TelegramListenerError,
    ConnectionError,
    RegistrationError,
    InvalidConfigError,
)

# Enable debug logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    try:
        # Try to create a listener with invalid config
        listener = ChatListener(chat_id=-1)
        
    except InvalidConfigError as e:
        print(f"Invalid configuration: {e}")
        return
    
    try:
        # Create listener with valid config
        listener = ChatListener(chat_id=123456789)
        
        @listener.on_message
        def handle_message(event):
            try:
                print(f"Message: {event.text}")
            except Exception as e:
                print(f"Error processing message: {e}")
        
        print("Listener created successfully")
        
    except ConnectionError as e:
        print(f"Cannot connect to Telegram Desktop: {e}")
        print("Make sure Telegram Desktop is running")
        return
        
    except RegistrationError as e:
        print(f"Registration failed: {e}")
        print("Check that you have access to the chat")
        return
        
    except TelegramListenerError as e:
        print(f"Telegram listener error: {e}")
        return
    
    except Exception as e:
        print(f"Unexpected error: {e}")
        return


if __name__ == "__main__":
    main()
