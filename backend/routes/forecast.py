# backend/routes/forecast.py

from backend.utils.logger import logger
from fastapi import APIRouter, Query
from backend.routes.upload import transactions_db
from models import forecast  # Import your forecast module
import pandas as pd

router = APIRouter(prefix="/forecast", tags=["Forecast"])

@router.get("")
def get_forecast_endpoint(method: str = Query("rolling", enum=["rolling", "linear"])):
    """
    Forecast next month's spending.
    - method: "rolling" (default) or "linear"

    Returns:
        predicted_next_month_amount, historical_months, historical_amounts
    """
    if not transactions_db:
        return {"error": "No transactions found."}

    try:
        # ✅ Convert the in-memory list of dicts to a DataFrame
        df = pd.DataFrame(transactions_db)

        # ✅ Run forecast
        result = forecast.get_forecast(
            transactions_df=df,
            method=method
        )

        return {
            "status": "success",
            "method": method,
            **result
        }

    except Exception as e:
        return {"error": f"Forecasting failed: {str(e)}"}


@router.get("")
def get_forecast_endpoint(method: str = Query("rolling", enum=["rolling", "linear"])):
    if not transactions_db:
        logger.warning("⚠️ No transactions found for forecasting.")
        return {"error": "No transactions found."}

    try:
        logger.info(f"Running forecast using method='{method}' on {len(transactions_db)} records.")
        result = forecast.get_forecast(transactions_df=transactions_db, method=method)
        logger.info(f"✅ Forecast completed. Next month prediction: {result['predicted_next_month_amount']}")
        return {"status": "success", "method": method, **result}
    except Exception as e:
        logger.error(f"❌ Forecasting failed: {str(e)}")
        return {"error": f"Forecasting failed: {str(e)}"}
