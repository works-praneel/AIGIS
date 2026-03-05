import docker, yaml, os, requests

def run_engine_scan(job_id: str, file_path: str, metadata: dict, store: dict):
    try:
        store[job_id]["status"] = "scanning"
        
        # 1. Load Manifest
        with open("../engines_manifest.yaml", "r") as f:
            manifest = yaml.safe_load(f)

        lang = metadata["language"]
        engine_name = manifest["languages"].get(lang, {}).get("engines", [None])[0]
        image_name = manifest["engines"][engine_name]["docker_image"]

        # 2. Execute Docker (Member 3 integration)
        client = docker.from_env()
        container_log = client.containers.run(
            image=image_name,
            volumes={os.path.abspath(file_path): {'bind': '/src/app_file', 'mode': 'ro'}},
            remove=True
        ).decode('utf-8')

        store[job_id]["results"] = container_log
        store[job_id]["status"] = "analyzing_with_ai"

        # 3. AI Remediation (Member 4 integration - Local LLM)
        remediation = get_ai_remediation(container_log)
        store[job_id]["remediation"] = remediation
        store[job_id]["status"] = "completed"

    except Exception as e:
        store[job_id]["status"] = "failed"
        store[job_id]["results"] = str(e)

def get_ai_remediation(logs):
    # Calls local Ollama instance
    try:
        payload = {
            "model": "llama3",
            "prompt": f"Analyze these security logs and provide a fix:\n{logs}",
            "stream": False
        }
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        return response.json().get("response", "AI could not generate fix.")
    except:
        return "AI Remediation Offline (Check Ollama)"