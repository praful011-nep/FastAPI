"""
Need of Pydantic
- A normal accepts anything and noboady checks the data
"""
bad_student = {
    "name"  :"",
    "age"   :"Twenty",
    "marks" :150,
    "email" :"not-an-email"
}

from pydantic import BaseModel, Field, EmailStr, field_validator, computed_field
"""
Step 2 - BASEMODEL + TYPE HINTS
we describe a RECORD ONCE. Python checks every record against it.
"""
class SimpleStudent(BaseModel): #Pydantic Model
    name:str
    age: int
    marks: int
s = SimpleStudent(name = "Mark", age = '21', marks = 80)
# print(s.name, s.age, s.marks)

"""
Step 3 - FIELD() RULES
gt = greater than               lt = less than
ge = greater or equal           le = less or equal
"""
class RuleStudent(BaseModel):
    name    : str = Field(..., min_length=2, max_length=50)     #... = required
    age     : int = Field(..., gt=0, lt=100)                    #1 to 99
    marks   : int = Field(..., gt=0, le=100)                    #0 to 100
    course  : str = "Python"                                    #default value -> Python
    phone   : str | None = None                                 #Optional field can be empty
# s = RuleStudent(name= "Rohan Verma", age = 21, marks = 77)
# print(s.name)
# print(s.age)
# print(s.course)
# print(s.phone)
# print(s.marks)

"""
Step 4 - EMAILSTR
checks the text really looks like an email.
"""
class EmailStudent(BaseModel):
    name : str
    email: EmailStr

s = EmailStudent(name= "Thomas", email="thomas@gmail.com")
# print(s.name)
# print(s.email) # thomasatgmail.com: would give an error for invalid email


"""
Step 5 - FINAL STUDENT MODEL
1. field_validator  -> our OWN custom rule.
2. computed_field   -> a value Pydantic calculates for US.
"""

class Student(BaseModel):
    id: str = Field(..., examples=['S001'])
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=0, le=100)
    course: str = Field(..., max_length=50)
    marks: int  = Field(...,ge=0, le=100)
    email: EmailStr

    #Custom Rule: Name must contain letter and spaces
    @field_validator("name")
    @classmethod
    def check_name(cls, value): #value: name
        if not value.replace(" ","").isalpha():
            raise ValueError("Name must contain only letters and spaces")
        return value.title() #Capital first letter of word
    @computed_field #Pydantic will create by itself: value calculated from other field
    @property # Decorator (getter)
    def grade(self) -> str:
        if self.marks >= 90:
            return "A+"
        elif self.marks >= 80:
            return "A"
        elif self.marks >= 70:
            return "B"
        elif self.marks >= 60:
            return "C"
        else:
            return "F"


s = Student(id="S001",
            name = "Thomas Kent",
            age = 21,
            course="Python",
            marks=88,
            email="thomas@gmail.com")

# print(s.id)
# print(s.name)
# print(s.age)
# print(s.course)
# print(s.marks)
# print(s.grade) #Grade is automatically created and assigned by Pydantic
#Output
# S001
# Thomas Kent
# 21
# Python
# 88
# A


"""
Step 6 MODEL_DUMP()
turn a model back into Python dictionary (so that we can save it later)
"""

data = s.model_dump()
# print(data)
#Output
#{'id': 'S001', 'name': 'Thomas Kent', 'age': 21, 'course': 'Python', 'marks': 88, 'email': 'thomas@gmail.com', 'grade': 'A'
