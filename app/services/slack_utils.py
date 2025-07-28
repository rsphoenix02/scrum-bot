import os
import requests
from dotenv import load_dotenv

load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

def send_slack_message(channel, text):
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-type": "application/json"
    }
    
    payload = {
        "channel": channel,
        "text": text
    }
    response = requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=payload)
    if not response.ok or not response.json().get("ok", False):
        print("Slack postMessage failed:", response.text)
    return response

