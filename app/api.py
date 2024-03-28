from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

from app import settings
from app.models import QueryRequest

# from app.services.agent import create_agent

grace_assistant = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Initialize FastAPI and load model
    """
    load_dotenv()
    grace_assistant["agent"] = None
    yield
    grace_assistant.clear()


app = FastAPI(lifespan=lifespan, title=settings.TITLE, description=settings.DESCRIPTION)


@app.post("/query", summary=settings.QUERY_SUMMARY)
def query(request: QueryRequest):
    try:
        response = ""
        # response = grace_assistant["agent"]({"input": request.message})["output"]
        return {"result": f"{response}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
