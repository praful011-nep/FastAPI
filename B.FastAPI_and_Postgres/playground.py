'''
Pyhton will interact with PostgreSQL directly without any FastAPI routes or endpoints
'''
import os
import psycopg
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
# Step-1 -> Get the URL from .env file

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
# print(DATABASE_URL)

#Step-2 -> Engine: The road to the database
engine = create_engine(DATABASE_URL)
# Check the version of postgres to verigy connection
with engine.connect() as conn:
    version = conn.execute(text("SELECT version()")).scalar()
    print(f"Connected to {version.split(","[0])}")