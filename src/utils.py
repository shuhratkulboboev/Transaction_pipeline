import logging
from typing import List
from .models import Transaction

def setup_logging(log_level=logging.INFO):
    """Configure logging for the application"""
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def print_transactions(transactions: List[Transaction]):
    """Print list of transactions for debugging"""
    for t in transactions:
        print(f"{t.transaction_id}: {t.user_id} - {t.transaction_date} - ${t.amount:.2f} - {t.category}")