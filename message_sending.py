import requests
import dotenv
import os

dotenv.load_dotenv()

bottoken = os.getenv("BOT_TOKEN")

message_url = f"https://api.telegram.org/{bottoken}/sendMessage"

headers = {
    "accept": "application/json",
    "User-Agent": "Telegram Bot SDK - (https://github.com/irazasyed/telegram-bot-sdk)",
    "content-type": "image/png"
}

def send_message(message):
    payload = {
    "chat_id": "@weather845173",
    "text":message,
    "caption": "Optional",
    "disable_notification": False,
    "reply_to_message_id": None
    }
    response = requests.post(message_url, data=payload)

    print(response.content)

if __name__ == "__main__":
    send_message("test")