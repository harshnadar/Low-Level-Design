from decimal import Decimal
from typing import List
from src.exceptions.custom_exceptions import InvalidSplitException

class Validator:
    @staticmethod
    def validate_percent_split(splits: List[Decimal]) -> bool:
        total = sum(splits)
        if abs(total - Decimal('100')) > Decimal('0.01'):
            raise InvalidSplitException(f"Percentages must sum to 100, but got {total}")
        return True
    
    @staticmethod
    def validate_exact_split(amount: Decimal, splits: List[Decimal]) -> bool:
        total = sum(splits)
        if abs(total - amount) > Decimal('0.01'):
            raise InvalidSplitException(f"Exact amounts must sum to {amount}, but got {total}")
        return True
    
    @staticmethod
    def round_to_two_places(value: Decimal) -> Decimal:
        return value.quantize(Decimal('0.01'))