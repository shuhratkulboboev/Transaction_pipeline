import sqlite3
import logging
import os
from pathlib import Path
from typing import List, Optional
from .models import Transaction

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self, db_path: str = "db/transactions.db"):
        # Convert to absolute path to prevent path confusion
        self.db_path = os.path.abspath(db_path)
        logger.info(f"Database path: {self.db_path}")
        self._initialize_db()

    def _initialize_db(self):
        """Initialize the database with required tables"""
        Path(self.db_path).parent.mkdir(exist_ok=True)
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")  # Better concurrency
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS transactions (
                    transaction_id TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    transaction_date DATE NOT NULL,
                    amount REAL NOT NULL,
                    category TEXT NOT NULL
                )
            """)
            conn.commit()
            logger.info("Database initialized")

    def save_transactions(self, transactions: List[Transaction]):
        """Save cleaned transactions to database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            cursor = conn.cursor()
            
            # Verify connection is working
            test_count = cursor.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
            logger.debug(f"Pre-insert count: {test_count}")
            
            inserted = 0
            for transaction in transactions:
                try:
                    cursor.execute("""
                        INSERT OR IGNORE INTO transactions 
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        transaction.transaction_id,
                        transaction.user_id,
                        transaction.transaction_date.isoformat(),
                        transaction.amount,
                        transaction.category
                    ))
                    inserted += cursor.rowcount
                except sqlite3.Error as e:
                    logger.error(f"Error saving transaction {transaction.transaction_id}: {e}")
                    conn.rollback()
                    raise
            
            conn.commit()
            
            # Verify insertion
            new_count = cursor.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
            logger.info(f"Saved {inserted} transactions. Total now: {new_count}")

    def get_summary(self):
        """Get summary statistics from the database"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("PRAGMA journal_mode=WAL")
            cursor = conn.cursor()
            
            # First verify we can see data
            cursor.execute("SELECT COUNT(*) FROM transactions")
            total_transactions = cursor.fetchone()[0]
            logger.debug(f"Current transaction count: {total_transactions}")
            
            if total_transactions == 0:
                logger.warning("No transactions found in database")
            
            # Rest of your summary logic...
            cursor.execute("""
                SELECT category, SUM(amount), AVG(amount), COUNT(*)
                FROM transactions
                GROUP BY category
            """)
            category_stats = cursor.fetchall()
            
            cursor.execute("""
                SELECT MIN(transaction_date), MAX(transaction_date)
                FROM transactions
            """)
            min_date, max_date = cursor.fetchone()
            
            return {
                "total_transactions": total_transactions,
                "category_stats": [
                    {
                        "category": row[0],
                        "total_amount": row[1],
                        "average_amount": row[2],
                        "count": row[3]
                    }
                    for row in category_stats
                ],
                "date_range": (min_date, max_date)
            }