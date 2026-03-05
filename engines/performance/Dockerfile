FROM python:3.10-slim

WORKDIR /app

COPY engines/performance/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY engines/performance/runner.py .
COPY engines/performance/locustfile.py .
COPY engines/sast/engine_manager.py .

CMD ["python", "runner.py"]