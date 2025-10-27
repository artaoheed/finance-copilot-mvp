"""
Tests for SpendingForecaster.
"""

import pytest
from datetime import datetime, timedelta
from finance_copilot.transaction import Transaction, TransactionType, TransactionCategory
from finance_copilot.forecaster import SpendingForecaster


@pytest.fixture
def sample_transactions():
    """Create sample transactions for testing."""
    today = datetime.now()
    transactions = []
    
    # Add 30 days of daily spending
    for i in range(30):
        transactions.append(
            Transaction(
                id=f"TXN{i:03d}",
                date=today - timedelta(days=i),
                description=f"Purchase {i}",
                amount=50.00,  # $50/day
                type=TransactionType.DEBIT,
                category=TransactionCategory.GROCERIES,
                merchant="Store"
            )
        )
    
    # Add bi-weekly paychecks
    transactions.append(
        Transaction(
            id="INC001",
            date=today - timedelta(days=7),
            description="Paycheck",
            amount=2000.00,
            type=TransactionType.CREDIT,
            category=TransactionCategory.INCOME,
            merchant="Employer"
        )
    )
    transactions.append(
        Transaction(
            id="INC002",
            date=today - timedelta(days=21),
            description="Paycheck",
            amount=2000.00,
            type=TransactionType.CREDIT,
            category=TransactionCategory.INCOME,
            merchant="Employer"
        )
    )
    
    return transactions


def test_forecaster_initialization(sample_transactions):
    """Test forecaster initialization."""
    forecaster = SpendingForecaster(sample_transactions)
    assert len(forecaster.transactions) == 32


def test_forecast_monthly_spending(sample_transactions):
    """Test monthly spending forecast."""
    forecaster = SpendingForecaster(sample_transactions)
    forecast = forecaster.forecast_monthly_spending(1)
    
    assert 'forecast_amount' in forecast
    assert 'daily_average' in forecast
    assert 'confidence' in forecast
    
    # With $50/day spending, expect ~$1500 for 30 days
    assert 1400 < forecast['forecast_amount'] < 1600


def test_forecast_category_spending(sample_transactions):
    """Test category spending forecast."""
    forecaster = SpendingForecaster(sample_transactions)
    forecast = forecaster.forecast_category_spending(30)
    
    assert TransactionCategory.GROCERIES.value in forecast
    # Should be close to $1500 (30 days * $50/day)
    assert 1400 < forecast[TransactionCategory.GROCERIES.value] < 1600


def test_predict_next_paycheck_date(sample_transactions):
    """Test paycheck prediction."""
    forecaster = SpendingForecaster(sample_transactions)
    next_paycheck = forecaster.predict_next_paycheck_date()
    
    assert next_paycheck is not None
    # Should predict ~14 days from last paycheck
    today = datetime.now()
    days_until = (next_paycheck - today).days
    assert 5 < days_until < 15


def test_get_spending_velocity(sample_transactions):
    """Test spending velocity calculation."""
    forecaster = SpendingForecaster(sample_transactions)
    velocity = forecaster.get_spending_velocity(7)
    
    assert 'velocity' in velocity
    assert 'trend' in velocity
    assert 'recent_spending' in velocity


def test_identify_recurring_expenses():
    """Test recurring expense identification."""
    today = datetime.now()
    transactions = []
    
    # Add monthly recurring expense
    for i in range(3):
        transactions.append(
            Transaction(
                id=f"TXN{i:03d}",
                date=today - timedelta(days=30*i),
                description="Rent Payment",
                amount=1200.00,
                type=TransactionType.DEBIT,
                category=TransactionCategory.BILLS_UTILITIES,
                merchant="Landlord"
            )
        )
    
    forecaster = SpendingForecaster(transactions)
    recurring = forecaster.identify_recurring_expenses(tolerance_days=3)
    
    assert len(recurring) > 0
    # Find rent in recurring expenses
    rent_found = any(r['description'] == 'Rent Payment' for r in recurring)
    assert rent_found


def test_empty_transactions():
    """Test forecaster with no transactions."""
    forecaster = SpendingForecaster([])
    
    forecast = forecaster.forecast_monthly_spending()
    assert forecast['forecast_amount'] == 0.0
