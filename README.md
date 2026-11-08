# FastAPI Learning & Projects

A hands-on repository covering FastAPI fundamentals—from basic routing and Pydantic validation to building, testing, and containerizing a PostgreSQL-backed REST API.

---

## 📁 Repository Structure

```text
FastAPI/
├── A.FastAPI_Basics/
│   ├── main.py              # FastAPI CRUD endpoints with JSON file storage
│   ├── pydantic_basics.py   # Pydantic schema validation, field rules & validators
│   ├── app.py               # Streamlit frontend dashboard for student registry
│   ├── students.json        # Sample JSON database
│   └── web/                 # HTML/CSS/JavaScript web interface
│
└── B.FastAPI_and_Postgres/
    ├── main.py              # Full CRUD API using SQLAlchemy ORM & PostgreSQL
    ├── playground.py        # Database query & testing experiments
    ├── Dockerfile           # FastAPI application container definition
    ├── docker-compose.yml   # Multi-container setup (FastAPI + PostgreSQL 16)
    └── requirements.txt     # Python project dependencies
```

---

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- (Optional) Docker & Docker Compose for PostgreSQL containerization

### 2. Setup Virtual Environment

```bash
# Clone the repository
git clone <repo-url>
cd FastAPI

# Create and activate a virtual environment
python -m venv .venv

# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# Install dependencies
pip install -r B.FastAPI_and_Postgres/requirements.txt
```

---

## 🏃 Running the Projects

### Part A: FastAPI Basics
Explore beginner-friendly endpoints and Pydantic validation:
```bash
cd A.FastAPI_Basics
uvicorn main:app --reload
```
- Interactive API Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- *(Optional)* Launch the Streamlit dashboard:
  ```bash
  pip install streamlit pandas altair
  streamlit run app.py
  ```

---

### Part B: FastAPI with PostgreSQL

#### Option 1: Using Docker Compose (Quickest)
Starts both PostgreSQL and the FastAPI application automatically:
```bash
cd B.FastAPI_and_Postgres
docker-compose up --build
```

#### Option 2: Running Locally
1. Ensure a PostgreSQL instance is running.
2. Create or verify `.env` inside `B.FastAPI_and_Postgres`:
   ```env
   DATABASE_URL=postgresql://<user>:<password>@localhost:5432/<dbname>
   ```
3. Start the API server:
   ```bash
   cd B.FastAPI_and_Postgres
   uvicorn main:app --reload
   ```

---

## 📖 API Documentation
FastAPI provides automatic interactive documentation out of the box:
- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)
