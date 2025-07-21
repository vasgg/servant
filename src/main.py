import secrets

from fastapi import Depends, FastAPI
import logging

from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from starlette.exceptions import HTTPException

from src.config import get_settings
from src.routers.blink1 import router as blink1_router
from src.helpers import setup_logs

app = FastAPI()
setup_logs("servant")
security = HTTPBasic()
settings = get_settings()


def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username, settings.ngrok.USER.get_secret_value()
    )
    correct_password = secrets.compare_digest(
        credentials.password, settings.ngrok.PASS.get_secret_value()
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


app.include_router(blink1_router, prefix="/blink")
logging.info("servant started")
