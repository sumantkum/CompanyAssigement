from pydantic import BaseModel
from typing import Optional, Any, Dict, List
from datetime import datetime


class FileBase(BaseModel):
    filename: str

class FileCreate(FileBase):
    pass

class FileUpdate(BaseModel):
    status: Optional[str] = None
    progress: Optional[float] = None
    parsed_data: Optional[Any] = None

class FileInDB(FileBase):
    id: str
    status: str
    progress: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class FileProgress(BaseModel):
    file_id: str
    status: str
    progress: float

class FileContent(BaseModel):
    data: Optional[Any] = None
    message: Optional[str] = None







