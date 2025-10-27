# backend/routes/analyze.py
from fastapi import APIRouter
from backend.routes.upload import transactions_db
import pandas as pd
from statistics import mean
from pydantic import BaseModel

class AnalyzeRequest(BaseModel):
    transactions: list[dict]

router = APIRouter(prefix="/analyze", tags=["Analyze"])

@router.post("")
async def analyze_transactions(request: AnalyzeRequest):
    if not transactions_db:
        return {"error": "No transactions found."}

    df = pd.DataFrame(transactions_db)
    top_category = df.groupby("category")["amount"].sum().abs().idxmax()
    avg_spend = round(mean(df["amount"].abs()), 2)
    suggestion = f"You spend most in '{top_category}'. Try setting a weekly budget to cut {top_category} costs."

    return {
        "top_category": top_category,
        "average_spend": avg_spend,
        "suggestion": suggestion
    }
