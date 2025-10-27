"""
Budget advisor module for automated budgeting recommendations.
"""

from typing import List, Dict, Optional
from datetime import datetime, timedelta
from .transaction import Transaction, TransactionType, TransactionCategory
from .analyzer import TransactionAnalyzer
from .forecaster import SpendingForecaster


class BudgetAdvisor:
    """
    Provides automated budgeting advice based on transaction analysis.
    """
    
    def __init__(self, transactions: List[Transaction], monthly_income: Optional[float] = None):
        """
        Initialize budget advisor.
        
        Args:
            transactions: List of Transaction objects
            monthly_income: Optional monthly income amount
        """
        self.transactions = transactions
        self.analyzer = TransactionAnalyzer(transactions)
        self.forecaster = SpendingForecaster(transactions)
        self.monthly_income = monthly_income or self._estimate_monthly_income()
    
    def _estimate_monthly_income(self) -> float:
        """Estimate monthly income from transaction history."""
        total_income = self.analyzer.get_total_income(30)
        return total_income if total_income > 0 else 0.0
    
    def get_recommended_budget(self) -> Dict[str, any]:
        """
        Get recommended budget allocations based on the 50/30/20 rule.
        
        Returns:
            Dictionary with budget recommendations
        """
        if self.monthly_income == 0:
            return {
                'error': 'Unable to determine monthly income',
                'recommendation': 'Add income transactions to get personalized budget advice'
            }
        
        # 50/30/20 rule: 50% needs, 30% wants, 20% savings
        needs_budget = self.monthly_income * 0.50
        wants_budget = self.monthly_income * 0.30
        savings_budget = self.monthly_income * 0.20
        
        return {
            'monthly_income': self.monthly_income,
            'needs': {
                'budget': needs_budget,
                'percentage': 50,
                'categories': ['Groceries', 'Bills & Utilities', 'Healthcare', 'Transportation']
            },
            'wants': {
                'budget': wants_budget,
                'percentage': 30,
                'categories': ['Food & Dining', 'Entertainment', 'Shopping', 'Personal']
            },
            'savings': {
                'budget': savings_budget,
                'percentage': 20,
                'description': 'Emergency fund and investments'
            }
        }
    
    def get_category_budgets(self) -> Dict[str, Dict[str, float]]:
        """
        Get recommended budgets for each spending category.
        
        Returns:
            Dictionary mapping category to budget details
        """
        recommended = self.get_recommended_budget()
        
        if 'error' in recommended:
            return {}
        
        # Get historical spending by category
        historical_spending = self.analyzer.get_spending_by_category(30)
        
        category_budgets = {}
        
        # Allocate needs budget
        needs_categories = [
            TransactionCategory.GROCERIES.value,
            TransactionCategory.BILLS_UTILITIES.value,
            TransactionCategory.HEALTHCARE.value,
            TransactionCategory.TRANSPORTATION.value,
        ]
        
        needs_total_historical = sum(
            historical_spending.get(cat, 0) for cat in needs_categories
        )
        needs_budget = recommended['needs']['budget']
        
        for category in needs_categories:
            historical = historical_spending.get(category, 0)
            if needs_total_historical > 0:
                proportion = historical / needs_total_historical
                budget = needs_budget * proportion
            else:
                budget = needs_budget / len(needs_categories)
            
            category_budgets[category] = {
                'recommended': budget,
                'actual_spending': historical,
                'difference': budget - historical,
                'status': 'under_budget' if budget > historical else 'over_budget'
            }
        
        # Allocate wants budget
        wants_categories = [
            TransactionCategory.FOOD_DINING.value,
            TransactionCategory.ENTERTAINMENT.value,
            TransactionCategory.SHOPPING.value,
            TransactionCategory.PERSONAL.value,
        ]
        
        wants_total_historical = sum(
            historical_spending.get(cat, 0) for cat in wants_categories
        )
        wants_budget = recommended['wants']['budget']
        
        for category in wants_categories:
            historical = historical_spending.get(category, 0)
            if wants_total_historical > 0:
                proportion = historical / wants_total_historical
                budget = wants_budget * proportion
            else:
                budget = wants_budget / len(wants_categories)
            
            category_budgets[category] = {
                'recommended': budget,
                'actual_spending': historical,
                'difference': budget - historical,
                'status': 'under_budget' if budget > historical else 'over_budget'
            }
        
        return category_budgets
    
    def get_savings_potential(self) -> Dict[str, any]:
        """
        Analyze savings potential based on current spending patterns.
        
        Returns:
            Dictionary with savings analysis
        """
        total_income = self.analyzer.get_total_income(30)
        total_spent = self.analyzer.get_total_spent(30)
        
        current_savings = total_income - total_spent
        recommended_savings = self.monthly_income * 0.20
        
        return {
            'current_monthly_savings': current_savings,
            'recommended_monthly_savings': recommended_savings,
            'savings_gap': recommended_savings - current_savings,
            'savings_rate': (current_savings / total_income * 100) if total_income > 0 else 0,
            'recommended_rate': 20.0,
            'status': 'on_track' if current_savings >= recommended_savings else 'needs_improvement'
        }
    
    def get_spending_alerts(self) -> List[Dict[str, any]]:
        """
        Generate alerts for concerning spending patterns.
        
        Returns:
            List of spending alerts
        """
        alerts = []
        
        # Check spending velocity
        velocity = self.forecaster.get_spending_velocity(7)
        if velocity['velocity'] > 25:
            alerts.append({
                'type': 'warning',
                'title': 'Spending Increasing Rapidly',
                'message': f"Your spending has increased by {velocity['velocity']:.1f}% in the last week.",
                'severity': 'high'
            })
        
        # Check category budgets
        category_budgets = self.get_category_budgets()
        for category, budget_info in category_budgets.items():
            if budget_info['status'] == 'over_budget':
                overage = abs(budget_info['difference'])
                overage_pct = (overage / budget_info['recommended'] * 100) if budget_info['recommended'] > 0 else 0
                
                if overage_pct > 20:
                    alerts.append({
                        'type': 'warning',
                        'title': f'{category} Over Budget',
                        'message': f"You're ${overage:.2f} over budget in {category} ({overage_pct:.1f}% over).",
                        'severity': 'medium'
                    })
        
        # Check savings
        savings = self.get_savings_potential()
        if savings['status'] == 'needs_improvement':
            gap = savings['savings_gap']
            alerts.append({
                'type': 'info',
                'title': 'Savings Below Target',
                'message': f"You're saving ${gap:.2f} less than the recommended 20% of income.",
                'severity': 'medium'
            })
        
        # Check for unusual large transactions
        insights = self.analyzer.get_insights()
        if insights.get('largest_expense'):
            largest = insights['largest_expense']
            avg_transaction = insights['average_transaction']['debit']
            
            if largest['amount'] > avg_transaction * 5:
                alerts.append({
                    'type': 'info',
                    'title': 'Large Transaction Detected',
                    'message': f"Unusually large expense of ${largest['amount']:.2f} for {largest['description']}.",
                    'severity': 'low'
                })
        
        return alerts
    
    def get_recommendations(self) -> List[str]:
        """
        Get personalized financial recommendations.
        
        Returns:
            List of recommendation strings
        """
        recommendations = []
        
        # Analyze spending patterns
        spending_by_category = self.analyzer.get_spending_by_category(30)
        total_spent = self.analyzer.get_total_spent(30)
        
        if total_spent > 0:
            # Check dining out
            dining_spent = spending_by_category.get(TransactionCategory.FOOD_DINING.value, 0)
            dining_pct = (dining_spent / total_spent) * 100
            
            if dining_pct > 15:
                recommendations.append(
                    f"Consider reducing dining out expenses (currently {dining_pct:.1f}% of spending). "
                    f"Cooking at home could save you approximately ${dining_spent * 0.3:.2f} per month."
                )
            
            # Check entertainment
            entertainment_spent = spending_by_category.get(TransactionCategory.ENTERTAINMENT.value, 0)
            entertainment_pct = (entertainment_spent / total_spent) * 100
            
            if entertainment_pct > 10:
                recommendations.append(
                    f"Entertainment spending is {entertainment_pct:.1f}% of your budget. "
                    f"Look for free or lower-cost alternatives to save money."
                )
        
        # Check savings
        savings = self.get_savings_potential()
        if savings['status'] == 'needs_improvement':
            recommendations.append(
                f"Increase your savings by ${savings['savings_gap']:.2f} per month to reach the recommended 20% savings rate."
            )
        
        # Check recurring expenses
        recurring = self.forecaster.identify_recurring_expenses()
        if recurring:
            recommendations.append(
                f"You have {len(recurring)} recurring expenses. Review subscriptions and services to eliminate unused ones."
            )
        
        # General advice
        if not recommendations:
            recommendations.append(
                "Great job! Your spending is well-balanced. Continue monitoring your budget regularly."
            )
        
        return recommendations
