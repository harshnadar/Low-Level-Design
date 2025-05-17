from color import Color

class Player:
    def __init__(self, name: str, color: Color):
        self.name = name
        self.color = color

    def get_name(self) -> str:
        return self.name
    
    def get_color(self) -> Color:
        return self.color