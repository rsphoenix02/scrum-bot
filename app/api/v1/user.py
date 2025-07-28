from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas import user as schemas
from app.services import user as services
from app.db.session import get_db
from uuid import UUID

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=schemas.UserOut)
def create(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    return services.create_user(db, user_in)


@router.get("/{user_id}", response_model=schemas.UserOut)
def read(user_id: UUID, db: Session = Depends(get_db)):
    user = services.get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.get("/", response_model=list[schemas.UserOut])
def read_all(db: Session = Depends(get_db)):
    return services.get_all_users(db)


@router.put("/{user_id}", response_model=schemas.UserOut)
def update(user_id: UUID, user_update: schemas.UserUpdate, db: Session = Depends(get_db)):
    user = services.update_user(db, user_id, user_update)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.delete("/{user_id}", response_model=schemas.UserOut)
def delete(user_id: UUID, db: Session = Depends(get_db)):
    user = services.delete_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
