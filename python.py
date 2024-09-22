import RPi.GPIO as GPIO
import time
import requests
import yaml

# Konfigurationsdatei laden
with open("config.yml", "r") as ymlfile:
    config = yaml.safe_load(ymlfile)

API_TOKEN = config['telegram']['api_token']
CHAT_ID = config['telegram']['chat_id']

def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{API_TOKEN}/sendMessage'
    data = {'chat_id': CHAT_ID, 'text': message}
    requests.post(url, data=data)

# GPIO Setup
GPIO.setmode(GPIO.BCM)  # Verwende BCM-Nummerierung
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # GPIO-Pin 17 als Eingang

# System gestartet Nachricht
print("System gestartet und bereit, Klingelsignale zu empfangen.")

try:
    while True:
        if GPIO.input(17) == GPIO.HIGH:  # Wenn der Pin auf High geht (Schaltkontakt geschlossen)
            print("Klingel gedrückt!")
            send_telegram_message("Jemand hat an der Tür geklingelt!")
            time.sleep(1)  # Verhindert mehrfaches Auslösen
        time.sleep(0.1)
except KeyboardInterrupt:
    print("\nProgramm wird beendet...")
finally:
    GPIO.cleanup()  # GPIO-Pins zurücksetzen
    print("GPIO-Pins zurückgesetzt.")
