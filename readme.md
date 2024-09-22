
# Raspberry Pi Doorbell to Telegram Message

This project allows you to connect a physical doorbell to a Raspberry Pi and send a notification to a Telegram chat when the doorbell is pressed. It's a simple and effective way to integrate your doorbell with a messaging platform for real-time notifications.

## Requirements

- Raspberry Pi (with GPIO support)
- Python 3
- Internet connection
- Telegram account

## Installation

1. **Install Python** on your Raspberry Pi:
   ```bash
   sudo apt-get update
   sudo apt-get install python3 python3-pip
   ```

2. **Install required Python packages** by creating a virtual environment (optional but recommended):
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # activate the virtual environment
   pip install -r requirements.txt
   ```

   If you don’t want to use a virtual environment, simply run:
   ```bash
   pip3 install -r requirements.txt
   ```

## Setup

1. **Create a Telegram Bot**:
   - Open Telegram and search for `@BotFather`.
   - Start a chat with `@BotFather` and use the `/newbot` command to create a new bot.
   - Follow the instructions and get your **API Token**.
   
2. **Configure `config.yml`**:
   - Copy the **API Token** you received from `@BotFather` into the `config.yml` file under the `telegram.api_token` field.
   - Send a message to the bot you just created to initialize the chat.
   - Retrieve your **Chat ID**:
     - Open a browser and visit the following URL (replace `API_KEY_HERE` with your bot's API key):
       ```
       https://api.telegram.org/botAPI_KEY_HERE/getUpdates
       ```
     - Look for your message and copy the `chat.id` value.
   - Add this **Chat ID** to your `config.yml` file under `telegram.chat_id`.

3. **Connect your Doorbell to the Raspberry Pi**:
   - Connect a button or sensor (doorbell) to one of the Raspberry Pi's GPIO pins (e.g., GPIO pin 17).
   - Ensure proper wiring (one side to a GPIO pin, the other side to GND).

4. **Edit Configurable Messages**:
   - You can modify the messages that are sent when the system starts, when the doorbell is pressed, or when the system is stopped. These are located in the `config.yml` file under `messages`:
     ```yaml
     messages:
       system_start: "System started and ready to receive doorbell signals."
       doorbell_ring: "Someone rang the doorbell!"
       system_shutdown: "The system is shutting down."
       gpio_cleanup: "GPIO pins have been reset and the system has stopped."
     ```

## Running the Script

1. **Start the Python script** to listen for the doorbell:
   ```bash
   python3 your_script.py
   ```

2. The system will now monitor the GPIO pin for a doorbell press and send a Telegram notification to the configured chat.

## Example Config (`config.yml`)

```yaml
telegram:
  api_token: 'YOUR_BOT_API_KEY'
  chat_id: 'YOUR_CHAT_ID'

messages:
  system_start: "System started and ready to receive doorbell signals."
  doorbell_ring: "Someone rang the doorbell!"
  system_shutdown: "The system is shutting down."
  gpio_cleanup: "GPIO pins have been reset and the system has stopped."
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
