from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.models.standup import StandupEntry
from app.models.user import User

router = APIRouter()

@router.get("/standups/latest")
def get_latest_standups(db: Session = Depends(get_db)):
    entries = (
        db.query(StandupEntry)
        .order_by(StandupEntry.created_at.desc())
        .limit(10)
        .all()
    )

    response = []
    for entry in entries:
        user = db.query(User).filter(User.slack_id == entry.user_id).first()
        response.append({
            "user": user.name or user.slack_id,
            "yesterday": entry.yesterday,
            "today": entry.today,
            "blockers": entry.blockers,
            "time": entry.created_at.isoformat()
        })

    return {"entries": response}
