import pytest
from decimal import Decimal
from src.strategies.equal_split import EqualSplitStrategy
from src.strategies.exact_split import ExactSplitStrategy
from src.strategies.percent_split import PercentSplitStrategy
from src.exceptions.custom_exceptions import InvalidSplitException

class TestSplitStrategies:
    def test_equal_split_basic(self):
        strategy = EqualSplitStrategy()
        amount = Decimal('100')
        participants = ['u1', 'u2', 'u3']
        
        splits = strategy.calculate_splits(amount, participants)
        
        assert len(splits) == 3
        assert splits['u1'] == Decimal('33.34')
        assert splits['u2'] == Decimal('33.33')
        assert splits['u3'] == Decimal('33.33')
        assert sum(splits.values()) == amount
    
    def test_equal_split_two_users(self):
        strategy = EqualSplitStrategy()
        amount = Decimal('100')
        participants = ['u1', 'u2']
        
        splits = strategy.calculate_splits(amount, participants)
        
        assert splits['u1'] == Decimal('50.00')
        assert splits['u2'] == Decimal('50.00')
    
    def test_exact_split_valid(self):
        strategy = ExactSplitStrategy()
        amount = Decimal('1250')
        participants = ['u1', 'u2']
        split_amounts = [Decimal('370'), Decimal('880')]
        
        splits = strategy.calculate_splits(amount, participants, split_amounts)
        
        assert splits['u1'] == Decimal('370.00')
        assert splits['u2'] == Decimal('880.00')
    
    def test_exact_split_invalid_sum(self):
        strategy = ExactSplitStrategy()
        amount = Decimal('1000')
        participants = ['u1', 'u2']
        split_amounts = [Decimal('400'), Decimal('500')]
        
        with pytest.raises(InvalidSplitException):
            strategy.calculate_splits(amount, participants, split_amounts)
    
    def test_percent_split_valid(self):
        strategy = PercentSplitStrategy()
        amount = Decimal('1200')
        participants = ['u1', 'u2', 'u3', 'u4']
        percentages = [Decimal('40'), Decimal('20'), Decimal('20'), Decimal('20')]
        
        splits = strategy.calculate_splits(amount, participants, percentages)
        
        assert splits['u1'] == Decimal('480.00')
        assert splits['u2'] == Decimal('240.00')
        assert splits['u3'] == Decimal('240.00')
        assert splits['u4'] == Decimal('240.00')
        assert sum(splits.values()) == amount
    
    def test_percent_split_invalid_sum(self):
        strategy = PercentSplitStrategy()
        amount = Decimal('1000')
        participants = ['u1', 'u2']
        percentages = [Decimal('60'), Decimal('50')]
        
        with pytest.raises(InvalidSplitException):
            strategy.calculate_splits(amount, participants, percentages)
    
    def test_percent_split_with_rounding(self):
        strategy = PercentSplitStrategy()
        amount = Decimal('100')
        participants = ['u1', 'u2', 'u3']
        percentages = [Decimal('33.33'), Decimal('33.33'), Decimal('33.34')]
        
        splits = strategy.calculate_splits(amount, participants, percentages)
        
        assert sum(splits.values()) == amount