from abc import ABC, abstractmethod
from typing import List, Dict
from decimal import Decimal

class SplitStrategy(ABC):
    @abstractmethod
    def calculate_splits(self, amount: Decimal, participants: List[str], 
                        splits: List[Decimal] = None) -> Dict[str, Decimal]:
        pass