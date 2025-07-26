import os
import requests

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

def send_slack_message(channel, text):
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "channel": channel,
        "text": text
    }
    response = requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=payload)
    return response.json()
