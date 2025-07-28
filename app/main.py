from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
from app.db.base import Base
from app.db.engine import engine
from app.models import user, standup
from app.routes import slack_events
from app.routes import standup

load_dotenv()

app = FastAPI()

# Base.metadata.create_all(bind=engine)

app.include_router(slack_events.router)
app.include_router(standup.router)
