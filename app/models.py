from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    message: str
    temperature: float = Field(default=0.1, ge=0.0, le=1.0)
