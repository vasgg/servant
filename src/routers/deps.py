import secrets

from fastapi import Depends
from fastapi.security import HTTPBasicCredentials
from starlette import status
from starlette.exceptions import HTTPException

from main import security, settings


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
