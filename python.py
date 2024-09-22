import RPi.GPIO as GPIO
import time
import requests
import yaml
import json

# Load configuration file
with open("config.yml", "r") as ymlfile:
    config = yaml.safe_load(ymlfile)

API_TOKEN = config['telegram']['api_token']

# Load messages from the configuration
telegram_messages = config['telegram_messages']

# Chat-IDs speichern
def save_chat_id(chat_id):
    try:
        with open('chat_ids.json', 'r') as file:
            chat_ids = json.load(file)
    except FileNotFoundError:
        chat_ids = []

    if chat_id not in chat_ids:
        chat_ids.append(chat_id)
        with open('chat_ids.json', 'w') as file:
            json.dump(chat_ids, file)
        print(f"Neue Chat-ID gespeichert: {chat_id}")
    else:
        print(f"Chat-ID {chat_id} bereits gespeichert.")

# Alle Chat-IDs laden
def load_chat_ids():
    try:
        with open('chat_ids.json', 'r') as file:
            chat_ids = json.load(file)
        return chat_ids
    except FileNotFoundError:
        return []

# Telegram Nachricht senden
def send_telegram_message(message):
    chat_ids = load_chat_ids()
    current_time = time.strftime('%Y-%m-%d %H:%M:%S')
    message_with_time = f"{message}\n\n📅 Datum und Uhrzeit: {current_time}"
    
    for chat_id in chat_ids:
        url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
        data = {'chat_id': chat_id, 'text': message_with_time}
        response = requests.post(url, data=data)
        if response.status_code == 200:
            print(f"Telegram Nachricht an {chat_id} gesendet: {message_with_time}")
        else:
            print(f"Fehler beim Senden der Nachricht an {chat_id}: {response.status_code}")

# Neue Chat-IDs automatisch speichern, wenn Nutzer eine Nachricht senden
def check_for_new_users():
    url = f'https://api.telegram.org/bot{API_TOKEN}/getUpdates'
    response = requests.get(url)
    updates = response.json()

    for update in updates['result']:
        if 'message' in update:
            chat_id = update['message']['chat']['id']
            save_chat_id(chat_id)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Überprüfe regelmäßig neue Benutzer und speichere deren Chat-IDs
check_for_new_users()

# Nachricht beim Starten des Systems senden
send_telegram_message(telegram_messages['system_start'])

try:
    while True:
        if GPIO.input(17) == GPIO.HIGH:
            print(telegram_messages['doorbell_ring'])
            send_telegram_message(telegram_messages['doorbell_ring'])
            time.sleep(1)  # Prevent multiple triggers
        time.sleep(0.1)
except KeyboardInterrupt:
    send_telegram_message(telegram_messages['system_shutdown'])
finally:
    GPIO.cleanup()
    send_telegram_message(telegram_messages['gpio_cleanup'])
