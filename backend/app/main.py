from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import yaml
import os
from .classifier import discover_capabilities
from .orchestrator import execute_engine

app = FastAPI()

# Utility to get specific test config from YAML
def get_test_config(file_path, test_choice):
    mime = magic.Magic(mime=True).from_file(file_path)
    ext = os.path.splitext(file_path)[1]
    
    with open("../engines_manifest.yaml", "r") as f:
        manifest = yaml.safe_load(f)

    for engine in manifest.get('engines', []):
        if engine['extension'] == ext or engine['mime_type'] == mime:
            return engine['test_types'].get(test_choice)
    return None

@app.post("/execute")
async def run_test(filename: str = Form(...), test_choice: str = Form(...)):
    file_path = f"data/{filename}"
    
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found. Please upload again.")

    # 1. Fetch the exact Image and Command from YAML
    config = get_test_config(file_path, test_choice)
    
    if not config:
        raise HTTPException(status_code=400, detail="Invalid test selection for this file type.")

    # 2. Hand off to Orchestrator (Member 1/3's domain)
    # The command is dynamically pulled: e.g., 'mvn test' or 'bandit -r'
    logs = execute_engine(
        image_name=config['image'], 
        command=config['command'], 
        file_path=file_path
    )

    return {
        "test_performed": test_choice,
        "engine_used": config['image'],
        "output": logs
    }