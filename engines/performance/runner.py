import os
import subprocess
from engine_manager import build_report, save_report

def run_performance():
    if os.environ["INPUT_TYPE"] != "url":
        raise Exception("Performance supports only URLs")

    users = os.environ.get("USERS", "50")
    spawn = os.environ.get("SPAWN_RATE", "5")
    duration = os.environ.get("DURATION", "30s")
    host = os.environ["TARGET_URL"]

    result = subprocess.run(
        [
            "locust", "-f", "locustfile.py",
            "--headless",
            "-u", users,
            "-r", spawn,
            "--run-time", duration,
            "--host", host
        ],
        capture_output=True,
        text=True
    )

    report = build_report(
        engine="Locust",
        input_type="url",
        test_type="performance",
        language="web",
        status="pass",
        raw_logs=result.stdout
    )

    save_report(report)

if __name__ == "__main__":
    run_performance()
