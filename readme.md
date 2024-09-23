# Raspberry Pi: Doorbell Ring to Telegram Message 

This project allows you to connect a physical doorbell to a Raspberry Pi and send a notification to a Telegram chat when the doorbell is pressed. It's a simple and effective way to integrate your doorbell with a messaging platform for real-time notifications.

<p align="center">
  <a href="https://github.com/EbookFoundation/free-programming-books/stargazers">
    <img src="https://img.shields.io/github/forks/SimpliAj/PiBellBot?style=flat&logo=github&logoColor=whitesmoke&label=Forks" alt="GitHub repo stars"/>
    <img src="https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram Badge" width="90"  height="20"/>
    <img src="https://img.shields.io/github/stars/SimpliAj/PiBellBot?style=flat&logo=github&logoColor=whitesmoke&label=Stars" alt="GitHub repo stars"/>
  </a>
</p>
<p align="center">
  <img src="https://i.imgur.com/Lgy4a8N.png" alt="PiBellBot Logo" width="250"/>
  <br><a href="https://discord.gg/dRjXvWcbsM">Discord Server</a>
</p>


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
      telegram_messages:
        system_start: "The doorbell notification system is online."
        doorbell_ring: "Someone is at the door!"
        system_shutdown: "The doorbell notification system is being turned off."
        gpio_cleanup: "The system has been shut down and cleaned up."
     ```

## Running the Script

1. **Start the Python script** to listen for the doorbell:
   ```bash
   python3 your_script.py
   ```

2. The system will now monitor the GPIO pin for a doorbell press and send a Telegram notification to the configured chat.

## Example Config (`config.yml`)

```yaml
settings:
  enable_cmd_prints: false  # Toggle to enable/disable console prints
  log_telegram_send: false  # Toggle to enable/disable logging Telegram message send status
  gpio_pin: 17  # Define the GPIO pin number here

telegram:
  api_token: 'YOUR_BOT_API_KEY'
  chat_id: 'YOUR_CHAT_ID'

print_messages:
  system_start: "System started and waiting for the doorbell signal."
  doorbell_ring: "Doorbell was pressed!"
  system_shutdown: "System is shutting down..."
  gpio_cleanup: "GPIO cleanup done and system is stopped."

telegram_messages:
  system_start: "ℹ️ Important Information\n\nThe doorbell system has started!"
  doorbell_ring: "💥 Important Information 💥\n\nThe doorbell has rung!"
  system_shutdown: "ℹ️ Important Information\n\nThe system is shutting down!"
  gpio_cleanup: "ℹ️ Important Information\n\nThe system has been powered off."
```
## TO DO:
- [ ] /help command - shows all commands the bot has
- [ ] /lr command - sends message when last time doorbell was pressed
- [ ] Add a way to use /setup command to get CHAT_ID by the bot and store it locally, so multiple people in a household can get the bot messages
- [ ] Add a way to get removed from the CHAT_ID list
- [W.I.P Branch](https://github.com/SimpliAj/PiBellBot/tree/multiple_chat_ids)

## Future Updates:
- TBC

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.
