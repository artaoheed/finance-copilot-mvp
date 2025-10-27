"""
Transaction data model for Cash App-style transactions.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional
import json


class TransactionCategory(Enum):
    """Categories for transactions similar to Cash App."""
    
    FOOD_DINING = "Food & Dining"
    GROCERIES = "Groceries"
    SHOPPING = "Shopping"
    ENTERTAINMENT = "Entertainment"
    TRANSPORTATION = "Transportation"
    BILLS_UTILITIES = "Bills & Utilities"
    HEALTHCARE = "Healthcare"
    PERSONAL = "Personal"
    TRANSFER = "Transfer"
    INCOME = "Income"
    OTHER = "Other"


class TransactionType(Enum):
    """Type of transaction."""
    
    DEBIT = "debit"  # Money out
    CREDIT = "credit"  # Money in


@dataclass
class Transaction:
    """
    Represents a single transaction in Cash App style.
    
    Attributes:
        id: Unique transaction identifier
        date: Date and time of transaction
        description: Transaction description
        amount: Transaction amount (positive for all, type determines direction)
        type: Transaction type (debit or credit)
        category: Transaction category
        merchant: Merchant or recipient name
        status: Transaction status (completed, pending, failed)
        notes: Optional user notes
    """
    
    id: str
    date: datetime
    description: str
    amount: float
    type: TransactionType
    category: TransactionCategory = TransactionCategory.OTHER
    merchant: Optional[str] = None
    status: str = "completed"
    notes: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert transaction to dictionary."""
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "description": self.description,
            "amount": self.amount,
            "type": self.type.value,
            "category": self.category.value,
            "merchant": self.merchant,
            "status": self.status,
            "notes": self.notes,
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> "Transaction":
        """Create transaction from dictionary."""
        return cls(
            id=data["id"],
            date=datetime.fromisoformat(data["date"]),
            description=data["description"],
            amount=data["amount"],
            type=TransactionType(data["type"]),
            category=TransactionCategory(data["category"]),
            merchant=data.get("merchant"),
            status=data.get("status", "completed"),
            notes=data.get("notes"),
        )
    
    def __str__(self) -> str:
        """String representation of transaction."""
        sign = "+" if self.type == TransactionType.CREDIT else "-"
        return f"{self.date.strftime('%Y-%m-%d')} | {sign}${self.amount:.2f} | {self.description} | {self.category.value}"
