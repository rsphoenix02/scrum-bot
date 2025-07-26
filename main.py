from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os

load_dotenv()
SLACK_API_TOKEN = os.getenv("SLACK_API_TOKEN")

app = FastAPI()

@app.post("/slack/events")
async def slack_events(request: Request):
    data = await request.json()

    # Slack verification challenge
    if "challenge" in data:
        return JSONResponse(content={"challenge": data["challenge"]})

    # Ignore bot's own messages
    if data.get("event", {}).get("bot_id"):
        return {"ok": True}

    # Handle user messages
    event = data.get("event", {})
    user = event.get("user")
    text = event.get("text")
    channel = event.get("channel")

    print(f"User {user} said: {text} in channel {channel}")

    return {"ok": True}
