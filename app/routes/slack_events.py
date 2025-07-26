from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.standup import StandupEntry
from app.models.user import User
from datetime import datetime
from app.services.slack_utils import send_slack_message
import os
import requests


router = APIRouter()

@router.post("/slack/events")
async def slack_events(request: Request, db: Session = Depends(get_db)):
    data = await request.json()

    if "challenge" in data:
        return {"challenge": data["challenge"]}

    event = data.get("event", {})
    if event.get("bot_id"):
        return {"ok": True}

    text = event.get("text")
    user_id = event.get("user")
    channel_id = event.get("channel")

    if not user_id or not text:
        return {"ok": True}

    # ✅ Check if user exists in the DB
    user = db.query(User).filter(User.slack_id == user_id).first()
    if not user:
        # Insert new user
        user = User(slack_id=user_id, name=None, created_at=datetime.utcnow())
        db.add(user)
        db.commit()
        print(f"🟢 New user added: {user_id}")

    # ✅ Proceed with standup entry parsing
    if text.startswith("yesterday:") and "today:" in text and "blockers:" in text:
        try:
            _, y = text.split("yesterday:")
            y, t = y.split("today:")
            t, b = t.split("blockers:")
            entry = StandupEntry(
                user_id=user_id,
                channel_id=channel_id,
                yesterday=y.strip(),
                today=t.strip(),
                blockers=b.strip()
            )
            db.add(entry)
            db.commit()
            # send_slack_message(channel_id, "✅ Thanks! Your standup has been saved.")
            print(f"✅ Standup saved for user {user_id}")


            SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

            headers = {
                "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
                "Content-type": "application/json"
            }

            payload = {
                "channel": channel_id,
                "text": f"✅ Thanks <@{user_id}>! Your standup has been recorded."
            }

            response = requests.post("https://slack.com/api/chat.postMessage", headers=headers, json=payload)

            if not response.ok:
                print("Slack postMessage failed:", response.text)



            return {"ok": True, "msg": "Standup recorded!"}
        except Exception as e:
            print("❌ Parse error:", e)

    return {"ok": True}