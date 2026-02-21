import os
import sys
import json
import subprocess
from engine_manager import build_report, save_report


def validate_env():
    required = ["INPUT_TYPE", "LANGUAGE", "TARGET_PATH", "OUTPUT_DIR"]

    for var in required:
        if var not in os.environ:
            print(f"Missing required environment variable: {var}")
            sys.exit(1)

    if os.environ["INPUT_TYPE"] != "code":
        print("SAST supports only 'code' input type.")
        sys.exit(1)


def load_config():
    try:
        with open("config/test-matrix.json", "r") as f:
            return json.load(f)
    except Exception:
        print("Unable to load test-matrix.json")
        sys.exit(1)


def resolve_tool(language, config):
    try:
        if "sast" not in config["code"][language]:
            print(f"SAST not enabled for language: {language}")
            sys.exit(1)
    except KeyError:
        print(f"Unsupported language: {language}")
        sys.exit(1)

    tool_map = {
        "python": ["bandit", "-r"],
        "java": ["semgrep", "--config=auto"],
        "kotlin": ["semgrep", "--config=auto"],
        "cpp": ["cppcheck", "--enable=all"],
        "go": ["govulncheck"]
    }

    return tool_map.get(language)


def run_sast():
    validate_env()

    language = os.environ["LANGUAGE"]
    target = os.environ["TARGET_PATH"]

    config = load_config()
    tool_command = resolve_tool(language, config)

    if not tool_command:
        print(f"No tool configured for language: {language}")
        sys.exit(1)

    # ---- GO SPECIAL HANDLING ----
    if language == "go":
        cmd = ["govulncheck", "./..."]
        working_dir = target
    else:
        cmd = tool_command + [target]
        working_dir = None

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=working_dir
    )

    findings = []
    status = "pass"

    output_text = (result.stdout + result.stderr).lower()

    # ---- Generic non-zero exit detection ----
    if result.returncode != 0:
        status = "fail"
        findings.append("Security issues detected")

    # ---- Cppcheck detection ----
    if language == "cpp" and "warning:" in output_text:
        status = "fail"
        findings.append("Cppcheck warning detected")

    # ---- Semgrep detection (Java/Kotlin) ----
    if language in ["java", "kotlin"] and "finding" in output_text:
        status = "fail"
        findings.append("Semgrep findings detected")

    report = build_report(
        engine="SAST",
        input_type="code",
        test_type="static",
        language=language,
        status=status,
        findings=findings,
        raw_logs=result.stdout + result.stderr
    )

    save_report(report)


if __name__ == "__main__":
    run_sast()