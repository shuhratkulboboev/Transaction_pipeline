# test/test_integration.py
import pytest
import sqlite3  # <-- Add this import
from pathlib import Path
from src.processor import DataProcessor
from src.database import DatabaseManager

def test_real_data_pipeline():
    """End-to-end test with real data files"""
    csv_path = "data/transactions.csv"
    db_path = "db/transactions.db"
    
    # Clean up existing database
    Path(db_path).unlink(missing_ok=True)
    
    # Initialize
    processor = DataProcessor()
    db_manager = DatabaseManager(db_path)
    
    # Process and save
    transactions = processor.process_csv(csv_path)
    db_manager.save_transactions(transactions)
    
    # Verify
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM transactions")
        assert cursor.fetchone()[0] > 0, "No transactions found in database"
        
        # Additional verification
        cursor.execute("SELECT COUNT(*) FROM transactions WHERE amount <= 0")
        assert cursor.fetchone()[0] == 0, "Invalid amounts found"
        
        cursor.execute("SELECT transaction_date FROM transactions WHERE transaction_id = 't001'")
        assert cursor.fetchone()[0] == "2023-01-15", "Date format incorrect"