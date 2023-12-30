from fastapi import FastAPI, Depends
from api import notification

app = FastAPI()

app.include_router(notification.router)