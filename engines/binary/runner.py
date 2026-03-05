import os
import subprocess
from engine_manager import build_report, save_report


def validate_env():
    required = ["INPUT_TYPE", "TARGET_PATH"]

    for var in required:
        if var not in os.environ:
            raise Exception(f"Missing environment variable: {var}")

    if os.environ["INPUT_TYPE"] != "binary":
        raise Exception("Binary engine supports only binary input")


def run_binary_scan():
    validate_env()

    target = os.environ["TARGET_PATH"]

    findings = []
    status = "pass"
    logs = ""

    # file type detection
    file_type = subprocess.run(
        ["file", target],
        capture_output=True,
        text=True
    )

    logs += file_type.stdout

    # generate SHA256
    sha = subprocess.run(
        ["sha256sum", target],
        capture_output=True,
        text=True
    )

    logs += sha.stdout

    # extract suspicious strings
    strings = subprocess.run(
        ["strings", target],
        capture_output=True,
        text=True
    )

    suspicious_keywords = ["password", "secret", "token", "key"]

    for word in suspicious_keywords:
        if word in strings.stdout.lower():
            findings.append(f"Suspicious keyword detected: {word}")

    if findings:
        status = "fail"

    report = build_report(
        engine="Binary",
        input_type="binary",
        test_type="static",
        language="generic",
        status=status,
        findings=findings,
        raw_logs=logs
    )

    save_report(report)


if __name__ == "__main__":
    run_binary_scan()