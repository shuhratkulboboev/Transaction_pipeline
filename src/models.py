from dataclasses import dataclass
from datetime import date

@dataclass
class Transaction:
    transaction_id: str
    user_id: int
    transaction_date: date
    amount: float
    category: str