import pandas as pd
from models import forecast

def test_forecast_output_structure():
    df = pd.read_csv("data/sample_transactions.csv")
    result = forecast.get_forecast(df, method="rolling") # using rolling method for this test
    
    assert "predicted_next_month_amount" in result
    assert isinstance(result["predicted_next_month_amount"], float)
    assert len(result["historical_months"]) == len(result["historical_amounts"])
    assert result["predicted_next_month_amount"] > 0
