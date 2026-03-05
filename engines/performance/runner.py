import os
import subprocess
import re
from engine_manager import build_report, save_report


def validate_env():
    required = ["INPUT_TYPE", "TARGET_URL"]

    for var in required:
        if var not in os.environ:
            raise Exception(f"Missing environment variable: {var}")

    if os.environ["INPUT_TYPE"] != "url":
        raise Exception("Performance engine supports only URL input")


def run_performance():
    validate_env()

    url = os.environ["TARGET_URL"]

    locust_command = [
        "locust",
        "-f", "locustfile.py",
        "--headless",
        "-u", "10",
        "-r", "2",
        "-t", "10s",
        "--host", url
    ]

    result = subprocess.run(
        locust_command,
        capture_output=True,
        text=True
    )

    logs = result.stdout + result.stderr

    findings = []
    status = "pass"

    # extract request/failure counts from output
    match = re.search(r'GET\s+/\s+(\d+)\s+(\d+)\(', logs)

    if match:
        requests = int(match.group(1))
        failures = int(match.group(2))

        if failures > 0:
            status = "fail"
            findings.append(f"{failures} failed requests out of {requests}")
    else:
        status = "fail"
        findings.append("Could not parse Locust results")

    report = build_report(
        engine="Performance",
        input_type="url",
        test_type="load",
        language="web",
        status=status,
        findings=findings,
        raw_logs=logs
    )

    save_report(report)


if __name__ == "__main__":
    run_performance()