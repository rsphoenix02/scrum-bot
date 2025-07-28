from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

from app.api.v1 import user, slack_events, standup



app = FastAPI()

# Base.metadata.create_all(bind=engine)

app.include_router(slack_events.router)
app.include_router(standup.router)
app.include_router(user.router)