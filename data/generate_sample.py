"""
generate_sample_v2.py
---------------------
Enhanced sample data generator for the Finance Copilot project.
- Adds seasonality and realistic spending patterns
- Includes user-like transaction behavior (salary, bills, leisure)
- Supports optional location/currency
"""

import pandas as pd
import random
from datetime import datetime, timedelta
import uuid
import numpy as np
import os

# --- Configuration ---
NUM_MONTHS = random.randint(12, 24)   # Generate between 1–2 years of data
TX_PER_MONTH = random.randint(100, 200)
CURRENCY = random.choice(["USD", "EUR", "GBP", "NGN"])  # Randomized currency
USER_LOCATION = random.choice(["New York", "London", "Lagos", "Berlin", "Toronto"])

# Categories and merchants
CATEGORIES = {
    "Food": ["McDonald's", "Starbucks", "KFC", "Domino's Pizza", "Chipotle", "Subway"],
    "Transport": ["Uber", "Lyft", "Bolt", "Shell Gas", "ExxonMobil", "TotalEnergies"],
    "Entertainment": ["Netflix", "Spotify", "Steam", "YouTube Premium", "Disney+"],
    "Shopping": ["Amazon", "Walmart", "Target", "Best Buy", "AliExpress"],
    "Bills": ["AT&T", "Comcast", "Verizon", "Electric Co.", "Water Utility"],
    "Groceries": ["Kroger", "Costco", "Whole Foods", "Aldi", "Shoprite"],
    "Salary": ["Employer Inc.", "Company Ltd."],
    "Transfers": ["Friend Transfer", "Cash App Refill", "Peer Payment"]
}

# Amount ranges per category
AMOUNT_RANGE = {
    "Food": (5, 40),
    "Transport": (10, 80),
    "Entertainment": (5, 30),
    "Shopping": (20, 300),
    "Bills": (80, 400),
    "Groceries": (30, 200),
    "Salary": (1500, 4000),
    "Transfers": (10, 200)
}

# --- Helper Functions ---
def random_date_in_month(year: int, month: int) -> datetime:
    """Generate a random date within a given month."""
    start = datetime(year, month, 1)
    if month == 12:
        end = datetime(year + 1, 1, 1)
    else:
        end = datetime(year, month + 1, 1)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days - 1))

def seasonal_multiplier(month: int) -> float:
    """Simulate seasonality (e.g., higher shopping in December)."""
    # Slight increase around festive months
    if month in [11, 12]:
        return 1.25
    elif month in [6, 7, 8]:  # Summer spending
        return 1.1
    else:
        return 1.0

def generate_transactions():
    end_date = datetime.today()
    start_date = end_date - timedelta(days=NUM_MONTHS * 30)

    data = []
    current = start_date

    for i in range(NUM_MONTHS):
        current_month = (start_date + timedelta(days=i * 30)).month
        current_year = (start_date + timedelta(days=i * 30)).year

        for _ in range(TX_PER_MONTH):
            category = random.choices(
                list(CATEGORIES.keys()),
                weights=[20, 15, 10, 15, 10, 10, 5, 5],
                k=1
            )[0]

            merchant = random.choice(CATEGORIES[category])
            base_amount = random.uniform(*AMOUNT_RANGE[category])
            amount = round(base_amount * seasonal_multiplier(current_month), 2)
            tx_type = "credit" if category == "Salary" else "debit"
            date = random_date_in_month(current_year, current_month).strftime("%Y-%m-%d")
            tx_id = str(uuid.uuid4())[:8]
            description = f"{category} payment at {merchant} ({USER_LOCATION})"

            # Add some noise for realism (e.g., weekends cheaper)
            if category != "Salary" and random.random() < 0.3:
                amount *= random.uniform(0.8, 1.05)
                amount = round(amount, 2)

            data.append({
                "tx_id": tx_id,
                "date": date,
                "amount": amount,
                "currency": CURRENCY,
                "merchant": merchant,
                "category": category,
                "description": description,
                "type": tx_type,
                "location": USER_LOCATION
            })

    df = pd.DataFrame(data)
    df.sort_values(by="date", inplace=True)

    # Simulate salary at start of month (positive credits)
    df.loc[df["category"] == "Salary", "amount"] = df.loc[df["category"] == "Salary", "amount"].abs()

    return df


if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = generate_transactions()
    output_file = "data/sample_transactions_v2.csv"
    df.to_csv(output_file, index=False)
    print(f"✅ Generated {len(df)} transactions across {NUM_MONTHS} months in {USER_LOCATION}")
    print(f"📁 Saved to {output_file}")
