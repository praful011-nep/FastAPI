from fastapi import FastAPI
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
def get_id(student_id:str):
    data = laod_data()
    return data[student_id]