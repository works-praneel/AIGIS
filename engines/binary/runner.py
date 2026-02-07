import os
import subprocess
from engine_manager import build_report, save_report

def run_binary_scan():
    if os.environ["INPUT_TYPE"] != "binary":
        raise Exception("Binary engine supports only binary files")

    target = os.environ["TARGET_PATH"]

    file_info = subprocess.run(["file", target], capture_output=True, text=True)
    strings_out = subprocess.run(["strings", target], capture_output=True, text=True)

    report = build_report(
        engine="Binary Analysis",
        input_type="binary",
        test_type="basic-security",
        language="N/A",
        status="pass",
        findings=[{"file_info": file_info.stdout}],
        raw_logs=strings_out.stdout[:2000]
    )

    save_report(report)

if __name__ == "__main__":
    run_binary_scan()
