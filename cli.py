#!/usr/bin/env python3
"""
Command-line interface for Finance Copilot.
"""

import argparse
import sys
from typing import List
from finance_copilot import FinanceCopilot
from finance_copilot.sample_data import SampleDataGenerator
from finance_copilot.transaction import Transaction


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Finance Copilot - AI-powered financial assistant"
    )
    
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Run with sample transaction data"
    )
    
    parser.add_argument(
        "--transactions",
        type=int,
        default=150,
        help="Number of sample transactions to generate (default: 150)"
    )
    
    parser.add_argument(
        "--days",
        type=int,
        default=90,
        help="Number of days of transaction history (default: 90)"
    )
    
    parser.add_argument(
        "--summary",
        action="store_true",
        help="Show financial summary and exit"
    )
    
    parser.add_argument(
        "--ask",
        type=str,
        help="Ask a specific question and exit"
    )
    
    args = parser.parse_args()
    
    # Load or generate transactions
    if args.demo:
        print("Generating sample transaction data...")
        transactions = SampleDataGenerator.generate_with_patterns(days_back=args.days)
        print(f"Generated {len(transactions)} sample transactions over {args.days} days.\n")
    else:
        print("Error: Currently only demo mode is supported.")
        print("Use --demo flag to run with sample data.")
        sys.exit(1)
    
    # Initialize copilot
    copilot = FinanceCopilot(transactions)
    
    # Handle specific commands
    if args.summary:
        print(copilot.get_summary())
        sys.exit(0)
    
    if args.ask:
        response = copilot.ask(args.ask)
        print(f"\nQuestion: {args.ask}")
        print(f"Answer: {response}\n")
        sys.exit(0)
    
    # Interactive mode
    print("=" * 60)
    print("Finance Copilot - AI-Powered Financial Assistant")
    print("=" * 60)
    print("\nCommands:")
    print("  summary - Show financial summary")
    print("  insights - Show key insights")
    print("  forecast - Show spending forecast")
    print("  budget - Show budget recommendations")
    print("  alerts - Show spending alerts")
    print("  ask <question> - Ask a question in natural language")
    print("  help - Show this help message")
    print("  quit - Exit the application")
    print()
    
    while True:
        try:
            user_input = input("finance-copilot> ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            elif user_input.lower() == 'help':
                print("\nCommands:")
                print("  summary - Show financial summary")
                print("  insights - Show key insights")
                print("  forecast - Show spending forecast")
                print("  budget - Show budget recommendations")
                print("  alerts - Show spending alerts")
                print("  ask <question> - Ask a question in natural language")
                print("  help - Show this help message")
                print("  quit - Exit the application\n")
            
            elif user_input.lower() == 'summary':
                print("\n" + copilot.get_summary())
            
            elif user_input.lower() == 'insights':
                insights = copilot.analyzer.get_insights()
                print("\n=== Key Insights ===")
                print(f"Total Transactions: {insights['total_transactions']}")
                print(f"Total Spent (30d): ${insights['total_spent_30d']:.2f}")
                print(f"Total Income (30d): ${insights['total_income_30d']:.2f}")
                print(f"Net Cashflow: ${insights['net_cashflow_30d']:.2f}")
                
                if insights['largest_expense']:
                    exp = insights['largest_expense']
                    print(f"\nLargest Expense: ${exp['amount']:.2f} - {exp['description']}")
                    print(f"Date: {exp['date']}, Category: {exp['category']}")
                
                print()
            
            elif user_input.lower() == 'forecast':
                forecast = copilot.forecaster.forecast_monthly_spending()
                print("\n=== Spending Forecast ===")
                print(f"Forecasted Monthly Spending: ${forecast['forecast_amount']:.2f}")
                print(f"Daily Average: ${forecast['daily_average']:.2f}")
                print(f"Confidence: {forecast['confidence']}")
                
                # Category forecast
                cat_forecast = copilot.forecaster.forecast_category_spending(30)
                if cat_forecast:
                    print("\nForecast by Category (30 days):")
                    for cat, amount in sorted(cat_forecast.items(), key=lambda x: x[1], reverse=True):
                        print(f"  {cat}: ${amount:.2f}")
                
                print()
            
            elif user_input.lower() == 'budget':
                budget = copilot.advisor.get_recommended_budget()
                if 'error' in budget:
                    print(f"\n{budget['recommendation']}\n")
                else:
                    print("\n=== Budget Recommendations (50/30/20 Rule) ===")
                    print(f"Monthly Income: ${budget['monthly_income']:.2f}\n")
                    print(f"Needs (50%): ${budget['needs']['budget']:.2f}")
                    print(f"  Categories: {', '.join(budget['needs']['categories'])}")
                    print(f"\nWants (30%): ${budget['wants']['budget']:.2f}")
                    print(f"  Categories: {', '.join(budget['wants']['categories'])}")
                    print(f"\nSavings (20%): ${budget['savings']['budget']:.2f}")
                    print(f"  {budget['savings']['description']}")
                    print()
            
            elif user_input.lower() == 'alerts':
                alerts = copilot.advisor.get_spending_alerts()
                if not alerts:
                    print("\n✅ No alerts - your spending looks good!\n")
                else:
                    print("\n=== Spending Alerts ===")
                    for alert in alerts:
                        icon = "⚠️" if alert['severity'] == 'high' else "ℹ️"
                        print(f"{icon} [{alert['type'].upper()}] {alert['title']}")
                        print(f"   {alert['message']}\n")
            
            elif user_input.lower().startswith('ask '):
                question = user_input[4:].strip()
                if question:
                    response = copilot.ask(question)
                    print(f"\n{response}\n")
                else:
                    print("\nPlease provide a question after 'ask'\n")
            
            else:
                # Treat as a natural language question
                response = copilot.ask(user_input)
                print(f"\n{response}\n")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {str(e)}\n")


if __name__ == "__main__":
    main()
