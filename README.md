# Telegram Notification Bot

This bot monitors a specified Telegram channel and triggers notifications via phone calls when new messages are detected. Notifications are managed using Twilio, ensuring prompt alerts. Message forwarding is also supported as an additional feature.

## Features

- **Real-time Notifications**: Receives Telegram messages and triggers phone calls instantly.
- **Message Forwarding**: Optionally forwards messages to a target Telegram channel.
- **Flask Server**: Includes a lightweight Flask server for health checks.
2. **Download the Session File**:
   - Save your Telegram session file to Google Drive.
   - Update the `drive_link` variable in the code with the Google Drive file link.

3. **Configuration**:
   - Replace placeholders in the code:
     - `api_id` and `api_hash`: Your Telegram API credentials.
     - `source_channel_name` and `target_channel_name`: Names of your Telegram channels.
     - `account_sid1`, `auth_token1`, `twilio_phone_number1`, and `your_phone_number1`: First Twilio account details.
     - `account_sid2`, `auth_token2`, `twilio_phone_number2`, and `your_phone_number2`: Second Twilio account details.

4. **Run the Script**:
   - Start the bot by running:
     ```bash
     python main.py
     ```

5. **Access the Flask Server**:
   - The integrated Flask server allows health checks.
   - Visit: `http://localhost:8000/health_check` to check the bot's status.

## Usage

- **Phone Call Notifications**: The bot monitors the `source_channel_name` for new messages and triggers phone call notifications using Twilio.
- **Optional Message Forwarding**: The bot can also forward messages to `target_channel_name`, if configured.
