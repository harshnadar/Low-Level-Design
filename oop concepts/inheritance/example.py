class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    
    def display_details(self):
        print(f"Employee: {self.name}, Salary: {self.salary}")

class Manager(Employee):
    def __init__(self, name, salary, bonus):
        super().__init__(name, salary)
        self.bonus = bonus
    
    def display_details(self):
        super().display_details()
        print(f"Bonus: {self.bonus}")