from sqlalchemy.orm import Session
from app import models
from app.schemas.user import UserCreate, UserUpdate
from uuid import uuid4
from datetime import datetime


def create_user(db: Session, user_in: UserCreate) -> models.User:
    user = models.User(
        id=uuid4(),
        slack_id=user_in.slack_id,
        name=user_in.name,
        created_at=datetime.utcnow(),
    )
    print("adding a user: ", user.id)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_user(db: Session, user_id) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_slack_id(db: Session, slack_id: str) -> models.User | None:
    return db.query(models.User).filter(models.User.slack_id == slack_id).first()



def get_all_users(db: Session):
    return db.query(models.User).all()


def update_user(db: Session, user_id, user_update: UserUpdate):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        return None
    for key, value in user_update.dict(exclude_unset=True).items():
        setattr(user, key, value)
    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        db.delete(user)
        db.commit()
    return user
