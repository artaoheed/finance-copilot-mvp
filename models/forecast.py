# models/forecast.py
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import os

def prepare_monthly_data(transactions_df: pd.DataFrame):
    """
    Aggregate transactions by month.
    Ensures clean 'date' and numeric 'amount' columns.
    """
    df = transactions_df.copy()

    # Ensure 'date' column exists
    if "date" not in df.columns:
        raise ValueError("❌ Missing 'date' column in transactions data.")

    # Ensure 'amount' column exists (case-insensitive check)
    amount_col = next((c for c in df.columns if c.lower() == "amount"), None)
    if not amount_col:
        raise ValueError(f"❌ No 'amount' column found. Columns: {df.columns.tolist()}")

    # Convert data types safely
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df[amount_col] = pd.to_numeric(df[amount_col], errors="coerce")
    df = df.dropna(subset=["date", amount_col])

    # Group by month
    monthly = (
        df.groupby(df["date"].dt.to_period("M"))[amount_col]
        .sum()
        .reset_index()
    )
    monthly["month"] = monthly["date"].dt.to_timestamp()
    monthly["month_idx"] = np.arange(len(monthly))

    return monthly[["month", amount_col, "month_idx"]].rename(columns={amount_col: "amount"})

def forecast_rolling_trend(monthly_df: pd.DataFrame, window: int = 3):
    """
    Forecast next month's spending using rolling average + linear trend.
    """
    if monthly_df.empty:
        raise ValueError("No data available for forecasting.")
    rolling_avg = monthly_df["amount"].rolling(window=window, min_periods=1).mean()
    trend = monthly_df["amount"].diff().fillna(0).mean()
    forecast = rolling_avg.iloc[-1] + trend
    return round(float(forecast), 2)

def forecast_linear_regression(monthly_df: pd.DataFrame):
    """
    Forecast next month's spending using LinearRegression.
    """
    if monthly_df.shape[0] < 2:
        raise ValueError("Need at least 2 months of data for linear regression.")
    model = LinearRegression()
    X = monthly_df[["month_idx"]]
    y = monthly_df["amount"]
    model.fit(X, y)
    next_month_idx = np.array([[monthly_df["month_idx"].iloc[-1] + 1]])
    forecast = model.predict(next_month_idx)[0]
    return round(float(forecast), 2)

def get_forecast(transactions_df: pd.DataFrame, method: str = "rolling"):
    """
    Return forecast and historical months & amounts.
    method: "rolling" or "linear"
    """
    monthly = prepare_monthly_data(transactions_df)

    if method == "rolling":
        forecast_value = forecast_rolling_trend(monthly)
    elif method == "linear":
        forecast_value = forecast_linear_regression(monthly)
    else:
        raise ValueError("Invalid method. Choose 'rolling' or 'linear'.")

    historical_months = monthly["month"].dt.strftime("%Y-%m").tolist()
    historical_amounts = monthly["amount"].tolist()

    return {
        "predicted_next_month_amount": forecast_value,
        "historical_months": historical_months,
        "historical_amounts": historical_amounts
    }

# Example usage
if __name__ == "__main__":
    path = "data/sample_transactions.csv"
    if not os.path.exists(path):
        raise FileNotFoundError(f"❌ File not found: {path}")

    df = pd.read_csv(path)
    forecast_result = get_forecast(df, method="rolling")
    print("Rolling forecast:", forecast_result)

    forecast_result_linear = get_forecast(df, method="linear")
    print("Linear forecast:", forecast_result_linear)
