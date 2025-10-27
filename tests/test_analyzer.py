"""
Tests for TransactionAnalyzer.
"""

import pytest
from datetime import datetime, timedelta
from finance_copilot.transaction import Transaction, TransactionType, TransactionCategory
from finance_copilot.analyzer import TransactionAnalyzer


@pytest.fixture
def sample_transactions():
    """Create sample transactions for testing."""
    today = datetime.now()
    
    transactions = [
        # Debits (spending)
        Transaction(
            id="TXN001",
            date=today - timedelta(days=5),
            description="Groceries",
            amount=150.00,
            type=TransactionType.DEBIT,
            category=TransactionCategory.GROCERIES,
            merchant="Whole Foods"
        ),
        Transaction(
            id="TXN002",
            date=today - timedelta(days=10),
            description="Coffee",
            amount=5.50,
            type=TransactionType.DEBIT,
            category=TransactionCategory.FOOD_DINING,
            merchant="Starbucks"
        ),
        Transaction(
            id="TXN003",
            date=today - timedelta(days=15),
            description="Gas",
            amount=45.00,
            type=TransactionType.DEBIT,
            category=TransactionCategory.TRANSPORTATION,
            merchant="Gas Station"
        ),
        # Credit (income)
        Transaction(
            id="INC001",
            date=today - timedelta(days=7),
            description="Paycheck",
            amount=2500.00,
            type=TransactionType.CREDIT,
            category=TransactionCategory.INCOME,
            merchant="Employer"
        ),
    ]
    
    return transactions


def test_analyzer_initialization(sample_transactions):
    """Test analyzer initialization."""
    analyzer = TransactionAnalyzer(sample_transactions)
    assert len(analyzer.transactions) == 4


def test_get_total_spent(sample_transactions):
    """Test total spending calculation."""
    analyzer = TransactionAnalyzer(sample_transactions)
    total_spent = analyzer.get_total_spent()
    
    # Should sum all debits: 150 + 5.50 + 45 = 200.50
    assert total_spent == 200.50


def test_get_total_income(sample_transactions):
    """Test total income calculation."""
    analyzer = TransactionAnalyzer(sample_transactions)
    total_income = analyzer.get_total_income()
    
    # Should sum all credits: 2500
    assert total_income == 2500.00


def test_get_net_cashflow(sample_transactions):
    """Test net cashflow calculation."""
    analyzer = TransactionAnalyzer(sample_transactions)
    net_cashflow = analyzer.get_net_cashflow()
    
    # Income - Spending: 2500 - 200.50 = 2299.50
    assert net_cashflow == 2299.50


def test_get_spending_by_category(sample_transactions):
    """Test spending breakdown by category."""
    analyzer = TransactionAnalyzer(sample_transactions)
    spending = analyzer.get_spending_by_category()
    
    assert spending[TransactionCategory.GROCERIES.value] == 150.00
    assert spending[TransactionCategory.FOOD_DINING.value] == 5.50
    assert spending[TransactionCategory.TRANSPORTATION.value] == 45.00


def test_get_top_merchants(sample_transactions):
    """Test top merchants calculation."""
    analyzer = TransactionAnalyzer(sample_transactions)
    top_merchants = analyzer.get_top_merchants(limit=3)
    
    assert len(top_merchants) <= 3
    assert top_merchants[0][0] == "Whole Foods"
    assert top_merchants[0][1] == 150.00


def test_get_average_transaction(sample_transactions):
    """Test average transaction calculation."""
    analyzer = TransactionAnalyzer(sample_transactions)
    averages = analyzer.get_average_transaction()
    
    # Average debit: (150 + 5.50 + 45) / 3 = 66.83...
    assert 66.0 < averages['debit'] < 67.0
    # Average credit: 2500
    assert averages['credit'] == 2500.00


def test_get_insights(sample_transactions):
    """Test comprehensive insights generation."""
    analyzer = TransactionAnalyzer(sample_transactions)
    insights = analyzer.get_insights()
    
    assert 'total_transactions' in insights
    assert 'total_spent_30d' in insights
    assert 'total_income_30d' in insights
    assert 'net_cashflow_30d' in insights
    assert 'spending_by_category' in insights
    assert insights['total_transactions'] == 4


def test_empty_transactions():
    """Test analyzer with no transactions."""
    analyzer = TransactionAnalyzer([])
    
    assert analyzer.get_total_spent() == 0.0
    assert analyzer.get_total_income() == 0.0
    assert analyzer.get_net_cashflow() == 0.0
    assert analyzer.get_spending_by_category() == {}
