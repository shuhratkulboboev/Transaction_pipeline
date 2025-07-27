# Transaction Data Pipeline

A Python application that processes CSV transaction data, cleans it, and stores it in a SQLite database with a command-line interface.

## 📦 Features

- **CSV Processing**: Ingests transaction data from CSV files
- **Data Cleaning**:
  - Standardizes date formats to ISO (YYYY-MM-DD)
  - Removes transactions with negative/null amounts
  - Eliminates duplicate entries
- **Database Storage**: Stores cleaned data in SQLite
- **CLI Interface**: Simple command-line interaction
- **Testing**: Comprehensive unit and integration tests

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/transaction-pipeline.git
   cd transaction-pipeline
2. Create and activate virtual environment (Windows):
   ```bash
   python -m venv venv
   venv\Scripts\activate
3. Install dependencies::
   ```bash
   pip install -r requirements.txt
   # For development, also install:
   pip install -e .
## 🚀 Usage
Process CSV File:
```bash
   transaction-pipeline load data/transactions.csv
```
View Summary:
```bash
   transaction-pipeline summary
