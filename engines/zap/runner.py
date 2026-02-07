import os
import subprocess
from engine_manager import build_report, save_report

def run_zap():
    if os.environ["INPUT_TYPE"] != "url":
        raise Exception("ZAP supports only URLs")

    url = os.environ["TARGET_URL"]

    subprocess.run([
        "zap-baseline.py",
        "-t", url,
        "-J", "zap.json"
    ])

    with open("zap.json") as f:
        raw = f.read()

    report = build_report(
        engine="OWASP ZAP",
        input_type="url",
        test_type="vulnerability",
        language="web",
        status="fail",
        raw_logs=raw
    )

    save_report(report)

if __name__ == "__main__":
    run_zap()
