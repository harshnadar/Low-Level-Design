from typing import List, Dict
from decimal import Decimal
from src.strategies.split_strategy import SplitStrategy
from src.utils.validators import Validator

class EqualSplitStrategy(SplitStrategy):
    def calculate_splits(self, amount: Decimal, participants: List[str], 
                        splits: List[Decimal] = None) -> Dict[str, Decimal]:
        if not participants:
            return {}
        
        num_participants = len(participants)
        base_amount = amount / num_participants
        
        # Round to 2 decimal places
        base_amount = Validator.round_to_two_places(base_amount)
        
        result = {}
        total_assigned = Decimal('0')
        
        # Assign base amount to all except the first participant
        for i, participant in enumerate(participants[1:], 1):
            result[participant] = base_amount
            total_assigned += base_amount
        
        # Assign remaining amount to first participant to handle rounding
        result[participants[0]] = Validator.round_to_two_places(amount - total_assigned)
        
        return result