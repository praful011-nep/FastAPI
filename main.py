from fastapi import FastAPI, HTTPException, Path, Query
from pydantic import BaseModel, field_validator, EmailStr, computed_field, Field
import json

# Object of FastAPI
app = FastAPI()

#Endpoint -> where on the URL the below message must be diplayed
@app.get('/') # Output will be displayed in homepage
def greet():
    return {"hello learner."}

@app.get('/hello') #Output will be displayed in hello page
def greet():
    return {"hello this is hello page."}

# HTTP Methods
# 1. GET: Just show message not change
# 2. POST: Can create
# 3. PUT: Add in existing data
# 4. DELETE: Delete record

@app.get("/hi")
def hello():
    return {"This is hello page"}

"""
Load JSON Data
1. Load: fetch data
2. Dump: Create data
"""

def laod_data():
    # Helper function
    with open("students.json", "r") as file:
        return json.load(file)

def save_data(data):
    with open("students.json",'w') as file:
        json.dump(data, file, indent=4) # indent = 4 keeps the file readable

@app.get('/student')
def student():
    return laod_data() 

"""
Path Parameters
- variable part of URL that points to one specific thing
"""
# student_id is path parameter
@app.get("/student/{student_id}") # /student/S001
def get_id(
    student_id:str = Path(..., description="The ID of the student", examples=['S001'])
    ):
    data = laod_data()
    if student_id not in data:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id '{student_id}' not found"
        )
    return data[student_id]

"""
Query Paramter
- Filter and sort the data using values after the ? in the URL
Example
http://127.0.0.1:8000/filter?course=Python
- ? -> after this query is present
- course=Python -> this is a key-value pair
"""

@app.get('/filter')
def filter_student(
    course:str = Query(None, description= "show only students in this course", examples=["Python"])
    ):
    data = laod_data()
    if course ==  None:
        return data

    filter = {} 
    for student_id, info, in data.items():
        if info['course'] == course:
            filter[student_id] = info

    return filter

"""
Sorting Data:
http://127.0.0.1:8000/sort?sort_by=marks,age,name&order=asc,desc

"""
SORT_FIELDS = ['marks', 'age','name']
SORT_ORDER = ['asc', 'desc']
@app.get('/sort')
def sort_students(
    sort_by: str = Query(None, description="Sort by marks, name, age", examples=['marks']),
    order: str = Query(None, description="asc or desc", examples=['asc', 'desc'])
):
    #If the given sort_by input dosn't belongs to any (marks, age, name) we will raise an error.
    if sort_by not in SORT_FIELDS:
        raise HTTPException(
            status_code= 404,
            detail= f"Invalid sort_by {sort_by}, Choose form {SORT_FIELDS}"
        )
    #If the given order input dosn't belongs to any (asc, desc) we will raise an error.
    if order not in SORT_ORDER:
        raise HTTPException(
            status_code= 404,
            detail=f"Invalid order, {order}, Choose form {SORT_ORDER}"
        )
    data = laod_data()

    #step-1 Turn the dictionary into a list, putting the ID inside each student
    student = []
    for student_id, info in data.items():
        info['id'] = student_id
        student.append(info)

    #Step-2 Sort the list by the choosen field
    reverse = (order == 'desc')
    sorted_students = sorted(student, key = lambda s: s[sort_by ], reverse = reverse)

    return sorted_students

"""
Pagination
page - which page you want
limit - how many records on one page
Formula:
start = (page - 1) * limit
end = start + limit
"""

@app.get('/paginate')
def paginate_student(page:int = Query(1, ge=1, description="Which page you want(start from 1)"),
                     limit:int = Query(2, ge=1, le=100, description="How many students on one page")):
    data = laod_data()

    #Turn the dictionary into a list and putting the id in each record
    student = []
    for student_id, info in data.items():
        info['id'] = student_id
        student.append(info)

    start = (page - 1)* limit
    end = start+limit
    page_student = student[start : end]
    total_student = len(student)

    return {
        "page": page,
        "limit": limit,
        "total_student": total_student,
        "student": page_student
    }


"""
REQUEST BODY

POST -> data comes in the BODY (a JSON Object sent with the request)

When a function argument is a Pydantic Model, FastAPI reads it from the body
and validates automatically, Bad Data -> 422
"""
class Student(BaseModel):
    """
    This class is responisble for validating the inputs given by user in POST
    """
    id      : str = Field(..., examples=["S001"])
    name    : str = Field(..., min_length=2, max_length=50)
    age     : int = Field(..., gt=0, le=100)
    course  : str = Field(..., max_length=50)
    marks   : int = Field(..., ge=0, le=100)
    email   : EmailStr

    #Custom Rule : Name must contain only letters and spaces
    @field_validator("name")#name=Kabir singh
    @classmethod
    def check_name(cls, value):
        if not value.replace(" ", "").isalpha():
            raise ValueError("Name must contain only letters and spaces")
        
        return value.title()

    @computed_field
    @property
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


@app.post('/create', status_code=201)
def create_student(student: Student):
    data = laod_data()

    if student.id in data:
        raise HTTPException(
            status_code=400, detail=f"Student with id {student.id} already exist"
        )

    data[student.id] = student.model_dump(exclude={'id','grade'})
    save_data(data)

    return {"message": "Student created successfully",
            'student':student}


class StudentUpdate(BaseModel):
    name   : str | None = Field(None, min_length=2, max_length=50)
    age    : int |None = Field(None, ge=0, lt=100)
    course : str |None = Field(None, max_length=50)
    marks  : int |None = Field(None, ge=0, le=100)
    email  : EmailStr | None=None
@app.put('/update/{student_id}')

def update_student(
    student_update: StudentUpdate,
    student_id: str = Path(..., description="The ID of the student", examples="S001")

):
    data = laod_data()

    if student_id not in data:
        raise HTTPException(
            status_code=404, detail=f"Student with id {student_id} not found"
        )
    #STEP1 : The student as it is right now.
    existing = data[student_id]

    #STEP2 : ONLY the fields the client actually sent
    update = student_update.model_dump()

    #STEP3: COPY the new value on the top of old one.
    for key, value in update.items():
        existing[key] = value

    #STEP4: Check the final student again
    student = Student(id = student_id, **existing)

    data[student_id] = student.model_dump(exclude=['id', 'grade'])
    save_data(data)

    return {"Message": "Student Updated Successfully", "student": student}