# test/test_processor.py
import pytest
import sqlite3  # <-- Add this import
from pathlib import Path
from src.processor import DataProcessor
from src.database import DatabaseManager

@pytest.fixture
def test_db(tmp_path):
    """Creates a test database"""
    db_path = tmp_path / "test.db"
    return DatabaseManager(str(db_path))

def test_csv_to_database_flow(test_db):
    """Tests complete flow from CSV processing to database insertion"""
    csv_path = "data/transactions.csv"
    
    # Verify CSV exists
    assert Path(csv_path).exists(), f"CSV file not found at {csv_path}"
    
    # Process CSV
    processor = DataProcessor()
    transactions = processor.process_csv(csv_path)
    assert len(transactions) > 0, "No valid transactions processed"
    
    # Save to database
    test_db.save_transactions(transactions)
    
    # Verify database contents
    with sqlite3.connect(test_db.db_path) as conn:
        cursor = conn.cursor()
        
        # Check counts match
        cursor.execute("SELECT COUNT(*) FROM transactions")
        db_count = cursor.fetchone()[0]
        assert db_count == len(transactions), (
            f"Expected {len(transactions)} transactions, got {db_count}"
        )
        
        # Verify sample data
        cursor.execute("SELECT amount FROM transactions WHERE transaction_id = 't001'")
        assert cursor.fetchone()[0] == 125.50, "Transaction t001 amount mismatch"