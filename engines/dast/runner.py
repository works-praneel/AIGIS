import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from engine_manager import build_report, save_report

def run_dast():
    if os.environ["INPUT_TYPE"] != "url":
        raise Exception("DAST supports only URLs")

    url = os.environ["TARGET_URL"]

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    report = build_report(
        engine="DAST",
        input_type="url",
        test_type="functional",
        language="web",
        status="pass",
        findings=[{"page_title": driver.title}]
    )

    driver.quit()
    save_report(report)

if __name__ == "__main__":
    run_dast()
