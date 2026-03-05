import os, uuid, json
from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .classifier import identify_artifact
from .orchestrator import run_engine_scan

app = FastAPI(title="AIGIS Autonomous System")

# Enable CORS for Member 4's Frontend
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

job_status_store = {}
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploads")
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/scan/upload")
async def start_scan(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
    
    with open(file_path, "wb") as f:
        f.write(await file.read())

    metadata = identify_artifact(file_path)
    job_id = str(uuid.uuid4())
    
    job_status_store[job_id] = {
        "status": "queued",
        "file_name": file.filename,
        "metadata": metadata,
        "results": None,
        "remediation": None
    }

    background_tasks.add_task(run_engine_scan, job_id, file_path, metadata, job_status_store)
    return {"job_id": job_id, "metadata": metadata}

@app.get("/scan/status/{job_id}")
async def get_status(job_id: str):
    return job_status_store.get(job_id, {"status": "not_found"})