# app/crud.py
from database import get_connection


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
    conn.commit()
    conn.close()


def withdraw(account_id: int, amount: float):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE id=?", (account_id,))
    row = cur.fetchone()
    if not row or row["balance"] < amount:
        conn.close()
        return False
    cur.execute("UPDATE accounts SET balance = balance - ? WHERE id=?", (amount, account_id))
    conn.commit()
    conn.close()
    return True


def transfer(from_id: int, to_id: int, amount: float):
    conn = get_connection()
    cur = conn.cursor()

    # check balance
    cur.execute("SELECT balance FROM accounts WHERE id=?", (from_id,))
    row = cur.fetchone()
    if not row or row["balance"] < amount:
        conn.close()
        return False

    # perform transfer
    cur.execute("UPDATE accounts SET balance = balance - ? WHERE id=?", (amount, from_id))
    cur.execute("UPDATE accounts SET balance = balance + ? WHERE id=?", (amount, to_id))
    conn.commit()
    conn.close()
    return True
