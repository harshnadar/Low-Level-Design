from typing import List, Dict
from decimal import Decimal
from src.strategies.split_strategy import SplitStrategy
from src.utils.validators import Validator
from src.exceptions.custom_exceptions import InvalidSplitException

class ExactSplitStrategy(SplitStrategy):
    def calculate_splits(self, amount: Decimal, participants: List[str], 
                        splits: List[Decimal] = None) -> Dict[str, Decimal]:
        if not splits or len(splits) != len(participants):
            raise InvalidSplitException("Exact splits must be provided for all participants")
        
        # Validate that splits sum to total amount
        Validator.validate_exact_split(amount, splits)
        
        result = {}
        for participant, split_amount in zip(participants, splits):
            result[participant] = Validator.round_to_two_places(split_amount)
        
        return result