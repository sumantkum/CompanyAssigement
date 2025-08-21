import os, aiofiles
import pandas as pd, pdfplumber
from fastapi import UploadFile, HTTPException
import json
from typing import Dict, Any


async def save_upload_file(upload_file: UploadFile, destination: str)->None:
    try:
        async with aiofiles.open(destination, 'wb') as f:
            while content := await upload_file.read(1024*1024):
                await f.write(content)
    except Exception as a:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")
    
async def parse_file(file_path: str, file_extension: str) -> Dict[str, Any]:
    
    try:            
        if file_extension == '.csv':
            df = pd.read_csv(file_path)
            return df.to_dict(orient= 'records')
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file_path)
            return df.to_dict(orient='records')
        
        elif file_extension == '.pdf':
            text_content = []
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    text = page.extract_text()
                    if text:
                        text_content.append(text)
            return {"text": text_content}
        else:
            async with aiofiles.open(file_path, 'r') as f:
                content = await f.read()
            return {"content": content}

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error parsing file: {str(e)}"
        )

