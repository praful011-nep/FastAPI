import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, String, Integer, Column
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Part 1: Load DATABASE_URL from the .env file

load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')

# Part 2: Create the engine (connection to PostgreSQL)
engine = create_engine(DATABASE_URL)

# Part 3: Create SessionLocal and Base
class Base(DeclarativeBase):
    pass

SessionLocal = sessionmaker(DATABASE_URL)
db = SessionLocal()

Base.metadata.create_all(bind=engine)
# Part 4: Create the StudentDB table
class StudentDB(Base):
    __tablename__ = 'courses'
    id = Column(String, primary_key=True)
    cname = Column(String(50), nullable=False)
    price = Column(Integer, nullable=False)
    
# Part 5: Pydantic schemas for input (StudentCreate, StudentUpdate)

# Part 6: Pydantic schemas for output (StudentResponse, StudentPage, Message)

# Part 7: get_db() - one session per request

# Part 8: Create the FastAPI app

# Part 9: GET one student

# Part 10: POST - create a student

# Part 11: PUT - update a student

# Part 12: DELETE - remove a student

# Part 13: GET all students (filter + sort + paginate)