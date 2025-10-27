import numpy as np

def forecast_next_month_spending(monthly_totals):
    """
    monthly_totals: list or array of monthly totals (floats), oldest -> newest
    Returns a simple linear-fit prediction for the next time step.
    """
    if not monthly_totals:
        return 0.0
    y = np.array(monthly_totals, dtype=float)
    x = np.arange(len(y))
    if len(y) == 1:
        return float(y[-1])
    coef = np.polyfit(x, y, 1)
    pred = float(np.polyval(coef, len(y)))
    return max(pred, 0.0)
