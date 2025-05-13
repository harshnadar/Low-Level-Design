from interfaces import Beverage, DarkRoast
from decorator_base_class import CondimentDecorator
from concrete_decorators import Mocha, Whip


def func():
    # Create base beverage
    coffee: Beverage = DarkRoast()

    # Decorate with condiments
    coffee = Mocha(coffee)  # Wrap in Mocha
    coffee = Whip(coffee)   # Wrap in Whip

    print(coffee.get_description()) 
    # Output: "Dark Roast Coffee, Mocha, Whip"
    print(f"Total cost: ${coffee.cost():.2f}")  
    # Output: "Total cost: $3.87"

if __name__ == "__main__":
    func()