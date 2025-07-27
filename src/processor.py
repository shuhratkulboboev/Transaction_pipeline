import csv
import logging
from datetime import datetime
from typing import List, Optional
from pathlib import Path
from .models import Transaction

logger = logging.getLogger(__name__)

class DataProcessor:
    def __init__(self):
        self.seen_ids = set()

    def process_csv(self, file_path: str) -> List[Transaction]:
        """Process CSV file and return cleaned transactions"""
        if not Path(file_path).exists():
            raise FileNotFoundError(f"CSV file not found: {file_path}")

        transactions = []
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                try:
                    transaction = self._clean_row(row)
                    if transaction:
                        transactions.append(transaction)
                except Exception as e:
                    logger.error(f"Error processing row {row}: {e}")
        
        logger.info(f"Processed {len(transactions)} valid transactions from {file_path}")
        return transactions

    def _clean_row(self, row: dict) -> Optional[Transaction]:
        """Clean and validate a single row of data"""
        # Check for duplicates
        if row['transaction_id'] in self.seen_ids:
            logger.warning(f"Duplicate transaction_id: {row['transaction_id']}")
            return None
        self.seen_ids.add(row['transaction_id'])

        # Validate amount
        try:
            amount = float(row['amount'])
            if amount <= 0:
                logger.warning(f"Invalid amount {amount} for transaction {row['transaction_id']}")
                return None
        except (ValueError, TypeError):
            logger.warning(f"Missing or invalid amount for transaction {row['transaction_id']}")
            return None

        # Parse date (try multiple formats)
        date_formats = ["%Y-%m-%d", "%d/%m/%Y", "%m-%d-%Y"]
        transaction_date = None
        
        for date_format in date_formats:
            try:
                transaction_date = datetime.strptime(row['transaction_date'], date_format).date()
                break
            except ValueError:
                continue
        
        if not transaction_date:
            logger.warning(f"Invalid date format for transaction {row['transaction_id']}: {row['transaction_date']}")
            return None

        # Validate user_id
        try:
            user_id = int(row['user_id'])
        except ValueError:
            logger.warning(f"Invalid user_id for transaction {row['transaction_id']}")
            return None

        # Validate category
        category = row['category'].strip()
        if not category:
            logger.warning(f"Empty category for transaction {row['transaction_id']}")
            return None

        return Transaction(
            transaction_id=row['transaction_id'],
            user_id=user_id,
            transaction_date=transaction_date,
            amount=amount,
            category=category
        )