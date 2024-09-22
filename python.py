import RPi.GPIO as GPIO
import time
import requests
import yaml

# Load configuration file
with open("config.yml", "r") as ymlfile:
    config = yaml.safe_load(ymlfile)

API_TOKEN = config['telegram']['api_token']
CHAT_ID = config['telegram']['chat_id']

# Load both print and Telegram messages from the configuration
print_messages = config['print_messages']
telegram_messages = config['telegram_messages']

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print(f"Telegram message sent: {message}")
    else:
        print(f"Failed to send Telegram message. Status code: {response.status_code}")

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Print start message and send start Telegram message
print(print_messages['system_start'])
send_telegram_message(telegram_messages['system_start'])

try:
    while True:
        if GPIO.input(17) == GPIO.HIGH:
            print(print_messages['doorbell_ring'])
            send_telegram_message(telegram_messages['doorbell_ring'])
            time.sleep(1)  # Prevent multiple triggers
        time.sleep(0.1)
except KeyboardInterrupt:
    print(print_messages['system_shutdown'])
    send_telegram_message(telegram_messages['system_shutdown'])
finally:
    GPIO.cleanup()
    print(print_messages['gpio_cleanup'])
    send_telegram_message(telegram_messages['gpio_cleanup'])
