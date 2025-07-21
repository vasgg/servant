from fastapi import FastAPI
import logging
from routers.blink1 import router as blink1_router
from helpers import setup_logs

app = FastAPI()
setup_logs("servant")

app.include_router(blink1_router, prefix="/blink")
logging.info("servant started")
