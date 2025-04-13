"""
Key Characteristics of Aggregation:
- Represents a has-a relationship.
- The contained object can exist independently of the container.
- Implemented using references to objects.
- Promotes loose coupling between objects.

When to Use Aggregation?
- When an object can exist independently from the container.
- When designing loosely coupled systems.
- When different objects need to be shared across multiple containers.
- When following SOLID principles, particularly the Dependency Inversion Principle (DIP).
"""
class Professor:
    def __init__(self, name, subject):
        self.name = name
        self.subject = subject

    def teach(self):
        print(f"{self.name} is teaching {self.subject}")


class University:
    def __init__(self, university_name):
        self.university_name = university_name
        self.professors = []

    def add_professor(self, professor):
        self.professors.append(professor)

    def show_professors(self):
        print(f"Professors at {self.university_name}:")
        for professor in self.professors:
            print(f" - {professor.name}")


# Example Usage
if __name__ == "__main__":
    prof1 = Professor("Dr. Smith", "Computer Science")
    prof2 = Professor("Dr. Johnson", "Mathematics")
    
    university = University("Harvard University")
    university.add_professor(prof1)
    university.add_professor(prof2)
    
    university.show_professors()
    
    # Professors can exist independently
    prof1.teach()
    prof2.teach()
