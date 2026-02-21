import docker
import yaml
import os

client = docker.from_env()

def run_engine_scan(job_id: str, file_path: str, metadata: dict, store: dict):
    store[job_id]["status"] = "processing"
    
    # Load the "Brain" of the system
    with open("../engines_manifest.yaml", "r") as f:
        manifest = yaml.safe_load(f)

    lang = metadata["language"]
    if lang not in manifest["languages"]:
        store[job_id]["status"] = "failed"
        store[job_id]["results"] = f"No engine found for {lang}"
        return

    # Select the first available engine for that language
    engine_name = manifest["languages"][lang]["engines"][0]
    image_name = manifest["engines"][engine_name]["docker_image"]

    try:
        # Run Member 3's Docker Engine
        # We mount the uploaded file into the container's /src folder
        container = client.containers.run(
            image=image_name,
            volumes={os.path.abspath(file_path): {'bind': '/src/app_file', 'mode': 'ro'}},
            detach=False,
            remove=True
        )
        
        store[job_id]["status"] = "completed"
        store[job_id]["results"] = container.decode('utf-8')
    except Exception as e:
        store[job_id]["status"] = "failed"
        store[job_id]["results"] = str(e)