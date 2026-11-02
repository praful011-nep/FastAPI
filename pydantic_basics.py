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

from pydantic import BaseModel, Field, EmailStr
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
print(s.name)
print(s.email) # thomasatgmail.com: would give an error for invalid email

        
