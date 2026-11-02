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

from pydantic import BaseModel
"""
Step 2 - BASEMODEL + TYPE HINTS
we describe a RECORD ONCE. Python checks every record against it.
"""
class SimpleStudent(BaseModel): #Pydantic Model
    name:str
    age: int
    marks: int
s = SimpleStudent(name = "Mark", age = 21, marks = 80)
print(s.name, s.age, s.marks)