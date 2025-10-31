# backend/routes/upload.py
from fastapi import APIRouter, UploadFile, File
import pandas as pd
from io import StringIO
from backend.utils.logger import logger
from backend.utils.privacy import sanitize_dataframe


router = APIRouter(prefix="/upload", tags=["Upload"])

# This is our in-memory "database"
transactions_db = []

@router.post("")
async def upload_transactions(file: UploadFile = File(...)):
    """
    Accepts a CSV upload, parses it into JSON, and stores it in memory.
    """
    try:
        content = await file.read()
        df = pd.read_csv(StringIO(content.decode("utf-8")))
        records = df.to_dict(orient="records")

        global transactions_db
        transactions_db.clear()
        transactions_db.extend(records)

        return {"status": "success", "rows_uploaded": len(records)}

    except Exception as e:
        return {"error": f"Failed to process file: {e}"}


@router.post("")
async def upload_transactions(file: UploadFile = File(...)):
    try:
        logger.info("Starting CSV upload process...")
        content = await file.read()
        df = pd.read_csv(StringIO(content.decode("utf-8")))
        records = df.to_dict(orient="records")

        global transactions_db
        transactions_db.clear()
        transactions_db.extend(records)

        logger.info(f"✅ Uploaded {len(records)} transactions successfully.")
        return {"status": "success", "rows_uploaded": len(records)}

    except Exception as e:
        logger.error(f"❌ Upload failed: {str(e)}")
        return {"error": f"Failed to process file: {e}"}

@router.post("")
async def upload_transactions(file: UploadFile = File(...)):
    df = pd.read_csv(file.file)
    
    # ✅ Sanitize sensitive text columns
    df = sanitize_dataframe(df)
    
    # Store in memory
    transactions_db.clear()
    transactions_db.extend(df.to_dict(orient="records"))

    logger.info(f"Uploaded {len(df)} sanitized transactions.")
    return {"status": "success", "rows_uploaded": len(df)}