'''
Pyhton will interact with PostgreSQL directly without any FastAPI routes or endpoints
'''
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")
print(DATABASE_URL)