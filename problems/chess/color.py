from enum import Enum

class Color(Enum):
    BLACK = 1
    WHITE = 2

    @property
    def name_str(self)-> str:
        return self.name[0].upper()