from datetime import datetime
from pydantic import BaseModel, ConfigDict

class DocumentCreate(BaseModel):
    title: str
    filename: str

class DocumentUpdate(BaseModel):
    title: str | None = None
    filename: str | None = None

class DocumentResponse(BaseModel):
    id: int
    title: str
    filename: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
