# Raspberry PI Doorbell to Telegram Message

# Requirements
    - Raspberry Pi

# Installation
    - Python
    - Install requirements

# Setup
    - Create a Telegram Bot via @BotFather and copy the bot api key to your config.yml
    - Open Telegram App on Phone/Desktop
        - Send a message to the Bot you created
    - Open in a Browser the API URL and insert your Bot API KEY
        - https://api.telegram.org/botAPI_KEY_HERE/getUpdates
    - Now you should see on the API URL somee messages copy the CHAT_ID you will need this for the config.yml
        - Now the bot know to which chat send messages
