#Encapsulation ensures that data cannot be directly accessed but must be retrieved or modified through methods.

class Employee:
    def __init__(self):
        self.__name = ""
        self.__age = 0

    # Getter method
    def get_name(self):
        return self.__name

    # Setter method
    def set_name(self, name):
        self.__name = name

    def get_age(self):
        return self.__age

    def set_age(self, age):
        if age > 18:
            self.__age = age
        else:
            print("Age must be greater than 18")

# Usage
emp = Employee()
emp.set_name("John Doe")
emp.set_age(25)
print("Employee Name:", emp.get_name())
print("Employee Age:", emp.get_age())