import asyncio
import logging

from oauth2client.service_account import ServiceAccountCredentials
import gspread
from fastapi import APIRouter

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/update/{cell}/{value}")
async def update_google_sheet(cell: str, value: int):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']

    credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
    client = gspread.authorize(credentials)

    spreadsheet = client.open("users_counter")
    worksheet = spreadsheet.sheet1

    await asyncio.to_thread(worksheet.update, cell, [[value]])
    logger.info(f'Users counter updated. Cell: {cell} Value: {value}')
    return {"message": f'Users counter updated. Cell: {cell} Value: {value}'}
