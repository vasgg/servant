import asyncio
import logging

from oauth2client.service_account import ServiceAccountCredentials
import gspread
from fastapi import APIRouter, HTTPException
from starlette import status

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/update/{cell}/{value}")
async def update_google_sheet(cell: str, value: int):
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive",
    ]
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            "credentials.json", scope
        )
        client = gspread.authorize(credentials)
        spreadsheet = client.open("users_counter")
        worksheet = spreadsheet.sheet1
        await asyncio.to_thread(worksheet.update, cell, [[value]])
        logger.info(f"Users counter updated. Cell: {cell} Value: {value}")
        return {"message": f"Users counter updated. Cell: {cell} Value: {value}"}
    except gspread.exceptions.APIError as e:
        logger.error(f"Google Sheets API error: {e}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Google Sheets API error: {e}",
        )
    except Exception as e:
        logger.exception(f"Unhandled error updating Google Sheet: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating Google Sheet: {e}",
        )
