# app/main.py
from fastapi import FastAPI, HTTPException
import database
import crud
import schemas

app = FastAPI(title="ATM API")

# Initialize DB
database.init_db()


@app.post("/account/")
def create_account(account: schemas.AccountCreate):
    account_id = crud.create_account(account.name, account.balance)
    return {"message": "Account created", "account_id": account_id}


@app.get("/balance/{account_id}", response_model=schemas.BalanceResponse)
def get_balance(account_id: int):
    balance = crud.get_balance(account_id)
    if balance is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"account_id": account_id, "balance": balance}


@app.post("/deposit/")
def deposit(transaction: schemas.Transaction):
    if crud.get_balance(transaction.account_id) is None:
        raise HTTPException(status_code=404, detail="Account not found")
    crud.deposit(transaction.account_id, transaction.amount)
    return {"message": "Deposit successful"}


@app.post("/withdraw/")
def withdraw(transaction: schemas.Transaction):
    success = crud.withdraw(transaction.account_id, transaction.amount)
    if not success:
        raise HTTPException(status_code=400, detail="Insufficient balance or account not found")
    return {"message": "Withdrawal successful"}


@app.post("/transfer/")
def transfer(transfer: schemas.Transfer):
    success = crud.transfer(transfer.from_id, transfer.to_id, transfer.amount)
    if not success:
        raise HTTPException(status_code=400, detail="Transfer failed (check balance or accounts)")
    return {"message": "Transfer successful"}


@app.get("/account/{name}")
def get_account_by_name(name: str):
    account = crud.get_account_by_name(name)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {
        "account_id": account["id"],
        "name": account["name"],
        "balance": account["balance"]
    }

@app.get("/welcome")
def welcome_message():
    return {"message": "Welcome to the ATM!"}

@app.get("/ministatement/{account_id}", response_model=schemas.MiniStatementResponse)
def get_mini_statement(account_id: int):
    """
    Provides a mini statement with the last 5 transactions for an account.
    """
    history = crud.get_transaction_history(account_id)
    
    if history is None:
        raise HTTPException(status_code=404, detail="Account not found")
        
    return {"account_id": account_id, "transactions": history}
