from sqlalchemy import Column, Integer, String, DateTime, Text, Float
from sqlalchemy.dialects.sqlite import JSON
from database import Base
from datetime import datetime
import uuid

def generate_uuid():
    return str(uuid.uuid4())

class FileModel(Base):
    __tablename__ = 'files'

    id = Column(String, primary_key=True, default=generate_uuid)
    filename = Column(String, nullable=False)
    status = Column(String, default="uploading")

    progress = Column(Float, default=0.0)
    file_path = Column(String)
    parsed_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)






