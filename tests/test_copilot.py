"""
Tests for FinanceCopilot.
"""

import pytest
from datetime import datetime, timedelta
from finance_copilot.transaction import Transaction, TransactionType, TransactionCategory
from finance_copilot.copilot import FinanceCopilot


@pytest.fixture
def sample_transactions():
    """Create sample transactions for testing."""
    today = datetime.now()
    
    transactions = [
        Transaction(
            id="INC001",
            date=today - timedelta(days=15),
            description="Paycheck",
            amount=3000.00,
            type=TransactionType.CREDIT,
            category=TransactionCategory.INCOME,
            merchant="Employer"
        ),
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
    ]
    
    return transactions


def test_copilot_initialization(sample_transactions):
    """Test copilot initialization."""
    copilot = FinanceCopilot(sample_transactions)
    assert len(copilot.transactions) == 3
    assert copilot.analyzer is not None
    assert copilot.forecaster is not None
    assert copilot.advisor is not None


def test_get_summary(sample_transactions):
    """Test summary generation."""
    copilot = FinanceCopilot(sample_transactions)
    summary = copilot.get_summary()
    
    assert isinstance(summary, str)
    assert len(summary) > 0
    assert "Financial Summary" in summary


def test_ask_rule_based(sample_transactions):
    """Test rule-based question answering."""
    copilot = FinanceCopilot(sample_transactions)
    
    # Test spending question
    response = copilot.ask("How much did I spend?")
    assert isinstance(response, str)
    assert "$" in response
    
    # Test income question
    response = copilot.ask("What is my income?")
    assert isinstance(response, str)
    assert "$" in response
    
    # Test budget question
    response = copilot.ask("What is my budget?")
    assert isinstance(response, str)


def test_ask_with_monthly_income(sample_transactions):
    """Test copilot with specified monthly income."""
    copilot = FinanceCopilot(sample_transactions, monthly_income=4000.00)
    
    response = copilot.ask("What is my budget?")
    assert isinstance(response, str)
    assert "$" in response


def test_build_context(sample_transactions):
    """Test context building for AI."""
    copilot = FinanceCopilot(sample_transactions)
    context = copilot._build_context()
    
    assert 'insights' in context
    assert 'forecast' in context
    assert 'budget' in context
    assert 'savings' in context
    assert 'total_transactions' in context


def test_format_context(sample_transactions):
    """Test context formatting."""
    copilot = FinanceCopilot(sample_transactions)
    context = copilot._build_context()
    formatted = copilot._format_context(context)
    
    assert isinstance(formatted, str)
    assert len(formatted) > 0
