# backend/routes/transactions.py
from fastapi import APIRouter, Query
from backend.routes.upload import transactions_db

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.get("")
def get_transactions(skip: int = 0, limit: int = 10):
    return {
        "total": len(transactions_db),
        "transactions": transactions_db[skip: skip + limit]
    }
