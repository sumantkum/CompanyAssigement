
from fastapi import FastAPI, Depends, HTTPException, status, UploadFile, File as FastAPIFile, BackgroundTasks
from models import FileModel 

from sqlalchemy.orm import Session
from typing import List
import os, shutil, asyncio

from database import get_db, Base, engine
import schemas, utils

Base.metadata.create_all(bind=engine)


app = FastAPI(title="File Parser API", description="API for uploading parsing and managing files")

async def process_file_background(file_id: str, file_path: str, db: Session):
    try:
        db_file = db.query(FileModel).filter(FileModel.id == file_id).first()
        if not db_file:
            return
        db_file.status = "processing"
        db_file.progress = 10.0
        db.commit()

        file_extension = os.path.splitext(file_path)[1].lower()
        parsed_data = await utils.parse_file(file_path, file_extension)
        
        db_file.parsed_data = parsed_data
        db_file.status = 'ready'
        db_file.progress = 100.0
        db.commit()

    except Exception as e:
        db_file.status = "failed"
        db.commit()
        print(f"Error processing file {file_id}:{str(e)}")


# file endPoints

@app.post("/files", response_model=schemas.FileInDB)
async def upload_file(
    background_tasks: BackgroundTasks,
    file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db)
):
    
    db_file = FileModel(filename=file.filename)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)

    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{db_file.id}_{file.filename}"
    await utils.save_upload_file(file, file_path)


    db_file.file_path = file_path
    db_file.progress = 50.0
    db.commit()

    background_tasks.add_task(process_file_background, db_file.id, file_path, db)
    return db_file

@app.get("/files/{file_id}/progress", response_model=schemas.FileProgress)
async def get_file_progress(
    file_id: str,
    db: Session = Depends(get_db)
):
    db_file= db.query(FileModel).filter(FileModel.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {
        "file_id": db_file.id,
        "status": db_file.status,
        "progress": db_file.progress
    }

@app.get("/files/{file_id}", response_model=schemas.FileContent)
async def get_file_content(
    file_id: str,
    db: Session = Depends(get_db)
):
    db_file = db.query(FileModel).filter(FileModel.id == file_id).first()
    if not db_file:
        raise HTTPException(status_code=404, detail="File not found")
    
    if db_file.status != "ready":
        return {"message": "File upload or processiing in progess. please try again later"}
    return {"date": db_file.parsed_data}


@app.get("/files", response_model=List[schemas.FileInDB])
async def list_files(db: Session = Depends(get_db)):
    return db.query(FileModel).all()

@app.delete("/files/{file_id}")
async def delete_file(file_id: str, db: Session = Depends(get_db)):

    db_file = db.query(FileModel).filter(FileModel.id == file_id).first()

    if not db_file:
        raise HTTPException(status_code=404, detail="File not Found")
    
    db.delete(db_file)
    db.commit()

    return {"Message": "File deleted Succssfully"}
    


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


