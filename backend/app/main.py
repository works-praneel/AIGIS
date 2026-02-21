from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from typing import Dict
import uuid
import os
from .classifier import identify_artifact
from .orchestrator import run_engine_scan

app = FastAPI(title="AIGIS Backend - Member 2")

# In-memory status store for tracking long-running scans
# In Production (Member 1), this would move to Redis.
job_status_store: Dict[str, dict] = {}

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/scan/upload")
async def start_scan(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    # 1. Save file locally
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # 2. Identify the file (Member 2 Logic)
    metadata = identify_artifact(file_path)
    
    # 3. Initialize background job
    job_id = str(uuid.uuid4())
    job_status_store[job_id] = {
        "status": "queued",
        "file_name": file.filename,
        "language": metadata["language"],
        "results": None
    }

    # 4. Trigger Orchestrator in background
    background_tasks.add_task(run_engine_scan, job_id, file_path, metadata, job_status_store)

    return {"job_id": job_id, "message": "Scan started in background", "metadata": metadata}

@app.get("/scan/status/{job_id}")
async def get_status(job_id: str):
    if job_id not in job_status_store:
        raise HTTPException(status_code=404, detail="Job ID not found")
    return job_status_store[job_id]