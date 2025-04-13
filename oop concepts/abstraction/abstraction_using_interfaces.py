"""
Why Use Interfaces?

- Promotes full abstraction (hides all implementation details).
- Provides a standard way for different classes to implement behaviors.
"""
from abc import ABC, abstractmethod

# Defining an interface
class Animal(ABC):
    @abstractmethod
    def make_sound(self):
        pass

# Implementing the interface in Dog class
class Dog(Animal):
    def make_sound(self):
        print("Dog barks")

# Implementing the interface in Cat class
class Cat(Animal):
    def make_sound(self):
        print("Cat meows")

if __name__ == "__main__":
    # Creating instances of Dog and Cat
    dog = Dog()
    cat = Cat()

    # Calling the make_sound method
    dog.make_sound()  # Output: Dog barks
    cat.make_sound()  # Output: Cat meows
