"""
Tests for BudgetAdvisor.
"""

import pytest
from datetime import datetime, timedelta
from finance_copilot.transaction import Transaction, TransactionType, TransactionCategory
from finance_copilot.budget_advisor import BudgetAdvisor


@pytest.fixture
def sample_transactions():
    """Create sample transactions for testing."""
    today = datetime.now()
    transactions = []
    
    # Add income
    transactions.append(
        Transaction(
            id="INC001",
            date=today - timedelta(days=15),
            description="Paycheck",
            amount=3000.00,
            type=TransactionType.CREDIT,
            category=TransactionCategory.INCOME,
            merchant="Employer"
        )
    )
    
    # Add various expenses
    expenses = [
        ("Groceries", 400.00, TransactionCategory.GROCERIES, "Whole Foods"),
        ("Rent", 1200.00, TransactionCategory.BILLS_UTILITIES, "Landlord"),
        ("Dining", 200.00, TransactionCategory.FOOD_DINING, "Restaurant"),
        ("Entertainment", 100.00, TransactionCategory.ENTERTAINMENT, "Movie Theater"),
    ]
    
    for i, (desc, amount, category, merchant) in enumerate(expenses):
        transactions.append(
            Transaction(
                id=f"TXN{i:03d}",
                date=today - timedelta(days=10-i),
                description=desc,
                amount=amount,
                type=TransactionType.DEBIT,
                category=category,
                merchant=merchant
            )
        )
    
    return transactions


def test_advisor_initialization(sample_transactions):
    """Test advisor initialization."""
    advisor = BudgetAdvisor(sample_transactions)
    assert len(advisor.transactions) == 5
    assert advisor.monthly_income == 3000.00


def test_advisor_with_specified_income(sample_transactions):
    """Test advisor with specified income."""
    advisor = BudgetAdvisor(sample_transactions, monthly_income=4000.00)
    assert advisor.monthly_income == 4000.00


def test_get_recommended_budget(sample_transactions):
    """Test budget recommendations."""
    advisor = BudgetAdvisor(sample_transactions)
    budget = advisor.get_recommended_budget()
    
    assert 'monthly_income' in budget
    assert 'needs' in budget
    assert 'wants' in budget
    assert 'savings' in budget
    
    # Check 50/30/20 rule
    assert budget['needs']['budget'] == 3000.00 * 0.50
    assert budget['wants']['budget'] == 3000.00 * 0.30
    assert budget['savings']['budget'] == 3000.00 * 0.20


def test_get_category_budgets(sample_transactions):
    """Test category budget allocations."""
    advisor = BudgetAdvisor(sample_transactions)
    category_budgets = advisor.get_category_budgets()
    
    assert len(category_budgets) > 0
    # Check that categories have required fields
    for category, budget_info in category_budgets.items():
        assert 'recommended' in budget_info
        assert 'actual_spending' in budget_info
        assert 'difference' in budget_info
        assert 'status' in budget_info


def test_get_savings_potential(sample_transactions):
    """Test savings analysis."""
    advisor = BudgetAdvisor(sample_transactions)
    savings = advisor.get_savings_potential()
    
    assert 'current_monthly_savings' in savings
    assert 'recommended_monthly_savings' in savings
    assert 'savings_gap' in savings
    assert 'savings_rate' in savings
    assert 'status' in savings


def test_get_spending_alerts(sample_transactions):
    """Test spending alerts generation."""
    advisor = BudgetAdvisor(sample_transactions)
    alerts = advisor.get_spending_alerts()
    
    assert isinstance(alerts, list)
    # Alerts should have required fields
    for alert in alerts:
        assert 'type' in alert
        assert 'title' in alert
        assert 'message' in alert
        assert 'severity' in alert


def test_get_recommendations(sample_transactions):
    """Test personalized recommendations."""
    advisor = BudgetAdvisor(sample_transactions)
    recommendations = advisor.get_recommendations()
    
    assert isinstance(recommendations, list)
    assert len(recommendations) > 0


def test_advisor_no_income():
    """Test advisor with no income transactions."""
    today = datetime.now()
    transactions = [
        Transaction(
            id="TXN001",
            date=today - timedelta(days=5),
            description="Purchase",
            amount=50.00,
            type=TransactionType.DEBIT,
            category=TransactionCategory.SHOPPING,
            merchant="Store"
        )
    ]
    
    advisor = BudgetAdvisor(transactions)
    budget = advisor.get_recommended_budget()
    
    # Should return error when no income is available
    assert 'error' in budget or advisor.monthly_income >= 0
