import RPi.GPIO as GPIO
import time
import requests
import yaml
from datetime import datetime

# Load configuration file
with open("config.yml", "r") as ymlfile:
    config = yaml.safe_load(ymlfile)

API_TOKEN = config['telegram']['api_token']
CHAT_ID = config['telegram']['chat_id']

# Load both print and Telegram messages from the configuration
print_messages = config['print_messages']
telegram_messages = config['telegram_messages']

# Load GPIO pin number from config
gpio_pin = config['settings'].get('gpio_pin', 17)  # Default to pin 17 if not set

# Check if command-line prints are enabled
enable_cmd_prints = config['settings'].get('enable_cmd_prints', True)  # Default to True if not set
log_telegram_send = config['settings'].get('log_telegram_send', True)  # Default to True if not set

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    response = requests.post(url, data=data)
    
    if log_telegram_send:
        if response.status_code == 200:
            print(f"Telegram message sent: {message}")
        else:
            print(f"Failed to send Telegram message. Status code: {response.status_code}")

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # Use GPIO pin from config

# Print start message and send start Telegram message
if enable_cmd_prints:
    print(print_messages['system_start_print'])
send_telegram_message(telegram_messages['system_start'])

try:
    while True:
        if GPIO.input(gpio_pin) == GPIO.HIGH:
            if enable_cmd_prints:
                print(print_messages['doorbell_ring_print'])
            send_telegram_message(telegram_messages['doorbell_ring'])
            time.sleep(1)  # Prevent multiple triggers
        time.sleep(0.1)
except KeyboardInterrupt:
    if enable_cmd_prints:
        print(print_messages['system_shutdown_print'])
    send_telegram_message(telegram_messages['system_shutdown'])
finally:
    GPIO.cleanup()
    if enable_cmd_prints:
        print(print_messages['gpio_cleanup_print'])
    send_telegram_message(telegram_messages['gpio_cleanup'])
