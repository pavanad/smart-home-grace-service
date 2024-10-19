import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app import settings
from app.agent.service import GraceService
from app.models import QueryRequest

grace_service = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize FastAPI and load service
    """
    load_dotenv()
    grace_service["service"] = GraceService()

    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s %(levelname)s (%(name)s) %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
        filename="logs/grace_service.log",
        filemode="a",
    )
    grace_service["logger"] = logging.getLogger(__name__)
    yield
    grace_service.clear()


app = FastAPI(lifespan=lifespan, title=settings.TITLE, description=settings.DESCRIPTION)


@app.post("/query", summary=settings.QUERY_SUMMARY)
def query(request: QueryRequest):
    try:
        if request.chat_id is not None:
            os.environ["USER_CHAT_ID"] = str(request.chat_id)

        response = grace_service["service"].execute(request.message)
        return {"result": f"{response}"}
    except Exception as e:
        grace_service["logger"].error(str(e))
        raise HTTPException(status_code=500, detail=str(e))
