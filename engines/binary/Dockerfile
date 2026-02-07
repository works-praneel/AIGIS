FROM python:3.10-slim

RUN apt-get update && apt-get install -y binutils file
WORKDIR /app
COPY runner.py engine_manager.py ./

CMD ["python", "runner.py"]
