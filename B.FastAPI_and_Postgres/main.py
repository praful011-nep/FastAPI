import os
from fastapi import FastAPI, HTTPException, Path, Depends
from pydantic import BaseModel, Field, EmailStr, field_validator, computed_field, ConfigDict
from dotenv import load_dotenv
from sqlalchemy import create_engine, String, Integer, Column, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase, Session

# Part 1: Load DATABASE_URL from the .env file

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')
# print(DATABASE_URL)

# Part 2: Create the engine (connection to PostgreSQL)
engine = create_engine(DATABASE_URL)
with engine.connect() as conn:
    version = conn.execute(text("SELECT version()")).scalar()
    # print(f"Connected to {version.split(","[0])}")
# Part 3: Create SessionLocal and Base
class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(bind = engine)
db = SessionLocal()

Base.metadata.create_all(bind=engine)
# Part 4: Create the StudentDB table

class StudentDB(Base):
    __tablename__ = 'student_records'
    id      = Column(String, primary_key=True)
    name    = Column(String(50), nullable=False)
    age     = Column(Integer, nullable=False)
    course  = Column(String(50), nullable=False)
    marks   = Column(Integer, nullable=False)
    email   = Column(String, unique=True, nullable=False)  

# Part 5: Pydantic schemas for input (StudentCreate, StudentUpdate)

#Pydantic model
class StudentCreate(BaseModel):
    id: str = Field(..., examples=["S001"])
    name: str = Field(..., min_length=2, max_length=50)
    age: int = Field(..., gt=0, le=100)
    email: EmailStr
    course: str = Field(..., max_length=50)
    marks: int = Field(..., ge = 0, le=100)

    @field_validator("name")
    @classmethod
    def check_name(cls, value):
        if not value.replace(" ","").isalpha():
            raise ValueError("Name must contain only letters and spaces.")
        return value.title()

class StudentUpdate(BaseModel):
    id: str | None = Field(..., examples=["S001"])
    name: str | None = Field(..., min_length=2, max_length=50)
    age: int | None = Field(..., gt=0, le=100)
    email: EmailStr | None = None
    course: str | None = Field(..., max_length=50)
    marks: int | None= Field(..., ge = 0, le=100)
    @field_validator("name")
    @classmethod
    def check_name(cls, value):
        if not value.replace(" ","").isalpha():
            raise ValueError("Name must contain only letters and spaces.")
        return value.title()
    
# Part 6: Pydantic schemas for output (StudentResponse, StudentPage, Message)
#from_attributes=True lets Pydantic read student.marks (an object), not only student["marks"]
class StudentResponse(StudentCreate):
    model_config = ConfigDict(from_attributes=True)

    @computed_field
    @property
    def grade(self) -> str:
        if self.marks>=90:
            return "A+"
        elif self.marks>=80:
            return "A"
        elif self.marks>=70:
            return "B"
        elif self.marks>=60:
            return "C"
        else:
            return "F"


# Part 7: get_db() - one session per request
#   -Opens a session, gives it to the endpoint, always closes it,      replaces load_data/ save_data
# Opens a session, pauses at yield while the endpoint does its work and once completed its work the seeion will be closed.
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
# Part 8: Create the FastAPI app
app = FastAPI()

@app.get('/')
def home():
    return "HOME PAGE"
# Part 9: GET one student

#Depends(get_db) -> Before running the endpoint, run the get_db() and give me what it returns
#response_model -> what should the data look like
@app.get('/student/{student_id}', response_model=StudentResponse)
def get_student(
    student_id: str = Path(..., description="ID of Student"),
    db: Session = Depends(get_db)
):
    student = db.get(StudentDB, student_id)
    if student is None:
        raise HTTPException(
            status_code=404,
            detail=f"Student with id {student_id} not found"
        )
    return student

# Part 10: POST - create a student

# Part 11: PUT - update a student

# Part 12: DELETE - remove a student

# Part 13: GET all students (filter + sort + paginate)