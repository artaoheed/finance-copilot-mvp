"""
Sample transaction data generator for testing and demonstration.
"""

import random
from datetime import datetime, timedelta
from typing import List
from .transaction import Transaction, TransactionType, TransactionCategory


class SampleDataGenerator:
    """
    Generates realistic sample transaction data for testing.
    """
    
    # Sample merchants by category
    MERCHANTS = {
        TransactionCategory.FOOD_DINING: [
            "Starbucks", "McDonald's", "Chipotle", "Subway", "Pizza Hut",
            "Domino's", "Local Cafe", "Thai Restaurant", "Sushi Bar"
        ],
        TransactionCategory.GROCERIES: [
            "Whole Foods", "Trader Joe's", "Safeway", "Walmart", "Target",
            "Costco", "Local Market"
        ],
        TransactionCategory.SHOPPING: [
            "Amazon", "Target", "Walmart", "Best Buy", "Apple Store",
            "Nike", "H&M", "Zara", "IKEA"
        ],
        TransactionCategory.ENTERTAINMENT: [
            "Netflix", "Spotify", "Movie Theater", "Concert Venue",
            "Bowling Alley", "Game Store", "Streaming Service"
        ],
        TransactionCategory.TRANSPORTATION: [
            "Uber", "Lyft", "Gas Station", "Public Transit", "Parking Meter",
            "Auto Repair Shop"
        ],
        TransactionCategory.BILLS_UTILITIES: [
            "Electric Company", "Water Utility", "Internet Provider",
            "Phone Company", "Rent Payment"
        ],
        TransactionCategory.HEALTHCARE: [
            "CVS Pharmacy", "Doctor's Office", "Dental Clinic", "Vision Center"
        ],
        TransactionCategory.PERSONAL: [
            "Gym Membership", "Hair Salon", "Spa", "Clothing Store"
        ],
    }
    
    # Typical amount ranges by category
    AMOUNT_RANGES = {
        TransactionCategory.FOOD_DINING: (5, 75),
        TransactionCategory.GROCERIES: (30, 200),
        TransactionCategory.SHOPPING: (15, 300),
        TransactionCategory.ENTERTAINMENT: (10, 150),
        TransactionCategory.TRANSPORTATION: (8, 60),
        TransactionCategory.BILLS_UTILITIES: (50, 300),
        TransactionCategory.HEALTHCARE: (20, 200),
        TransactionCategory.PERSONAL: (25, 150),
        TransactionCategory.INCOME: (1000, 5000),
    }
    
    @classmethod
    def generate_transactions(
        cls,
        num_transactions: int = 100,
        days_back: int = 90,
        include_income: bool = True
    ) -> List[Transaction]:
        """
        Generate sample transactions.
        
        Args:
            num_transactions: Number of transactions to generate
            days_back: How many days back to generate transactions
            include_income: Whether to include income transactions
            
        Returns:
            List of generated transactions
        """
        transactions = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        # Generate regular spending transactions
        for i in range(num_transactions):
            # Random date within range
            days_offset = random.randint(0, days_back)
            transaction_date = end_date - timedelta(days=days_offset)
            
            # Random category (exclude INCOME and TRANSFER)
            category = random.choice([
                TransactionCategory.FOOD_DINING,
                TransactionCategory.GROCERIES,
                TransactionCategory.SHOPPING,
                TransactionCategory.ENTERTAINMENT,
                TransactionCategory.TRANSPORTATION,
                TransactionCategory.BILLS_UTILITIES,
                TransactionCategory.HEALTHCARE,
                TransactionCategory.PERSONAL,
            ])
            
            # Random merchant from category
            merchant = random.choice(cls.MERCHANTS.get(category, ["Unknown Merchant"]))
            
            # Random amount within category range
            min_amt, max_amt = cls.AMOUNT_RANGES.get(category, (10, 100))
            amount = round(random.uniform(min_amt, max_amt), 2)
            
            transaction = Transaction(
                id=f"TXN{i+1:04d}",
                date=transaction_date,
                description=f"Purchase at {merchant}",
                amount=amount,
                type=TransactionType.DEBIT,
                category=category,
                merchant=merchant,
                status="completed"
            )
            
            transactions.append(transaction)
        
        # Add income transactions (typically bi-weekly)
        if include_income:
            # Add paychecks every 14 days
            current_date = start_date + timedelta(days=7)  # Start a week in
            while current_date <= end_date:
                min_amt, max_amt = cls.AMOUNT_RANGES[TransactionCategory.INCOME]
                amount = round(random.uniform(min_amt, max_amt), 2)
                
                transaction = Transaction(
                    id=f"INC{len(transactions)+1:04d}",
                    date=current_date,
                    description="Paycheck Deposit",
                    amount=amount,
                    type=TransactionType.CREDIT,
                    category=TransactionCategory.INCOME,
                    merchant="Employer",
                    status="completed"
                )
                
                transactions.append(transaction)
                current_date += timedelta(days=14)
        
        # Sort by date (oldest first)
        transactions.sort(key=lambda t: t.date)
        
        return transactions
    
    @classmethod
    def generate_with_patterns(cls, days_back: int = 90) -> List[Transaction]:
        """
        Generate transactions with realistic patterns.
        
        Args:
            days_back: How many days back to generate transactions
            
        Returns:
            List of generated transactions with patterns
        """
        transactions = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days_back)
        
        txn_id = 1
        
        # Add recurring bills (monthly)
        recurring_bills = [
            ("Rent Payment", 1200, TransactionCategory.BILLS_UTILITIES, "Landlord", 1),
            ("Internet Service", 60, TransactionCategory.BILLS_UTILITIES, "ISP Provider", 5),
            ("Phone Bill", 80, TransactionCategory.BILLS_UTILITIES, "Phone Company", 10),
            ("Gym Membership", 45, TransactionCategory.PERSONAL, "Fitness Center", 15),
            ("Streaming Services", 25, TransactionCategory.ENTERTAINMENT, "Netflix", 8),
        ]
        
        current_date = start_date
        while current_date <= end_date:
            for desc, amount, category, merchant, day_of_month in recurring_bills:
                if current_date.day == day_of_month:
                    transaction = Transaction(
                        id=f"TXN{txn_id:04d}",
                        date=current_date,
                        description=desc,
                        amount=amount,
                        type=TransactionType.DEBIT,
                        category=category,
                        merchant=merchant,
                        status="completed"
                    )
                    transactions.append(transaction)
                    txn_id += 1
            
            current_date += timedelta(days=1)
        
        # Add bi-weekly paychecks
        paycheck_date = start_date + timedelta(days=7)
        while paycheck_date <= end_date:
            transaction = Transaction(
                id=f"INC{txn_id:04d}",
                date=paycheck_date,
                description="Paycheck Deposit",
                amount=2500.00,
                type=TransactionType.CREDIT,
                category=TransactionCategory.INCOME,
                merchant="Employer Inc",
                status="completed"
            )
            transactions.append(transaction)
            txn_id += 1
            paycheck_date += timedelta(days=14)
        
        # Add variable spending
        variable_transactions = cls.generate_transactions(
            num_transactions=150,
            days_back=days_back,
            include_income=False
        )
        
        # Update IDs for variable transactions
        for t in variable_transactions:
            t.id = f"TXN{txn_id:04d}"
            txn_id += 1
        
        transactions.extend(variable_transactions)
        
        # Sort by date
        transactions.sort(key=lambda t: t.date)
        
        return transactions
