# backend/routes/forecast.py
from fastapi import APIRouter
from backend.routes.upload import transactions_db
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

router = APIRouter(prefix="/forecast", tags=["Forecast"])

@router.post("")
def forecast_spending():
    if not transactions_db:
        return {"error": "No transactions found."}

    df = pd.DataFrame(transactions_db)
    df["date"] = pd.to_datetime(df["date"])
    df = df.groupby(df["date"].dt.to_period("M")).sum().reset_index()
    df["month_idx"] = np.arange(len(df))

    model = LinearRegression()
    model.fit(df[["month_idx"]], df["amount"])

    next_month = len(df)
    forecast = model.predict([[next_month]])[0]

    return {
        "months": df["date"].astype(str).tolist(),
        "amounts": df["amount"].tolist(),
        "forecast_next_month": round(float(forecast), 2)
    }
