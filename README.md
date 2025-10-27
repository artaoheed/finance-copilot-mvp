# Finance Copilot MVP

An AI-powered financial assistant that analyzes Cash App-style transaction history. It uses natural language to provide insights, forecast spending, and automate budgeting advice.

## Features

### Core Capabilities
- 📊 **Transaction Analysis**: Comprehensive analysis of spending patterns and income
- 🔮 **Spending Forecasting**: Predict future spending based on historical patterns
- 💰 **Budget Recommendations**: Automated budgeting advice using the 50/30/20 rule
- 🤖 **Natural Language Interface**: Ask questions about your finances in plain English
- 📈 **Spending Insights**: Category breakdowns, top merchants, and trends
- ⚠️ **Smart Alerts**: Warnings for unusual spending patterns
- 🔄 **Recurring Expense Detection**: Identify subscriptions and regular bills

### Analysis Features
- Total spending and income tracking
- Net cashflow calculation
- Spending breakdown by category
- Top merchant analysis
- Average transaction amounts
- Spending velocity and trends
- Largest expense identification

### Forecasting Features
- Monthly spending forecasts
- Category-specific predictions
- Next paycheck prediction
- Recurring expense identification
- Spending velocity tracking

### Budget Advisory Features
- 50/30/20 budget rule recommendations
- Category-specific budget allocations
- Savings potential analysis
- Spending alerts and warnings
- Personalized financial recommendations

## Installation

1. Clone the repository:
```bash
git clone https://github.com/artaoheed/finance-copilot-mvp.git
cd finance-copilot-mvp
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. (Optional) Set up OpenAI API for enhanced natural language processing:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Usage

### Command Line Interface

Run the interactive CLI with sample data:
```bash
python cli.py --demo
```

Show a financial summary:
```bash
python cli.py --demo --summary
```

Ask a specific question:
```bash
python cli.py --demo --ask "How much did I spend on groceries?"
```

Generate custom sample data:
```bash
python cli.py --demo --transactions 200 --days 120
```

### Interactive Mode

The CLI provides an interactive shell with the following commands:

- `summary` - Show comprehensive financial summary
- `insights` - Display key financial insights
- `forecast` - Show spending forecasts
- `budget` - Display budget recommendations
- `alerts` - Show spending alerts and warnings
- `ask <question>` - Ask any question in natural language
- `help` - Show available commands
- `quit` - Exit the application

Example session:
```
finance-copilot> summary
=== Financial Summary ===
Total Transactions: 175
Total Spent (30 days): $2,450.32
...

finance-copilot> ask How much am I spending on dining out?
You spent $285.50 on Food & Dining in the last 30 days.

finance-copilot> alerts
⚠️ [WARNING] Food & Dining Over Budget
   You're $85.50 over budget in Food & Dining (42.8% over).
```

### Python API

Use the Finance Copilot programmatically:

```python
from finance_copilot import FinanceCopilot, Transaction, TransactionType, TransactionCategory
from finance_copilot.sample_data import SampleDataGenerator
from datetime import datetime

# Generate sample data
transactions = SampleDataGenerator.generate_with_patterns(days_back=90)

# Initialize copilot
copilot = FinanceCopilot(transactions, monthly_income=3000.00)

# Get insights
insights = copilot.analyzer.get_insights()
print(f"Total spent: ${insights['total_spent_30d']:.2f}")

# Get forecast
forecast = copilot.forecaster.forecast_monthly_spending()
print(f"Forecasted spending: ${forecast['forecast_amount']:.2f}")

# Get budget recommendations
budget = copilot.advisor.get_recommended_budget()
print(f"Recommended needs budget: ${budget['needs']['budget']:.2f}")

# Ask natural language questions
response = copilot.ask("Am I overspending on entertainment?")
print(response)

# Get comprehensive summary
print(copilot.get_summary())
```

### Creating Custom Transactions

```python
from finance_copilot import Transaction, TransactionType, TransactionCategory
from datetime import datetime

# Create a transaction
transaction = Transaction(
    id="TXN001",
    date=datetime(2024, 1, 15, 10, 30),
    description="Coffee at Starbucks",
    amount=5.75,
    type=TransactionType.DEBIT,
    category=TransactionCategory.FOOD_DINING,
    merchant="Starbucks",
    status="completed"
)

# Build a transaction list and analyze
transactions = [transaction, ...]
copilot = FinanceCopilot(transactions)
```

## Architecture

### Core Components

1. **Transaction Model** (`transaction.py`)
   - Represents individual transactions
   - Supports both debit and credit types
   - 11 spending categories (Food & Dining, Groceries, Shopping, etc.)

2. **Transaction Analyzer** (`analyzer.py`)
   - Analyzes spending patterns
   - Calculates totals, averages, and trends
   - Identifies top merchants and categories

3. **Spending Forecaster** (`forecaster.py`)
   - Predicts future spending
   - Uses time-series analysis
   - Identifies recurring expenses

4. **Budget Advisor** (`budget_advisor.py`)
   - Provides budget recommendations
   - Implements 50/30/20 rule
   - Generates spending alerts

5. **Finance Copilot** (`copilot.py`)
   - Main interface combining all components
   - Natural language processing (with optional OpenAI integration)
   - Rule-based fallback for queries

6. **Sample Data Generator** (`sample_data.py`)
   - Generates realistic transaction data
   - Supports custom patterns
   - Useful for testing and demos

### Transaction Categories

- **Food & Dining**: Restaurants, cafes, food delivery
- **Groceries**: Supermarkets, grocery stores
- **Shopping**: General retail, online shopping
- **Entertainment**: Movies, concerts, subscriptions
- **Transportation**: Rideshare, gas, public transit
- **Bills & Utilities**: Rent, electricity, internet
- **Healthcare**: Medical, pharmacy, insurance
- **Personal**: Gym, salon, personal care
- **Transfer**: Money transfers
- **Income**: Paychecks, deposits
- **Other**: Uncategorized

## Testing

Run the test suite:
```bash
pytest
```

Run with coverage:
```bash
pytest --cov=finance_copilot --cov-report=html
```

Run specific test file:
```bash
pytest tests/test_analyzer.py
```

## Configuration

### Environment Variables

Create a `.env` file (copy from `.env.example`):

```env
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-3.5-turbo
```

**Note**: OpenAI integration is optional. The system works with rule-based responses if no API key is provided.

## Project Structure

```
finance-copilot-mvp/
├── finance_copilot/          # Main package
│   ├── __init__.py           # Package initialization
│   ├── transaction.py        # Transaction data model
│   ├── analyzer.py           # Transaction analysis engine
│   ├── forecaster.py         # Spending forecasting
│   ├── budget_advisor.py     # Budget recommendations
│   ├── copilot.py           # Main copilot interface
│   └── sample_data.py       # Sample data generator
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── test_transaction.py
│   ├── test_analyzer.py
│   ├── test_forecaster.py
│   ├── test_budget_advisor.py
│   └── test_copilot.py
├── cli.py                    # Command-line interface
├── requirements.txt          # Python dependencies
├── setup.py                  # Package setup
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

## Examples

### Example 1: Analyzing Spending Patterns

```python
from finance_copilot import FinanceCopilot
from finance_copilot.sample_data import SampleDataGenerator

# Generate 90 days of transaction history
transactions = SampleDataGenerator.generate_with_patterns(days_back=90)

# Create copilot
copilot = FinanceCopilot(transactions)

# Get spending by category
spending = copilot.analyzer.get_spending_by_category(30)
for category, amount in sorted(spending.items(), key=lambda x: x[1], reverse=True):
    print(f"{category}: ${amount:.2f}")
```

### Example 2: Forecasting Future Spending

```python
# Get monthly forecast
forecast = copilot.forecaster.forecast_monthly_spending()
print(f"Expected spending next month: ${forecast['forecast_amount']:.2f}")
print(f"Confidence: {forecast['confidence']}")

# Identify recurring expenses
recurring = copilot.forecaster.identify_recurring_expenses()
for expense in recurring:
    print(f"{expense['description']}: ${expense['average_amount']:.2f} every {expense['interval_days']} days")
```

### Example 3: Getting Budget Advice

```python
# Get budget recommendations
budget = copilot.advisor.get_recommended_budget()
print(f"Monthly Income: ${budget['monthly_income']:.2f}")
print(f"Needs (50%): ${budget['needs']['budget']:.2f}")
print(f"Wants (30%): ${budget['wants']['budget']:.2f}")
print(f"Savings (20%): ${budget['savings']['budget']:.2f}")

# Get personalized recommendations
recommendations = copilot.advisor.get_recommendations()
for i, rec in enumerate(recommendations, 1):
    print(f"{i}. {rec}")
```

### Example 4: Natural Language Queries

```python
# Ask questions in natural language
questions = [
    "How much did I spend last month?",
    "What are my top spending categories?",
    "Am I saving enough money?",
    "What will I spend next month?",
    "Do I have any recurring expenses?",
]

for question in questions:
    response = copilot.ask(question)
    print(f"Q: {question}")
    print(f"A: {response}\n")
```

## Development

### Adding New Features

1. **New Transaction Categories**: Edit `TransactionCategory` enum in `transaction.py`
2. **New Analysis Methods**: Add methods to `TransactionAnalyzer` class
3. **New Forecasting Algorithms**: Extend `SpendingForecaster` class
4. **Custom Budget Rules**: Modify `BudgetAdvisor` class

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## Future Enhancements

- [ ] Support for multiple data sources (CSV import, API integrations)
- [ ] More sophisticated forecasting models (ARIMA, Prophet)
- [ ] Goal tracking and progress monitoring
- [ ] Investment tracking and portfolio analysis
- [ ] Bill payment reminders
- [ ] Anomaly detection for fraud prevention
- [ ] Multi-currency support
- [ ] Data visualization and charts
- [ ] Mobile app interface
- [ ] Cloud storage and sync

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions, please visit the [GitHub repository](https://github.com/artaoheed/finance-copilot-mvp).

## Acknowledgments

- Built with Python, pandas, and NumPy
- Optional OpenAI integration for enhanced natural language processing
- Inspired by modern fintech applications like Cash App