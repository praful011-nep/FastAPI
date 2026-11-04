'''
Pyhton will interact with PostgreSQL directly without any FastAPI routes or endpoints
'''
import os
import psycopg
from dotenv import load_dotenv
from sqlalchemy import create_engine, text, Column, String, Integer
from sqlalchemy.orm import DeclarativeBase, sessionmaker
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

#Step 4: Session = One Visit, Open, Do work, Commit, Close
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

# Create a new data
#.get(Model, primary_key) -> retrieves a data using its primary key
#.add() -> creates a object in current session(not permanently saved in database)
#.commit() -> permanently adds to the database from session
if db.get(StudentDB, "S001") is None:
    db.add(StudentDB(id= "S001",
                    name = "Mark",
                    age = 25, 
                    course = "Python", 
                    marks = 80, 
                    email = 'mark@example.com'))
    db.commit()

if db.get(StudentDB, "S002") is None:
    db.add(StudentDB(id= "S002",
                    name = "Chris",
                    age = 24, 
                    course = "AI/ML", 
                    marks = 89, 
                    email = 'chris@example.com'))
    db.commit()
#Read it Back
#.query(Model) -> Creates a query to retrieve records from the Model
#.all() -> gives all records in object format
for i in db.query(StudentDB).all():
    pass
    # print(i.id, i.name, i.marks, i.course, i.email)

#Updata records
chris = db.get(StudentDB, "S002")
chris.marks = 93
db.commit()
