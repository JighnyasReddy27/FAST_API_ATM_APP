# app/schemas.py
from pydantic import BaseModel, Field
from typing import List

class AccountCreate(BaseModel):
    name: str
    balance: float = Field(default=0.0, ge=0.0)

class Transaction(BaseModel):
    account_id: int
    amount: float = Field(gt=0.0)

class Transfer(BaseModel):
    from_id: int
    to_id: int
    amount: float = Field(gt=0.0)

class BalanceResponse(BaseModel):
    account_id: int
    balance: float

class TransactionRecord(BaseModel):
    type: str
    amount: float
    timestamp: str

class MiniStatementResponse(BaseModel):
    account_id: int
    transactions: List[TransactionRecord]