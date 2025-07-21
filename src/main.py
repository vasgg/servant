from fastapi import FastAPI
import logging

from src.config import get_settings
from src.routers.blink1 import router as blink1_router
from src.helpers import setup_logs

app = FastAPI()
setup_logs("servant")
settings = get_settings()

app.include_router(blink1_router, prefix="/blink")

@app.get("/health")
async def health_check():
    return {"status": "ok"}

logging.info("servant started")
