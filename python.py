import RPi.GPIO as GPIO
import time
import requests
import yaml

# Konfigurationsdatei laden
with open("config.yml", "r") as ymlfile:
    config = yaml.safe_load(ymlfile)

API_TOKEN = config['telegram']['api_token']
CHAT_ID = config['telegram']['chat_id']

# Nachrichten aus der Konfiguration laden
messages = config['messages']

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print(f"Nachricht erfolgreich gesendet: {message}")
    else:
        print(f"Fehler beim Senden der Nachricht: {response.status_code}")

# GPIO Setup
GPIO.setmode(GPIO.BCM)  # Verwende BCM-Nummerierung
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # GPIO-Pin 17 als Eingang

# System gestartet Nachricht
print(messages['system_start'])
send_telegram_message(messages['system_start'])

try:
    while True:
        if GPIO.input(17) == GPIO.HIGH:  # Wenn der Pin auf High geht (Schaltkontakt geschlossen)
            print(messages['doorbell_ring'])
            send_telegram_message(messages['doorbell_ring'])
            time.sleep(1)  # Verhindert mehrfaches Auslösen
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nProgramm wird beendet...")
    send_telegram_message(messages['system_shutdown'])
finally:
    GPIO.cleanup()  # GPIO-Pins zurücksetzen
    print(messages['gpio_cleanup'])
    send_telegram_message(messages['gpio_cleanup'])
