from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.standup import StandupEntry
from app.models.user import User
from app.models.channel import Channel
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
    channel = db.query(Channel).filter(Channel.slack_id == channel_id).first()
    
    if not user:
        # Insert new user
        user = User(slack_id=user_id, name=None, created_at=datetime.utcnow())
        db.add(user)
        db.commit()
        print(f"🟢 New user added: {user_id}")

    if not channel:
        channel = Channel(slack_id=channel_id)
        db.add(channel)
        db.commit()
        db.refresh(channel)

    # ✅ Proceed with standup entry parsing
    if text.startswith("yesterday:") and "today:" in text and "blockers:" in text:
        try:
            _, y = text.split("yesterday:")
            y, t = y.split("today:")
            t, b = t.split("blockers:")
            entry = StandupEntry(
                user_id=user.id,
                channel_id=channel.id,
                yesterday=y.strip(),
                today=t.strip(),
                blockers=b.strip()
            )
            db.add(entry)

            db.commit()
            
            response = send_slack_message(channel_id, f"✅ Thanks <@{user_id}>! Your standup has been recorded.")
            print(f"✅ Standup saved for user {user_id}")

            return {"ok": True, "msg": "Standup recorded!"}
        except Exception as e:
            print("❌ Parse error:", e)

    return {"ok": True}