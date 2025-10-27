import numpy as np

def forecast_next_month_spending(monthly_totals): 
    """
    monthly_totals: list or array of monthly totals (floats), oldest -> newest
    Returns a simple linear-fit prediction for the next time step.
    """
    if not monthly_totals:
        return 0.0
    y = np.array(monthly_totals, dtype=float) # Convert to numpy array
    x = np.arange(len(y)) # Time indices
    if len(y) == 1: # If there is only one data point
        return float(y[-1]) # Return the same value
    coef = np.polyfit(x, y, 1) # Fit linear model
    pred = float(np.polyval(coef, len(y))) # Predict next month
    return max(pred, 0.0) 
