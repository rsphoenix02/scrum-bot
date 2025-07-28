from sqlalchemy.orm import Session
from app import models
from uuid import uuid4


def get_channel_by_slack_id(db: Session, slack_id: str) -> models.Channel | None:
    return db.query(models.Channel).filter(models.Channel.slack_id == slack_id).first()


def create_channel(db: Session, slack_id: str) -> models.Channel:
    channel = models.Channel(slack_id=slack_id)
    db.add(channel)
    db.commit()
    db.refresh(channel)
    return channel
