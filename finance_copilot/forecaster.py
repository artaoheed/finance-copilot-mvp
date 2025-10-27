"""
Spending forecasting module using simple time-series analysis.
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
import numpy as np
import pandas as pd
from .transaction import Transaction, TransactionType, TransactionCategory


class SpendingForecaster:
    """
    Forecasts future spending based on historical transaction patterns.
    """
    
    def __init__(self, transactions: List[Transaction]):
        """
        Initialize forecaster with transaction history.
        
        Args:
            transactions: List of Transaction objects
        """
        self.transactions = transactions
        self._df = self._to_dataframe()
    
    def _to_dataframe(self) -> pd.DataFrame:
        """Convert transactions to pandas DataFrame."""
        if not self.transactions:
            return pd.DataFrame()
        
        data = [t.to_dict() for t in self.transactions]
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        return df
    
    def forecast_monthly_spending(self, months: int = 1) -> Dict[str, float]:
        """
        Forecast total spending for the next N months.
        
        Args:
            months: Number of months to forecast
            
        Returns:
            Dictionary with forecast details
        """
        if self._df.empty:
            return {
                'forecast_amount': 0.0,
                'daily_average': 0.0,
                'months': months,
                'confidence': 'low',
                'method': 'average',
            }
        
        debits = self._df[self._df['type'] == TransactionType.DEBIT.value]
        
        if debits.empty:
            return {
                'forecast_amount': 0.0,
                'daily_average': 0.0,
                'months': months,
                'confidence': 'low',
                'method': 'average',
            }
        
        # Calculate daily average spending
        date_range = (debits['date'].max() - debits['date'].min()).days
        if date_range < 1:
            date_range = 1
        
        total_spent = debits['amount'].sum()
        daily_avg = total_spent / date_range
        
        # Forecast for next N months (assuming 30 days per month)
        forecast_amount = daily_avg * 30 * months
        
        # Determine confidence based on data availability
        confidence = 'high' if len(debits) > 50 else 'medium' if len(debits) > 20 else 'low'
        
        return {
            'forecast_amount': float(forecast_amount),
            'daily_average': float(daily_avg),
            'months': months,
            'confidence': confidence,
            'method': 'daily_average',
        }
    
    def forecast_category_spending(self, days: int = 30) -> Dict[str, float]:
        """
        Forecast spending by category for the next N days.
        
        Args:
            days: Number of days to forecast
            
        Returns:
            Dictionary mapping category to forecasted amount
        """
        if self._df.empty:
            return {}
        
        debits = self._df[self._df['type'] == TransactionType.DEBIT.value]
        
        if debits.empty:
            return {}
        
        # Calculate historical period
        date_range = (debits['date'].max() - debits['date'].min()).days
        if date_range < 1:
            date_range = 1
        
        # Calculate daily average by category
        category_totals = debits.groupby('category')['amount'].sum()
        category_daily_avg = category_totals / date_range
        
        # Forecast for next N days
        forecast = (category_daily_avg * days).to_dict()
        
        return forecast
    
    def predict_next_paycheck_date(self) -> Optional[datetime]:
        """
        Predict next paycheck date based on historical income patterns.
        
        Returns:
            Predicted date of next paycheck or None
        """
        if self._df.empty:
            return None
        
        credits = self._df[self._df['type'] == TransactionType.CREDIT.value]
        
        # Filter for likely paychecks (income category, substantial amounts)
        income = credits[credits['category'] == TransactionCategory.INCOME.value]
        
        if len(income) < 2:
            return None
        
        # Sort by date
        income = income.sort_values('date')
        
        # Calculate average interval between paychecks
        dates = income['date'].tolist()
        intervals = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
        
        if not intervals:
            return None
        
        avg_interval = np.mean(intervals)
        last_paycheck = income['date'].max()
        
        # Predict next paycheck
        next_paycheck = last_paycheck + timedelta(days=avg_interval)
        
        return next_paycheck
    
    def get_spending_velocity(self, window_days: int = 7) -> Dict[str, float]:
        """
        Calculate spending velocity (rate of spending change).
        
        Args:
            window_days: Window size for calculating velocity
            
        Returns:
            Dictionary with velocity metrics
        """
        if self._df.empty:
            return {
                'velocity': 0.0,
                'trend': 'stable',
                'recent_spending': 0.0,
                'previous_spending': 0.0,
                'window_days': window_days,
            }
        
        debits = self._df[self._df['type'] == TransactionType.DEBIT.value]
        
        if debits.empty:
            return {
                'velocity': 0.0,
                'trend': 'stable',
                'recent_spending': 0.0,
                'previous_spending': 0.0,
                'window_days': window_days,
            }
        
        # Get recent and previous period spending
        now = datetime.now()
        recent_start = now - timedelta(days=window_days)
        previous_start = now - timedelta(days=window_days * 2)
        
        recent_spending = debits[debits['date'] >= recent_start]['amount'].sum()
        previous_spending = debits[
            (debits['date'] >= previous_start) & (debits['date'] < recent_start)
        ]['amount'].sum()
        
        if previous_spending == 0:
            velocity = 0.0
            trend = 'stable'
        else:
            velocity = ((recent_spending - previous_spending) / previous_spending) * 100
            if velocity > 10:
                trend = 'increasing'
            elif velocity < -10:
                trend = 'decreasing'
            else:
                trend = 'stable'
        
        return {
            'velocity': float(velocity),
            'trend': trend,
            'recent_spending': float(recent_spending),
            'previous_spending': float(previous_spending),
            'window_days': window_days,
        }
    
    def identify_recurring_expenses(self, tolerance_days: int = 3) -> List[Dict[str, any]]:
        """
        Identify recurring expenses based on pattern matching.
        
        Args:
            tolerance_days: Tolerance for matching recurring patterns
            
        Returns:
            List of identified recurring expenses
        """
        if self._df.empty:
            return []
        
        debits = self._df[self._df['type'] == TransactionType.DEBIT.value]
        
        if debits.empty:
            return []
        
        recurring = []
        
        # Group by similar amounts and descriptions
        for description in debits['description'].unique():
            desc_transactions = debits[debits['description'] == description]
            
            if len(desc_transactions) < 2:
                continue
            
            # Check for regular intervals
            dates = sorted(desc_transactions['date'].tolist())
            if len(dates) < 2:
                continue
            
            intervals = [(dates[i+1] - dates[i]).days for i in range(len(dates)-1)]
            
            # Check if intervals are consistent
            if len(intervals) >= 2:
                avg_interval = np.mean(intervals)
                std_interval = np.std(intervals)
                
                # If standard deviation is low, it's likely recurring
                if std_interval <= tolerance_days:
                    avg_amount = desc_transactions['amount'].mean()
                    
                    recurring.append({
                        'description': description,
                        'average_amount': float(avg_amount),
                        'interval_days': float(avg_interval),
                        'occurrences': len(desc_transactions),
                        'category': desc_transactions.iloc[0]['category'],
                        'next_expected_date': (dates[-1] + timedelta(days=avg_interval)).strftime('%Y-%m-%d'),
                    })
        
        return recurring
