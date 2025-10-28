import pandas as pd
import random
from datetime import datetime, timedelta
import uuid
import numpy as np
import os

# --- Configuration ---
NUM_MONTHS = random.randint(6, 24)   # Generate 6–24 months of data
TX_PER_MONTH = random.randint(80, 150)
CURRENCY = "USD"

# Categories and merchants
CATEGORIES = {
    "Food": ["McDonald's", "Starbucks", "KFC", "Domino's Pizza", "Chipotle"],
    "Transport": ["Uber", "Lyft", "Shell Gas", "ExxonMobil"],
    "Entertainment": ["Netflix", "Spotify", "Steam", "YouTube Premium"],
    "Shopping": ["Amazon", "Walmart", "Target", "Best Buy"],
    "Bills": ["AT&T", "Comcast", "Verizon", "Electric Co."],
    "Groceries": ["Kroger", "Costco", "Whole Foods", "Aldi"],
    "Salary": ["Employer Inc."],
    "Transfers": ["Friend Transfer", "Cash App Refill"]
}

# Amount ranges per category
AMOUNT_RANGE = {
    "Food": (5, 40),
    "Transport": (10, 60),
    "Entertainment": (5, 25),
    "Shopping": (15, 200),
    "Bills": (50, 300),
    "Groceries": (20, 150),
    "Salary": (1500, 3000),
    "Transfers": (10, 150)
}

def random_date(start, end):
    """Return a random datetime between start and end."""
    delta = end - start
    random_days = random.randrange(delta.days)
    return start + timedelta(days=random_days)

def generate_transactions():
    end_date = datetime.today()
    start_date = end_date - timedelta(days=NUM_MONTHS * 30)

    data = []
    for _ in range(NUM_MONTHS * TX_PER_MONTH):
        category = random.choices(
            list(CATEGORIES.keys()),
            weights=[20, 15, 10, 15, 10, 10, 5, 5],
            k=1
        )[0]

        merchant = random.choice(CATEGORIES[category])
        amount = round(random.uniform(*AMOUNT_RANGE[category]), 2)
        tx_type = "credit" if category == "Salary" else "debit"
        date = random_date(start_date, end_date).strftime("%Y-%m-%d")
        tx_id = str(uuid.uuid4())[:8]
        description = f"{category} payment at {merchant}"

        data.append({
            "tx_id": tx_id,
            "date": date,
            "amount": amount,
            "currency": CURRENCY,
            "merchant": merchant,
            "category": category,
            "description": description,
            "type": tx_type
        })

    df = pd.DataFrame(data)
    df.sort_values(by="date", inplace=True)
    return df

if __name__ == "__main__":
    os.makedirs("data", exist_ok=True)
    df = generate_transactions()
    output_file = "data/sample_transactions.csv"
    df.to_csv(output_file, index=False)
    print(f"✅ Generated {len(df)} transactions over {NUM_MONTHS} months and saved to {output_file}")




























# import csv, random, datetime as dt # For generating sample data

# merchants = ['Uber','Starbucks','Amazon','Netflix','McDonald\'s','Apple','Shell','Spotify','Walmart','Lyft'] # Sample merchants
# categories = ['Transport','Food','Shopping','Entertainment','Salary','Groceries'] # Sample categories

# def generate(n=120, start_date=dt.date(2024,10,1)): # Generate n sample transactions
#     rows = []
#     for i in range(1, n+1):
#         date = start_date + dt.timedelta(days=random.randint(0,330)) # Random date within ~11 months
#         merchant = random.choice(merchants) # Random merchant
#         category = random.choice(categories) # Random category
#         amt = round(random.uniform(3,300),2) # Random amount
#         ttype = 'debit' if category != 'Salary' else 'credit' # Determine type
#         if ttype == 'credit':
#             amt = round(random.uniform(1000,4000),2)
#         rows.append([i, date.isoformat(), amt, 'USD', merchant, category, 'auto-generated', ttype]) # Append row to list
#     return rows

# if __name__ == '__main__': # If run as script, generate and write sample CSV
#     rows = generate(200) # Generate 200 transactions
#     with open('data/sample_generated_transactions.csv', 'w', newline='') as f: # Write to CSV file
#         w = csv.writer(f)
#         w.writerow(['tx_id','date','amount','currency','merchant','category','description','type'])
#         w.writerows(rows)
#     print('Wrote data/sample_generated_transactions.csv')
