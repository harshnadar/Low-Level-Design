"""
Key Characteristics of Association:
- Represents a uses-a or knows-a relationship.
- Objects in an association can exist independently.
- Can be unidirectional or bidirectional.
- Promotes modularity and code reusability.
"""

#A Student can be associated with multiple Teacher objects, and a Teacher can have multiple Student objects. This represents a many-to-many association.
class Teacher:
    def __init__(self, name):
        self.name = name
        self.students = []
    
    def add_student(self, student):
        self.students.append(student)
    
    def show_students(self):
        print(f"{self.name} teaches:")
        for student in self.students:
            print(f" - {student.name}")

class Student:
    def __init__(self, name):
        self.name = name

# Example Usage
if __name__ == "__main__":
    teacher1 = Teacher("Mr. Smith")
    teacher2 = Teacher("Mrs. Johnson")
    
    student1 = Student("Alice")
    student2 = Student("Bob")
    
    teacher1.add_student(student1)
    teacher1.add_student(student2)
    teacher2.add_student(student2)
    
    teacher1.show_students()
    teacher2.show_students()