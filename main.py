from telethon import TelegramClient, events
import asyncio
import requests
import time
from datetime import datetime, timedelta
import threading
from flask import Flask, jsonify
# from notee import amir
from twilio.rest import Client  # Import Twilio

# Replace with your Telegram API credentials
# Replace with your Telegram API credentials
api_id = ''  # Your API ID
api_hash = ''

# Channel names (replace with actual usernames or IDs)
source_channel_name = 'source cannel'  # The name of the source channel
target_channel_name = 'target'    # The name of the target channel

# Google Drive file link for session file
drive_link = ""

# Google Drive file link for session fi

# Twilio credentials/ use twilio for free offer or use another api 
account_sid1 = 'urid'
auth_token1 = ''
twilio_phone_number1 = '+1'
your_phone_number1 = '+251'

# Initialize Twilio client
twilio_client1 = Client(account_sid1, auth_token1)

last_call_time = None
cooldown_time = 3 * 60  # 3 minutes in seconds
# Function to make a call using Twilio with retry logic and immediate hangup after initiation
def phone1():
    global last_call_time

    max_retries = 5  # Maximum number of retries (you can increase if needed)
    attempt = 0

    # Only make a call if the cooldown period has passed
    if last_call_time and (datetime.now() - last_call_time).total_seconds() < cooldown_time:
        print("Call already made recently. Skipping this call.")
        return

    # Retry logic for making the call
    while attempt < max_retries:
        try:
            # Make the initial call
            call = twilio_client1.calls.create(
                to=your_phone_number1,
                from_=twilio_phone_number1,
                url="https://demo.twilio.com/welcome/voice/",
                
            )
            print(f"Call initiated successfully: {call.sid}")
            last_call_time = datetime.now()  # Update the last call time

            # # Immediately hang up the call
            # for _ in range(20):  # Checks every second for up to 20 seconds
            #     call = twilio_client1.calls(call.sid).fetch()
            #     if call.status == "in-progress":  # If the call is answered
            #         print(f"Call answered: {call.sid}. Ending the call.")
            #         twilio_client1.calls(call.sid).update(status="completed")
            #         print(f"Call ended immediately after being answered: {call.sid}")
            #         return
            #     elif call.status in ["completed", "canceled", "busy", "failed"]:
            #         print(f"Call status changed to {call.status}. Exiting without hanging up.")
            #         return
            #     time.sleep(1)  # Wait 1 second before checking again

            # print("Call was not answered within the check period. Exiting without hangup.")
            return  # Exit the function once the call is successful and ended

        except Exception as e:
            attempt += 1
            print(f"Failed to make the call (Attempt {attempt}/{max_retries}): {e}")

            # If max retries reached, stop retrying
            if attempt >= max_retries:
                print("Max retries reached. Call could not be initiated.")
                return

            # Wait a bit before retrying (to avoid rapid retries)
            time.sleep(5)  

account_sid2 = ''
auth_token2 = ''
twilio_phone_number2 = '+'
your_phone_number2 = '+'
message_timestamps = {}
# Initialize Twilio client
twilio_client2 = Client(account_sid2, auth_token2)

## Function to make a call using Twilio with retry logic
def phone2():
    max_retries = 7  # Maximum number of retries (you can increase if needed)
    attempt = 0

    while attempt < max_retries:
        try:
            call = twilio_client2.calls.create(
                to=your_phone_number2,
                from_=twilio_phone_number2,
                url='http://twimlets.com/holdmusic?Bucket=com.twilio.music.ambient'
            )
          
            print(f"Call initiated successfully: {call.sid}")
            return  # Exit the function once the call is successful
        except Exception as e:
            attempt += 1
            print(f"Failed to make the call (Attempt {attempt}/{max_retries}): {e}")

            # If max retries reached, stop retrying
            if attempt >= max_retries:
                print("Max retries reached. Call could not be initiated.")
                return

            # Wait a bit before retrying (to avoid rapid retries)
           
            time.sleep(5)  # Wait for 5 seconds before retrying

# Function to download session file from Google Drive
def download_session_file():
    response = requests.get(drive_link)
    if response.status_code == 200:
        with open('session_name.session', 'wb') as f:
            f.write(response.content)
        print("Session file downloaded.")
    else:
        print("Failed to download session file. Status code:", response.status_code)

async def start_bot():
    download_session_file()

    async with TelegramClient('session_name', api_id, api_hash) as client:
        print("Bot started.")

        dialogs = await client.get_dialogs()
        source_channel = None
        target_channel = None
        for dialog in dialogs:
            if dialog.name == source_channel_name:
                source_channel = dialog.entity
            if dialog.name == target_channel_name:
                target_channel = dialog.entity

        if source_channel and target_channel:
            print(f"Found source channel: {source_channel_name}")
            print(f"Found target channel: {target_channel_name}", flush=True)
        else:
            print(f"Could not find one or both channels.")
            return

        # # Handler for new messages
        @client.on(events.NewMessage(chats=source_channel))
        async def handler(event):
            # await forward_message(event)
            print("got message!!!")
            # Make a call when a new message is received
            
            phone1()
        
            phone2()
           

        # # Handler for edited messages
        # @client.on(events.MessageEdited(chats=source_channel))
        # async def edit_handler(event):
        #     await forward_message(event, is_edit=True)
        # @client.on(events.NewMessage(chats=source_channel))
        # async def handler(event):
        #     # Forward the new message immediately and store its timestamp
        #     await forward_message(event)
        #     message_timestamps[event.message.id] = time.time()
        #     print("Got new message!")

        # Handler for edited messages
        # @client.on(events.MessageEdited(chats=source_channel))
        # async def edit_handler(event):
        #     # Check if 20 seconds have passed since the message was initially sent
        #     message_id = event.message.id
        #     if message_id in message_timestamps and time.time() - message_timestamps[message_id] > 20:
        #         await forward_message(event, is_edit=True)
        #         print("Got edited message!")


        async def forward_message(event, is_edit=False):
            message = event.message
            try:
                if message.text and not message.photo:  # Text message
                    await client.send_message(target_channel, message.text)
                    print(f"{'Edited' if is_edit else 'Text'} message sent to {target_channel_name}: {message.text}")

                elif message.photo:  # Photo message
                    file_path = await message.download_media()
                    caption = message.text or ""
                    await client.send_file(target_channel, file_path, caption=caption)
                    print(f"{'Edited' if is_edit else 'Photo'} sent to {target_channel_name} with caption: {caption}")

                elif message.voice:  # Voice message
                    file_path = await message.download_media()
                    await client.send_file(target_channel, file_path)
                    print(f"{'Edited' if is_edit else 'Voice'} message sent to {target_channel_name}")

                elif message.document:  # Document message
                    file_path = await message.download_media()
                    await client.send_file(target_channel, file_path)
                    print(f"{'Edited' if is_edit else 'Document'} sent to {target_channel_name}")

                else:
                    print("Message type not supported.")

            except Exception as e:
                print(f"Failed to forward message: {e}")

        # Keep the bot running
        await client.run_until_disconnected()

# Flask app setup
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello, this is the home page of the bot!"

@app.route('/health_check', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

# Function to run the bot in a separate thread
def run_bot():
    asyncio.run(start_bot())

if __name__ == '__main__':
    threading.Thread(target=run_bot).start()
    app.run(host='0.0.0.0', port=8000)
