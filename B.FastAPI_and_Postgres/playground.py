'''
Pyhton will interact with PostgreSQL directly without any FastAPI routes or endpoints
'''
import os
import psycopg
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, Column, String, Integer
from sqlalchemy.orm import DeclarativeBase
# Step-1 -> Get the URL from .env file

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
# print(DATABASE_URL)

#Step-2 -> Engine: The road to the database
engine = create_engine(DATABASE_URL)
# Check the version of postgres to verigy connection
with engine.connect() as conn:
    version = conn.execute(text("SELECT version()")).scalar()
    # print(f"Connected to {version.split(","[0])}")

#.all() -> every row
#.first() -> only the first row
#.scalar() -> only the first value of the first row

'''
DeclarativeBase -> SQLAlchemy's parent class that gives 'table powers'
We make our own Base once, every table inherits from it
Declartive : You declare(describe) what a table looks like
Base       : It's the Parent class everything else built on top of this.
'''
class Base(DeclarativeBase):
    pass

class StudentDB(Base):
    __tablename__ = 'student_records'
    id      = Column(String, primary_key=True)
    name    = Column(String(50), nullable=False)
    age     = Column(Integer, nullable=False)
    course  = Column(String(50), nullable=False)
    marks   = Column(Integer, nullable=False)
    email   = Column(String, unique=True, nullable=False)  

#bind = engine -> Attach to: Create the table inside this database
Base.metadata.create_all(bind=engine)
