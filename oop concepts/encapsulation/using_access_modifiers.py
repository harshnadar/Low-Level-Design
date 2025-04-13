"""
Encapsulation is one of the four fundamental principles of Object-Oriented Programming (OOP). 
It is the practice of bundling data (variables) and methods that operate on that data into a single unit (class) while restricting direct access to the internal details.

Encapsulation in Python is achieved using:
- Access Modifiers (public, _protected, __private)
- Getters and Setters
- Data Hiding
- Encapsulation helps in data protection, modularity, and maintainability of the code.


Python provides access modifiers to enforce encapsulation:
    public: Accessible from anywhere.
    _protected: Accessible within the class and subclasses.
    __private: Accessible only within the class.

"""

class BankAccount:
    def __init__(self, account_holder, balance):
        self.__account_holder = account_holder  # Private attribute
        self.__balance = balance  # Private attribute

    # Getter method to access balance
    def get_balance(self):
        return self.__balance

    # Setter method to modify balance
    def deposit(self, amount):
        if amount > 0:
            self.__balance += amount
            print(f"Deposited: {amount}")
        else:
            print("Invalid deposit amount")

# Usage
account = BankAccount("Alice", 1000)
print("Current Balance:", account.get_balance())
account.deposit(500)
print("Updated Balance:", account.get_balance())
