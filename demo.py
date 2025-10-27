#!/usr/bin/env python3
"""
Demo script showing Finance Copilot capabilities.
"""

from finance_copilot import FinanceCopilot
from finance_copilot.sample_data import SampleDataGenerator


def main():
    """Run a comprehensive demo of Finance Copilot."""
    
    print("=" * 70)
    print("Finance Copilot Demo - AI-Powered Financial Assistant")
    print("=" * 70)
    print()
    
    # Generate sample data
    print("Step 1: Generating 90 days of transaction history...")
    transactions = SampleDataGenerator.generate_with_patterns(days_back=90)
    print(f"✓ Generated {len(transactions)} transactions\n")
    
    # Initialize copilot
    print("Step 2: Initializing Finance Copilot...")
    copilot = FinanceCopilot(transactions)
    print("✓ Copilot initialized\n")
    
    # Show insights
    print("=" * 70)
    print("FINANCIAL INSIGHTS")
    print("=" * 70)
    insights = copilot.analyzer.get_insights()
    print(f"Total Transactions: {insights['total_transactions']}")
    print(f"Total Spent (30 days): ${insights['total_spent_30d']:.2f}")
    print(f"Total Income (30 days): ${insights['total_income_30d']:.2f}")
    print(f"Net Cashflow: ${insights['net_cashflow_30d']:.2f}")
    print()
    
    # Show spending by category
    print("Top Spending Categories:")
    for i, (category, amount) in enumerate(
        sorted(insights['spending_by_category'].items(), key=lambda x: x[1], reverse=True)[:5],
        1
    ):
        print(f"  {i}. {category}: ${amount:.2f}")
    print()
    
    # Show forecasting
    print("=" * 70)
    print("SPENDING FORECAST")
    print("=" * 70)
    forecast = copilot.forecaster.forecast_monthly_spending()
    print(f"Predicted Next Month Spending: ${forecast['forecast_amount']:.2f}")
    print(f"Daily Average: ${forecast['daily_average']:.2f}")
    print(f"Confidence Level: {forecast['confidence']}")
    print()
    
    # Show recurring expenses
    recurring = copilot.forecaster.identify_recurring_expenses()
    if recurring:
        print("Recurring Expenses Detected:")
        for expense in recurring[:5]:
            print(f"  • {expense['description']}: ${expense['average_amount']:.2f} "
                  f"every ~{int(expense['interval_days'])} days")
        print()
    
    # Show budget recommendations
    print("=" * 70)
    print("BUDGET RECOMMENDATIONS (50/30/20 Rule)")
    print("=" * 70)
    budget = copilot.advisor.get_recommended_budget()
    if 'error' not in budget:
        print(f"Monthly Income: ${budget['monthly_income']:.2f}")
        print(f"Needs (50%): ${budget['needs']['budget']:.2f}")
        print(f"Wants (30%): ${budget['wants']['budget']:.2f}")
        print(f"Savings (20%): ${budget['savings']['budget']:.2f}")
        print()
    
    # Show savings analysis
    savings = copilot.advisor.get_savings_potential()
    print("Savings Analysis:")
    print(f"  Current Monthly Savings: ${savings['current_monthly_savings']:.2f}")
    print(f"  Recommended Savings: ${savings['recommended_monthly_savings']:.2f}")
    print(f"  Savings Rate: {savings['savings_rate']:.1f}%")
    print(f"  Status: {savings['status'].replace('_', ' ').title()}")
    print()
    
    # Show alerts
    alerts = copilot.advisor.get_spending_alerts()
    if alerts:
        print("=" * 70)
        print("SPENDING ALERTS")
        print("=" * 70)
        for alert in alerts[:5]:
            icon = "⚠️" if alert['severity'] == 'high' else "ℹ️"
            print(f"{icon} {alert['title']}")
            print(f"   {alert['message']}")
        print()
    
    # Show recommendations
    recommendations = copilot.advisor.get_recommendations()
    print("=" * 70)
    print("PERSONALIZED RECOMMENDATIONS")
    print("=" * 70)
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")
    print()
    
    # Natural language queries
    print("=" * 70)
    print("NATURAL LANGUAGE Q&A")
    print("=" * 70)
    questions = [
        "How much did I spend?",
        "What is my income?",
        "Am I overspending?",
    ]
    
    for question in questions:
        response = copilot.ask(question)
        print(f"Q: {question}")
        print(f"A: {response}")
        print()
    
    print("=" * 70)
    print("Demo Complete!")
    print("=" * 70)
    print("\nTo try the interactive CLI, run:")
    print("  python cli.py --demo")
    print()


if __name__ == "__main__":
    main()
