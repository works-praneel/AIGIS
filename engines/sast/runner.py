import os
import subprocess
from engine_manager import build_report, save_report

TOOLS = {
    "python": ["bandit", "-r"],
    "java": ["semgrep", "--config=auto"],
    "kotlin": ["semgrep", "--config=auto"],
    "cpp": ["cppcheck", "--enable=all"],
    "go": ["govulncheck"]
}

def run_sast():
    if os.environ["INPUT_TYPE"] != "code":
        raise Exception("SAST supports only source code")

    language = os.environ["LANGUAGE"]
    target = os.environ["TARGET_PATH"]

    cmd = TOOLS[language] + [target]
    result = subprocess.run(cmd, capture_output=True, text=True)

    report = build_report(
        engine="SAST",
        input_type="code",
        test_type="static",
        language=language,
        status="fail" if result.returncode != 0 else "pass",
        raw_logs=result.stdout
    )

    save_report(report)

if __name__ == "__main__":
    run_sast()
