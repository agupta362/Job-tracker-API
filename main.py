from fastapi import FastAPI, HTTPException
from database import execute_query
from models import JobCreate, JobUpdate

app = FastAPI()

def create_tables():
    execute_query("""
        CREATE TABLE IF NOT EXISTS jobs (
            id SERIAL PRIMARY KEY,
            company VARCHAR(200) NOT NULL,
            title VARCHAR(200) NOT NULL,
            status VARCHAR(50) NOT NULL DEFAULT 'applied',
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    print("Tables ready")

create_tables()

@app.get("/")
def root():
    return {"message": "Job Tracker API v2 - auto deployed"}

@app.post("/jobs")
def create_job(job: JobCreate):
    row = execute_query(
        "INSERT INTO jobs (company, title, status, notes) VALUES (%s, %s, %s, %s) RETURNING id",
        (job.company, job.title, job.status, job.notes),
        fetch="one"
    )
    return {"message": "Job created", "id": row[0]}

@app.get("/jobs")
def get_jobs():
    rows = execute_query("SELECT * FROM jobs ORDER BY created_at DESC", fetch="all")
    jobs = []
    for row in rows:
        jobs.append({
            "id": row[0],
            "company": row[1],
            "title": row[2],
            "status": row[3],
            "notes": row[4],
            "created_at": str(row[5])
        })
    return {"jobs": jobs}

@app.get("/jobs/status/{status}")
def get_jobs_by_status(status: str):
    rows = execute_query(
        "SELECT * FROM jobs WHERE status = %s ORDER BY created_at DESC",
        (status,),
        fetch="all"
    )
    jobs = []
    for row in rows:
        jobs.append({
            "id": row[0],
            "company": row[1],
            "title": row[2],
            "status": row[3],
            "notes": row[4],
            "created_at": str(row[5])
        })
    return {"jobs": jobs}

@app.get("/jobs/{id}")
def get_job(id: int):
    row = execute_query(
        "SELECT * FROM jobs WHERE id = %s",
        (id,),
        fetch="one"
    )
    if row is None:
        raise HTTPException(status_code=404, detail="Job not found")
    return {
        "id": row[0],
        "company": row[1],
        "title": row[2],
        "status": row[3],
        "notes": row[4],
        "created_at": str(row[5])
    }

@app.put("/jobs/{id}")
def update_job(id: int, job: JobUpdate):
    existing = execute_query(
        "SELECT * FROM jobs WHERE id = %s",
        (id,),
        fetch="one"
    )
    if existing is None:
        raise HTTPException(status_code=404, detail="Job not found")
    execute_query(
        "UPDATE jobs SET status = COALESCE(%s, status), notes = COALESCE(%s, notes) WHERE id = %s",
        (job.status, job.notes, id)
    )
    return {"message": "Job updated"}

@app.delete("/jobs/{id}")
def delete_job(id: int):
    existing = execute_query(
        "SELECT * FROM jobs WHERE id = %s",
        (id,),
        fetch="one"
    )
    if existing is None:
        raise HTTPException(status_code=404, detail="Job not found")
    execute_query(
        "DELETE FROM jobs WHERE id = %s",
        (id,)
    )
    return {"message": "Job deleted"}