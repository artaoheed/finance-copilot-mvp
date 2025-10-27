import csv, random, datetime as dt # For generating sample data

merchants = ['Uber','Starbucks','Amazon','Netflix','McDonald\'s','Apple','Shell','Spotify','Walmart','Lyft'] # Sample merchants
categories = ['Transport','Food','Shopping','Entertainment','Salary','Groceries'] # Sample categories

def generate(n=120, start_date=dt.date(2024,10,1)): # Generate n sample transactions
    rows = []
    for i in range(1, n+1):
        date = start_date + dt.timedelta(days=random.randint(0,330)) # Random date within ~11 months
        merchant = random.choice(merchants) # Random merchant
        category = random.choice(categories) # Random category
        amt = round(random.uniform(3,300),2) # Random amount
        ttype = 'debit' if category != 'Salary' else 'credit' # Determine type
        if ttype == 'credit':
            amt = round(random.uniform(1000,4000),2)
        rows.append([i, date.isoformat(), amt, 'USD', merchant, category, 'auto-generated', ttype]) # Append row to list
    return rows

if __name__ == '__main__': # If run as script, generate and write sample CSV
    rows = generate(200) # Generate 200 transactions
    with open('data/sample_generated_transactions.csv', 'w', newline='') as f: # Write to CSV file
        w = csv.writer(f)
        w.writerow(['tx_id','date','amount','currency','merchant','category','description','type'])
        w.writerows(rows)
    print('Wrote data/sample_generated_transactions.csv')
