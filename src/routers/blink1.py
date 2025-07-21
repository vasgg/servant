import asyncio
import logging

from fastapi import APIRouter, HTTPException
from starlette import status

from src.enums import Color

router = APIRouter()
logger = logging.getLogger(__name__)


async def run_blink1_tool(*args):
    try:
        process = await asyncio.create_subprocess_exec(
            "blink1-tool",
            *args,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await process.communicate()
        if process.returncode != 0:
            logger.error(
                f"Error running blink1-tool {' '.join(args)}: {stderr.decode()}"
            )
            raise HTTPException(
                status_code=500, detail=f"Error running blink1-tool: {stderr.decode()}"
            )
        return stdout.decode(), stderr.decode()
    except Exception as e:
        logger.exception("Exception occurred while running blink1-tool")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{color}", status_code=status.HTTP_200_OK)
async def blink_color(color: Color):
    await run_blink1_tool(f"--{color}")
    await asyncio.sleep(1)
    await run_blink1_tool("--off")
    return {"message": f"Blink1 set to {color} and then turned off"}
