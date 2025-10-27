"""
Finance Copilot - AI-powered financial assistant for Cash App-style transaction analysis.

This package provides tools for analyzing transaction history, forecasting spending,
and providing automated budgeting advice.
"""

__version__ = "0.1.0"

from .transaction import Transaction, TransactionCategory, TransactionType
from .analyzer import TransactionAnalyzer
from .forecaster import SpendingForecaster
from .budget_advisor import BudgetAdvisor
from .copilot import FinanceCopilot

__all__ = [
    "Transaction",
    "TransactionCategory",
    "TransactionType",
    "TransactionAnalyzer",
    "SpendingForecaster",
    "BudgetAdvisor",
    "FinanceCopilot",
]
