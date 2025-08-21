# app/crud.py

from database import get_connection
from datetime import datetime

# Helper function to log transactions
def _log_transaction(cur, account_id: int, type: str, amount: float):
    """Logs a transaction into the transactions table."""
    timestamp = datetime.now().isoformat()
    cur.execute(
        "INSERT INTO transactions (account_id, type, amount, timestamp) VALUES (?, ?, ?, ?)",
        (account_id, type, amount, timestamp)
    )

def create_account(name: str, balance: float = 0.0):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO accounts (name, balance) VALUES (?, ?)", (name, balance))
    conn.commit()
    account_id = cur.lastrowid
    conn.close()
    return account_id

def get_balance(account_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE id=?", (account_id,))
    row = cur.fetchone()
    conn.close()
    return row["balance"] if row else None

def deposit(account_id: int, amount: float):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE accounts SET balance = balance + ? WHERE id=?", (amount, account_id))
    _log_transaction(cur, account_id, "deposit", amount)
    conn.commit() # This line saves both the balance update and the transaction log
    conn.close()

def get_account_by_name(name: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, balance FROM accounts WHERE name=?", (name,))
    row = cur.fetchone()
    conn.close()
    return dict(row) if row else None

def withdraw(account_id: int, amount: float):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE id=?", (account_id,))
    row = cur.fetchone()
    if not row or row["balance"] < amount:
        conn.close()
        return False
    cur.execute("UPDATE accounts SET balance = balance - ? WHERE id=?", (amount, account_id))
    _log_transaction(cur, account_id, "withdraw", amount)
    conn.commit() # This line saves both the balance update and the transaction log
    conn.close()
    return True

def transfer(from_id: int, to_id: int, amount: float):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE id=?", (from_id,))
    row = cur.fetchone()
    if not row or row["balance"] < amount:
        conn.close()
        return False
        
    # Perform transfer and log both sides
    cur.execute("UPDATE accounts SET balance = balance - ? WHERE id=?", (amount, from_id))
    _log_transaction(cur, from_id, "transfer_out", amount) 
    
    cur.execute("UPDATE accounts SET balance = balance + ? WHERE id=?", (amount, to_id))
    _log_transaction(cur, to_id, "transfer_in", amount) 
    
    conn.commit() # This line saves all four database operations
    conn.close()
    return True

def get_transaction_history(account_id: int, limit: int = 5):
    if get_balance(account_id) is None:
        return None 
    conn = get_connection() 
    cur = conn.cursor()
    cur.execute(
        "SELECT type, amount, timestamp FROM transactions WHERE account_id = ? ORDER BY timestamp DESC LIMIT ?",
        (account_id, limit)
    )
    rows = cur.fetchall()
    history = [dict(row) for row in rows]
    conn.close()
    return history