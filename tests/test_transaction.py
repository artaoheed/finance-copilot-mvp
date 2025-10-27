"""
Tests for Transaction model.
"""

import pytest
from datetime import datetime
from finance_copilot.transaction import Transaction, TransactionType, TransactionCategory


def test_transaction_creation():
    """Test basic transaction creation."""
    transaction = Transaction(
        id="TXN001",
        date=datetime(2024, 1, 15, 10, 30),
        description="Coffee at Starbucks",
        amount=5.75,
        type=TransactionType.DEBIT,
        category=TransactionCategory.FOOD_DINING,
        merchant="Starbucks"
    )
    
    assert transaction.id == "TXN001"
    assert transaction.description == "Coffee at Starbucks"
    assert transaction.amount == 5.75
    assert transaction.type == TransactionType.DEBIT
    assert transaction.category == TransactionCategory.FOOD_DINING
    assert transaction.merchant == "Starbucks"
    assert transaction.status == "completed"


def test_transaction_to_dict():
    """Test transaction serialization to dictionary."""
    transaction = Transaction(
        id="TXN001",
        date=datetime(2024, 1, 15, 10, 30),
        description="Coffee at Starbucks",
        amount=5.75,
        type=TransactionType.DEBIT,
        category=TransactionCategory.FOOD_DINING,
        merchant="Starbucks"
    )
    
    data = transaction.to_dict()
    
    assert data['id'] == "TXN001"
    assert data['description'] == "Coffee at Starbucks"
    assert data['amount'] == 5.75
    assert data['type'] == TransactionType.DEBIT.value
    assert data['category'] == TransactionCategory.FOOD_DINING.value


def test_transaction_from_dict():
    """Test transaction deserialization from dictionary."""
    data = {
        'id': 'TXN001',
        'date': '2024-01-15T10:30:00',
        'description': 'Coffee at Starbucks',
        'amount': 5.75,
        'type': 'debit',
        'category': 'Food & Dining',
        'merchant': 'Starbucks',
        'status': 'completed',
        'notes': None
    }
    
    transaction = Transaction.from_dict(data)
    
    assert transaction.id == "TXN001"
    assert transaction.description == "Coffee at Starbucks"
    assert transaction.amount == 5.75
    assert transaction.type == TransactionType.DEBIT
    assert transaction.category == TransactionCategory.FOOD_DINING


def test_transaction_str_representation():
    """Test string representation of transaction."""
    transaction = Transaction(
        id="TXN001",
        date=datetime(2024, 1, 15),
        description="Coffee at Starbucks",
        amount=5.75,
        type=TransactionType.DEBIT,
        category=TransactionCategory.FOOD_DINING,
        merchant="Starbucks"
    )
    
    str_repr = str(transaction)
    
    assert "2024-01-15" in str_repr
    assert "-$5.75" in str_repr
    assert "Coffee at Starbucks" in str_repr
    assert "Food & Dining" in str_repr


def test_credit_transaction():
    """Test credit (income) transaction."""
    transaction = Transaction(
        id="INC001",
        date=datetime(2024, 1, 15),
        description="Paycheck",
        amount=2500.00,
        type=TransactionType.CREDIT,
        category=TransactionCategory.INCOME,
        merchant="Employer"
    )
    
    assert transaction.type == TransactionType.CREDIT
    str_repr = str(transaction)
    assert "+$2500.00" in str_repr
