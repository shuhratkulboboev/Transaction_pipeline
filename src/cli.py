import argparse
import logging
from pathlib import Path
from typing import Optional
from .database import DatabaseManager
from .processor import DataProcessor

logger = logging.getLogger(__name__)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def main():
    setup_logging()
    parser = argparse.ArgumentParser(description="Transaction Data Processing Pipeline")
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Load command
    load_parser = subparsers.add_parser('load', help='Load data from CSV to database')
    load_parser.add_argument('csv_file', help='Path to the CSV file')

    # Summary command
    summary_parser = subparsers.add_parser('summary', help='Show summary statistics')

    args = parser.parse_args()

    db_manager = DatabaseManager()
    processor = DataProcessor()

    if args.command == 'load':
        try:
            transactions = processor.process_csv(args.csv_file)
            db_manager.save_transactions(transactions)
            print(f"Successfully loaded {len(transactions)} transactions")
        except Exception as e:
            logger.error(f"Failed to load data: {e}")
            raise

    elif args.command == 'summary':
        try:
            summary = db_manager.get_summary()
            print("\nTransaction Summary:")
            print(f"Total Transactions: {summary['total_transactions']}")
            print(f"Date Range: {summary['date_range'][0]} to {summary['date_range'][1]}")
            
            print("\nCategory Statistics:")
            for stat in summary['category_stats']:
                print(f"{stat['category']}:")
                print(f"  Count: {stat['count']}")
                print(f"  Total Amount: {stat['total_amount']:.2f}")
                print(f"  Average Amount: {stat['average_amount']:.2f}\n")
        except Exception as e:
            logger.error(f"Failed to get summary: {e}")
            raise

if __name__ == "__main__":
    main()