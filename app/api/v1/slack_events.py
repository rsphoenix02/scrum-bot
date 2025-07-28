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
from app.services import user as user_service
from app.services import channel as channel_service
from app.schemas.user import UserCreate



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
    user = user_service.get_user_by_slack_id(db, user_id)
    channel = channel_service.get_channel_by_slack_id(db, channel_id)
    
    if not user:
        user_in = UserCreate(slack_id=user_id, name=None)
        user = user_service.create_user(db, user_in)

    if not channel:
        channel = channel_service.create_channel(db, channel_id)

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