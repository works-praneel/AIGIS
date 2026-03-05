FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    file \
    binutils \
    && rm -rf /var/lib/apt/lists/*

COPY engines/binary/runner.py .
COPY engines/sast/engine_manager.py .

CMD ["python", "runner.py"]