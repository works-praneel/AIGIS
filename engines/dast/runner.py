import os
import subprocess
import json
from engine_manager import build_report, save_report


def validate_env():
    required = ["INPUT_TYPE", "TARGET_URL"]

    for var in required:
        if var not in os.environ:
            raise Exception(f"Missing environment variable: {var}")

    if os.environ["INPUT_TYPE"] != "url":
        raise Exception("DAST supports only URL input")


def run_dast():
    validate_env()

    url = os.environ["TARGET_URL"]

    zap_command = [
        "zap-baseline.py",
        "-t", url,
        "-J", "zap_report.json"
    ]

    result = subprocess.run(
        zap_command,
        capture_output=True,
        text=True
    )

    findings = []
    status = "pass"
    total_alerts = 0

    # Parse ZAP JSON if it exists
    if os.path.exists("zap_report.json"):
        try:
            with open("zap_report.json") as f:
                zap_data = json.load(f)

            for site in zap_data.get("site", []):
                alerts = site.get("alerts", [])
                total_alerts += len(alerts)

            if total_alerts > 0:
                status = "fail"
                findings.append(f"{total_alerts} vulnerabilities detected")

        except Exception as e:
            status = "fail"
            findings.append("Error parsing ZAP report")

    else:
        # Only mark execution issue if no report file exists
        status = "fail"
        findings.append("ZAP execution failed")

    report = build_report(
        engine="DAST",
        input_type="url",
        test_type="dynamic",
        language="web",
        status=status,
        findings=findings,
        raw_logs=result.stdout + result.stderr
    )

    save_report(report)


if __name__ == "__main__":
    run_dast()