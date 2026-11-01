from fastapi import FastAPI

# Object of FastAPI
app = FastAPI()

@app.get('/') # Output will be displayed in homepage
def greet():
    return {"hello learner"}

@app.get('/hello') #Output will be displayed in hello page
def greet():
    return {"hello this is hello page"}
