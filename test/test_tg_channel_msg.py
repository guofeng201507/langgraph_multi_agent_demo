from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto, MessageMediaDocument
import os
from dotenv import load_dotenv

load_dotenv()

# Use user credentials instead of bot token
api_id = os.getenv("TG_API_ID")
api_hash = os.getenv("TG_API_HASH")
phone = os.getenv("TG_PHONE")
username = os.getenv("TG_USERNAME")

channel_username = 'OKXGLVoptionsCN'

# Create a session file for user authentication
session_file = 'user_session'

try:
    with TelegramClient(session_file, api_id, api_hash) as client:
        # Start the client with phone number authentication
        client.start(phone=phone)

        # Ensure we're connected
        if not client.is_connected():
            raise Exception("Failed to connect to Telegram")

        # Fetch messages
        messages = client.iter_messages(channel_username, limit=20)

        for i, message in enumerate(messages):
            print(f"\n🔹 Message {i + 1}")
            print(f"📅 Date: {message.date}")
            print(f"📝 Content: {message.text}")

            # Save photos
            if isinstance(message.media, MessageMediaPhoto):
                filename = f"photo_{message.id}.jpg"
                client.download_media(message, filename)
                print(f"🖼️ Photo saved as {filename}")

            # Save documents
            elif isinstance(message.media, MessageMediaDocument):
                filename = f"file_{message.id}"
                client.download_media(message, filename)
                print(f"📄 Document saved as {filename}")

except Exception as e:
    print(f"An error occurred: {str(e)}")