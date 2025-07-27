# tests/test_database.py
import pytest
import sqlite3
from datetime import date
from src.database import DatabaseManager
from src.models import Transaction

@pytest.fixture
def db_manager(tmp_path):
    db_path = tmp_path / "test.db"
    return DatabaseManager(str(db_path))

def test_initialize_db(db_manager):
    """Test table creation"""
    with sqlite3.connect(db_manager.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='transactions'")
        assert cursor.fetchone() is not None

def test_save_transactions(db_manager):
    """Test basic insertion"""
    transactions = [
        Transaction("t001", 101, date(2023, 1, 15), 125.50, "Groceries"),
        Transaction("t002", 102, date(2023, 2, 15), 200.00, "Electronics"),
    ]
    
    db_manager.save_transactions(transactions)
    
    with sqlite3.connect(db_manager.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM transactions")
        assert cursor.fetchone()[0] == 2

def test_duplicate_handling(db_manager):
    """Test duplicate prevention"""
    transactions = [
        Transaction("t001", 101, date(2023, 1, 15), 125.50, "Groceries"),
        Transaction("t001", 101, date(2023, 1, 15), 125.50, "Groceries"),
    ]
    
    db_manager.save_transactions(transactions)
    
    with sqlite3.connect(db_manager.db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM transactions")
        assert cursor.fetchone()[0] == 1