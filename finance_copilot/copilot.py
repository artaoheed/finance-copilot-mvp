"""
Main Finance Copilot interface with natural language processing.
"""

import os
from typing import List, Dict, Optional
from datetime import datetime
from .transaction import Transaction, TransactionType, TransactionCategory
from .analyzer import TransactionAnalyzer
from .forecaster import SpendingForecaster
from .budget_advisor import BudgetAdvisor

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class FinanceCopilot:
    """
    AI-powered financial assistant that provides natural language insights.
    """
    
    def __init__(
        self,
        transactions: List[Transaction],
        monthly_income: Optional[float] = None,
        api_key: Optional[str] = None,
        model: str = "gpt-3.5-turbo"
    ):
        """
        Initialize Finance Copilot.
        
        Args:
            transactions: List of Transaction objects
            monthly_income: Optional monthly income amount
            api_key: OpenAI API key (or set OPENAI_API_KEY env var)
            model: OpenAI model to use
        """
        self.transactions = transactions
        self.analyzer = TransactionAnalyzer(transactions)
        self.forecaster = SpendingForecaster(transactions)
        self.advisor = BudgetAdvisor(transactions, monthly_income)
        
        # Initialize OpenAI client if available
        self.openai_client = None
        self.model = model
        
        if OPENAI_AVAILABLE:
            api_key = api_key or os.getenv('OPENAI_API_KEY')
            if api_key:
                self.openai_client = OpenAI(api_key=api_key)
    
    def ask(self, question: str) -> str:
        """
        Ask the copilot a question in natural language.
        
        Args:
            question: Natural language question about finances
            
        Returns:
            Natural language response
        """
        # Get financial context
        context = self._build_context()
        
        # If OpenAI is available, use it for natural language response
        if self.openai_client:
            return self._ask_with_ai(question, context)
        else:
            # Fallback to rule-based responses
            return self._ask_rule_based(question, context)
    
    def get_summary(self) -> str:
        """
        Get a comprehensive financial summary.
        
        Returns:
            Natural language summary of financial situation
        """
        insights = self.analyzer.get_insights()
        recommendations = self.advisor.get_recommendations()
        alerts = self.advisor.get_spending_alerts()
        
        summary_parts = []
        
        # Overview
        summary_parts.append("=== Financial Summary ===\n")
        summary_parts.append(f"Total Transactions: {insights['total_transactions']}")
        summary_parts.append(f"Total Spent (30 days): ${insights['total_spent_30d']:.2f}")
        summary_parts.append(f"Total Income (30 days): ${insights['total_income_30d']:.2f}")
        summary_parts.append(f"Net Cashflow: ${insights['net_cashflow_30d']:.2f}\n")
        
        # Spending by category
        if insights['spending_by_category']:
            summary_parts.append("=== Spending by Category ===")
            for category, amount in sorted(
                insights['spending_by_category'].items(),
                key=lambda x: x[1],
                reverse=True
            ):
                summary_parts.append(f"  {category}: ${amount:.2f}")
            summary_parts.append("")
        
        # Top merchants
        if insights['top_merchants']:
            summary_parts.append("=== Top Merchants ===")
            for merchant, amount in insights['top_merchants']:
                summary_parts.append(f"  {merchant}: ${amount:.2f}")
            summary_parts.append("")
        
        # Alerts
        if alerts:
            summary_parts.append("=== Alerts ===")
            for alert in alerts:
                emoji = "⚠️" if alert['severity'] == 'high' else "ℹ️"
                summary_parts.append(f"  {emoji} {alert['title']}: {alert['message']}")
            summary_parts.append("")
        
        # Recommendations
        if recommendations:
            summary_parts.append("=== Recommendations ===")
            for i, rec in enumerate(recommendations, 1):
                summary_parts.append(f"  {i}. {rec}")
            summary_parts.append("")
        
        return "\n".join(summary_parts)
    
    def _build_context(self) -> Dict[str, any]:
        """Build financial context for AI queries."""
        insights = self.analyzer.get_insights()
        forecast = self.forecaster.forecast_monthly_spending()
        budget = self.advisor.get_recommended_budget()
        savings = self.advisor.get_savings_potential()
        
        return {
            'insights': insights,
            'forecast': forecast,
            'budget': budget,
            'savings': savings,
            'total_transactions': len(self.transactions),
        }
    
    def _ask_with_ai(self, question: str, context: Dict[str, any]) -> str:
        """
        Use OpenAI to answer questions.
        
        Args:
            question: User question
            context: Financial context
            
        Returns:
            AI-generated response
        """
        system_prompt = """You are a helpful financial advisor AI assistant. 
You analyze user transaction data and provide personalized financial insights and advice.
Be concise, friendly, and actionable in your responses.
Use the provided financial context to answer questions accurately."""
        
        user_prompt = f"""Financial Context:
{self._format_context(context)}

User Question: {question}

Please provide a helpful, concise answer based on the financial data."""
        
        try:
            response = self.openai_client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error communicating with AI: {str(e)}"
    
    def _ask_rule_based(self, question: str, context: Dict[str, any]) -> str:
        """
        Fallback rule-based question answering.
        
        Args:
            question: User question
            context: Financial context
            
        Returns:
            Rule-based response
        """
        question_lower = question.lower()
        insights = context['insights']
        
        # Spending-related queries
        if any(word in question_lower for word in ['spend', 'spent', 'expense']):
            if 'how much' in question_lower or 'total' in question_lower:
                return f"You spent ${insights['total_spent_30d']:.2f} in the last 30 days."
            elif 'category' in question_lower or 'categories' in question_lower:
                cats = insights['spending_by_category']
                response = "Your spending by category:\n"
                for cat, amount in sorted(cats.items(), key=lambda x: x[1], reverse=True):
                    response += f"  • {cat}: ${amount:.2f}\n"
                return response
            elif 'most' in question_lower:
                if insights['most_frequent_category']:
                    return f"You spend most frequently in: {insights['most_frequent_category']}"
        
        # Income-related queries
        if any(word in question_lower for word in ['income', 'earn', 'make']):
            return f"Your income in the last 30 days was ${insights['total_income_30d']:.2f}."
        
        # Savings-related queries
        if 'sav' in question_lower:
            savings = context['savings']
            return (f"Current savings: ${savings['current_monthly_savings']:.2f}/month "
                   f"(Recommended: ${savings['recommended_monthly_savings']:.2f})")
        
        # Budget-related queries
        if 'budget' in question_lower:
            budget = context['budget']
            if 'error' in budget:
                return budget['recommendation']
            return (f"Recommended monthly budget:\n"
                   f"  • Needs (50%): ${budget['needs']['budget']:.2f}\n"
                   f"  • Wants (30%): ${budget['wants']['budget']:.2f}\n"
                   f"  • Savings (20%): ${budget['savings']['budget']:.2f}")
        
        # Forecast-related queries
        if any(word in question_lower for word in ['forecast', 'predict', 'future']):
            forecast = context['forecast']
            return (f"Forecasted spending for next month: ${forecast['forecast_amount']:.2f} "
                   f"(Based on daily average of ${forecast['daily_average']:.2f})")
        
        # Default response
        return ("I can help you with:\n"
               "  • Spending analysis (how much did I spend?)\n"
               "  • Income tracking (what's my income?)\n"
               "  • Budget recommendations (what's my budget?)\n"
               "  • Savings goals (how much am I saving?)\n"
               "  • Spending forecasts (what will I spend next month?)")
    
    def _format_context(self, context: Dict[str, any]) -> str:
        """Format context for AI prompt."""
        insights = context['insights']
        forecast = context['forecast']
        
        parts = [
            f"Total Transactions: {context['total_transactions']}",
            f"Total Spent (30d): ${insights['total_spent_30d']:.2f}",
            f"Total Income (30d): ${insights['total_income_30d']:.2f}",
            f"Net Cashflow: ${insights['net_cashflow_30d']:.2f}",
            f"Forecasted Monthly Spending: ${forecast['forecast_amount']:.2f}",
        ]
        
        if insights['spending_by_category']:
            parts.append("\nSpending by Category:")
            for cat, amount in insights['spending_by_category'].items():
                parts.append(f"  {cat}: ${amount:.2f}")
        
        return "\n".join(parts)
