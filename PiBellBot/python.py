import RPi.GPIO as GPIO
import time
import requests
import yaml
from discord import Client
from datetime import datetime

# Load configuration file
with open("config.yml", "r") as ymlfile:
    config = yaml.safe_load(ymlfile)

# Telegram configuration
telegram_enabled = config['telegram']['enabled']
telegram_token = config['telegram'].get('api_token')
telegram_chat_id = config['telegram'].get('chat_id')

# Discord configuration
discord_enabled = config['discord']['enabled']
discord_token = config['discord'].get('bot_token')
discord_channel_id = config['discord'].get('channel_id')

# Load both print, Telegram, and Discord messages from the configuration
print_messages = config['print_messages']
telegram_messages = config['telegram_messages']
discord_messages = config['discord_messages']

# Load GPIO pin number from config
gpio_pin = config['settings'].get('gpio_pin', 17)  # Default to pin 17 if not set

# Check if command-line prints are enabled
enable_cmd_prints = config['settings'].get('enable_cmd_prints', True)
log_message_send = config['settings'].get('log_message_send', True)

# Define Telegram message sender
def send_telegram_message(message):
    if telegram_enabled:
        url = f'https://api.telegram.org/bot{telegram_token}/sendMessage'
        data = {'chat_id': telegram_chat_id, 'text': message}
        response = requests.post(url, data=data)

        if log_message_send:
            if response.status_code == 200:
                print(f"Telegram message sent: {message}")
            else:
                print(f"Failed to send Telegram message. Status code: {response.status_code}")

# Define Discord message sender
class DiscordBot(Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')
    
    async def send_message(self, message):
        if discord_enabled:
            channel = self.get_channel(int(discord_channel_id))
            if channel:
                await channel.send(message)
                if log_message_send:
                    print(f"Discord message sent: {message}")
            else:
                print("Failed to find Discord channel.")

discord_client = DiscordBot()

def send_discord_message(message):
    if discord_enabled:
        discord_client.loop.create_task(discord_client.send_message(message))

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Start message
if enable_cmd_prints:
    print(print_messages['system_start_print'])
send_telegram_message(telegram_messages['system_start'])
send_discord_message(discord_messages['system_start'])

try:
    discord_client.run(discord_token)
    
    while True:
        if GPIO.input(gpio_pin) == GPIO.HIGH:
            if enable_cmd_prints:
                print(print_messages['doorbell_ring_print'])
            send_telegram_message(telegram_messages['doorbell_ring'])
            send_discord_message(discord_messages['doorbell_ring'])
            time.sleep(1)
        time.sleep(0.1)
except KeyboardInterrupt:
    if enable_cmd_prints:
        print(print_messages['system_shutdown_print'])
    send_telegram_message(telegram_messages['system_shutdown'])
    send_discord_message(discord_messages['system_shutdown'])
finally:
    GPIO.cleanup()
    if enable_cmd_prints:
        print(print_messages['gpio_cleanup_print'])
    send_telegram_message(telegram_messages['gpio_cleanup'])
    send_discord_message(discord_messages['gpio_cleanup'])
