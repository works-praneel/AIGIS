import os
import json
from datetime import datetime

def build_report(engine, input_type, test_type, language, status, findings=None, raw_logs=None):
    return {
        "engine": engine,
        "input_type": input_type,
        "test_type": test_type,
        "language": language,
        "status": status,
        "timestamp": datetime.utcnow().isoformat(),
        "findings": findings or [],
        "raw_logs": raw_logs or ""
    }

def save_report(report):
    output_dir = os.environ["OUTPUT_DIR"]
    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(output_dir, "report.json")
    with open(path, "w") as f:
        json.dump(report, f, indent=4)
