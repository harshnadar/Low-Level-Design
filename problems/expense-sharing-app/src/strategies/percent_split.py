from typing import List, Dict
from decimal import Decimal
from src.strategies.split_strategy import SplitStrategy
from src.utils.validators import Validator
from src.exceptions.custom_exceptions import InvalidSplitException

class PercentSplitStrategy(SplitStrategy):
    def calculate_splits(self, amount: Decimal, participants: List[str], 
                        splits: List[Decimal] = None) -> Dict[str, Decimal]:
        if not splits or len(splits) != len(participants):
            raise InvalidSplitException("Percentage splits must be provided for all participants")
        
        # Validate that percentages sum to 100
        Validator.validate_percent_split(splits)
        
        result = {}
        total_assigned = Decimal('0')
        
        # Calculate amounts for all except the last participant
        for i, (participant, percentage) in enumerate(zip(participants[:-1], splits[:-1])):
            split_amount = (amount * percentage) / Decimal('100')
            split_amount = Validator.round_to_two_places(split_amount)
            result[participant] = split_amount
            total_assigned += split_amount
        
        # Assign remaining amount to last participant to handle rounding
        result[participants[-1]] = Validator.round_to_two_places(amount - total_assigned)
        
        return result