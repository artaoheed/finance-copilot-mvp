"""
Transaction analysis engine for generating insights from transaction history.
"""

from typing import List, Dict, Tuple, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import pandas as pd
from .transaction import Transaction, TransactionType, TransactionCategory


class TransactionAnalyzer:
    """
    Analyzes transaction history to provide insights and statistics.
    """
    
    def __init__(self, transactions: List[Transaction]):
        """
        Initialize analyzer with transaction history.
        
        Args:
            transactions: List of Transaction objects
        """
        self.transactions = transactions
        self._df = self._to_dataframe()
    
    def _to_dataframe(self) -> pd.DataFrame:
        """Convert transactions to pandas DataFrame for analysis."""
        if not self.transactions:
            return pd.DataFrame()
        
        data = [t.to_dict() for t in self.transactions]
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        df['amount'] = pd.to_numeric(df['amount'])
        return df
    
    def get_total_spent(self, days: Optional[int] = None) -> float:
        """
        Calculate total amount spent (debits only).
        
        Args:
            days: Optional number of days to look back
            
        Returns:
            Total amount spent
        """
        df = self._filter_by_days(days)
        if df.empty:
            return 0.0
        debits = df[df['type'] == TransactionType.DEBIT.value]
        return float(debits['amount'].sum())
    
    def get_total_income(self, days: Optional[int] = None) -> float:
        """
        Calculate total income (credits only).
        
        Args:
            days: Optional number of days to look back
            
        Returns:
            Total income amount
        """
        df = self._filter_by_days(days)
        if df.empty:
            return 0.0
        credits = df[df['type'] == TransactionType.CREDIT.value]
        return float(credits['amount'].sum())
    
    def get_net_cashflow(self, days: Optional[int] = None) -> float:
        """
        Calculate net cashflow (income - spending).
        
        Args:
            days: Optional number of days to look back
            
        Returns:
            Net cashflow amount
        """
        return self.get_total_income(days) - self.get_total_spent(days)
    
    def get_spending_by_category(self, days: Optional[int] = None) -> Dict[str, float]:
        """
        Get spending breakdown by category.
        
        Args:
            days: Optional number of days to look back
            
        Returns:
            Dictionary mapping category to total spent
        """
        df = self._filter_by_days(days)
        if df.empty:
            return {}
        debits = df[df['type'] == TransactionType.DEBIT.value]
        
        if debits.empty:
            return {}
        
        category_spending = debits.groupby('category')['amount'].sum()
        return category_spending.to_dict()
    
    def get_top_merchants(self, limit: int = 5, days: Optional[int] = None) -> List[Tuple[str, float]]:
        """
        Get top merchants by spending.
        
        Args:
            limit: Number of top merchants to return
            days: Optional number of days to look back
            
        Returns:
            List of tuples (merchant, total_spent)
        """
        df = self._filter_by_days(days)
        if df.empty:
            return []
        debits = df[df['type'] == TransactionType.DEBIT.value]
        
        if debits.empty or 'merchant' not in debits.columns:
            return []
        
        merchant_spending = debits[debits['merchant'].notna()].groupby('merchant')['amount'].sum()
        top_merchants = merchant_spending.nlargest(limit)
        return list(top_merchants.items())
    
    def get_average_transaction(self, days: Optional[int] = None) -> Dict[str, float]:
        """
        Calculate average transaction amounts.
        
        Args:
            days: Optional number of days to look back
            
        Returns:
            Dictionary with average debit and credit amounts
        """
        df = self._filter_by_days(days)
        
        result = {}
        if df.empty:
            result['debit'] = 0.0
            result['credit'] = 0.0
        else:
            debits = df[df['type'] == TransactionType.DEBIT.value]
            credits = df[df['type'] == TransactionType.CREDIT.value]
            
            result['debit'] = float(debits['amount'].mean()) if not debits.empty else 0.0
            result['credit'] = float(credits['amount'].mean()) if not credits.empty else 0.0
        
        return result
    
    def get_spending_trend(self, period: str = 'daily') -> pd.DataFrame:
        """
        Get spending trend over time.
        
        Args:
            period: Aggregation period ('daily', 'weekly', 'monthly')
            
        Returns:
            DataFrame with date and spending amount
        """
        if self._df.empty:
            return pd.DataFrame()
        
        df = self._df[self._df['type'] == TransactionType.DEBIT.value].copy()
        
        if df.empty:
            return pd.DataFrame()
        
        df.set_index('date', inplace=True)
        
        if period == 'daily':
            trend = df.resample('D')['amount'].sum()
        elif period == 'weekly':
            trend = df.resample('W')['amount'].sum()
        elif period == 'monthly':
            trend = df.resample('M')['amount'].sum()
        else:
            raise ValueError(f"Invalid period: {period}")
        
        return trend.reset_index()
    
    def get_insights(self) -> Dict[str, any]:
        """
        Generate comprehensive insights from transaction history.
        
        Returns:
            Dictionary containing various insights
        """
        insights = {
            'total_transactions': len(self.transactions),
            'total_spent_30d': self.get_total_spent(30),
            'total_income_30d': self.get_total_income(30),
            'net_cashflow_30d': self.get_net_cashflow(30),
            'spending_by_category': self.get_spending_by_category(30),
            'top_merchants': self.get_top_merchants(5, 30),
            'average_transaction': self.get_average_transaction(30),
            'largest_expense': self._get_largest_expense(),
            'most_frequent_category': self._get_most_frequent_category(),
        }
        
        return insights
    
    def _filter_by_days(self, days: Optional[int]) -> pd.DataFrame:
        """Filter dataframe by number of days from today."""
        if self._df.empty:
            return self._df
        
        if days is None:
            return self._df
        
        cutoff_date = datetime.now() - timedelta(days=days)
        return self._df[self._df['date'] >= cutoff_date]
    
    def _get_largest_expense(self) -> Optional[Dict[str, any]]:
        """Get the largest single expense."""
        if self._df.empty:
            return None
        debits = self._df[self._df['type'] == TransactionType.DEBIT.value]
        
        if debits.empty:
            return None
        
        largest = debits.loc[debits['amount'].idxmax()]
        return {
            'description': largest['description'],
            'amount': float(largest['amount']),
            'date': largest['date'].strftime('%Y-%m-%d'),
            'category': largest['category'],
        }
    
    def _get_most_frequent_category(self) -> Optional[str]:
        """Get the most frequent spending category."""
        if self._df.empty:
            return None
        debits = self._df[self._df['type'] == TransactionType.DEBIT.value]
        
        if debits.empty:
            return None
        
        return debits['category'].mode()[0] if not debits['category'].mode().empty else None
