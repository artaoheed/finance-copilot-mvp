# backend/routes/analyze.py
from fastapi import APIRouter
from backend.routes.upload import transactions_db
from backend.ai.llm_client import analyze_transactions_with_llm
import pandas as pd
from statistics import mean
from backend.utils.logger import logger

router = APIRouter(prefix="/analyze", tags=["Analyze"])


@router.post("")
async def analyze_transactions():
    """
    Analyze transactions using LLM (Gemini/OpenAI/Claude).
    Falls back to local summary if LLM fails.
    """
    if not transactions_db:
        return {"error": "No transactions found."}

    try:
        # --- Step 1: Run through AI analysis ---
        llm_result = analyze_transactions_with_llm(transactions_db)

        if "error" not in llm_result:
            return {
                "status": "success",
                "analysis_source": "LLM",
                "results": llm_result
            }

        # --- Step 2: If AI fails, use fallback ---
        else:
            df = pd.DataFrame(transactions_db)
            top_category = df.groupby("category")["amount"].sum().abs().idxmax()
            avg_spend = round(mean(df["amount"].abs()), 2)
            suggestion = f"You spend most in '{top_category}'. Try setting a weekly budget to cut {top_category} costs."

            return {
                "status": "success",
                "analysis_source": "Fallback",
                "results": {
                    "top_categories": [{"category": top_category, "total": avg_spend}],
                    "advice": suggestion,
                    "summary": f"Average spend per transaction is ${avg_spend}."
                }
            }

    except Exception as e:
        return {"error": f"Analysis failed: {str(e)}"}



@router.post("")
async def analyze_transactions():
    if not transactions_db:
        logger.warning("⚠️ No transactions found for analysis.")
        return {"error": "No transactions found."}

    try:
        logger.info(f"Starting AI analysis on {len(transactions_db)} transactions.")
        llm_result = analyze_transactions_with_llm(transactions_db)

        if "error" not in llm_result:
            logger.info("✅ LLM analysis completed successfully.")
            return {
                "status": "success",
                "analysis_source": "LLM",
                "results": llm_result
            }
        else:
            logger.warning("LLM failed — switching to fallback analysis.")
            ...
    except Exception as e:
        logger.error(f"❌ Analysis failed: {str(e)}")
        return {"error": f"Analysis failed: {str(e)}"}
