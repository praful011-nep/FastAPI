from fastapi import FastAPI, HTTPException, Path, Query
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
def paginate_student(page:int, limit:int):
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