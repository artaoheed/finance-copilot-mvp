# backend/routes/upload.py
from fastapi import APIRouter, UploadFile, File
import pandas as pd
import io

router = APIRouter(prefix="/upload", tags=["Upload"])

transactions_db = []  # temporary storage

@router.post("")
async def upload_file(file: UploadFile = File(...)):
    content = await file.read()
    df = pd.read_csv(io.BytesIO(content))
    transactions_db.clear()
    transactions_db.extend(df.to_dict(orient="records"))
    return {"status": "success", "rows_uploaded": len(transactions_db)}
