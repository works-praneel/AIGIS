FROM owasp/zap2docker-stable

WORKDIR /zap
COPY runner.py engine_manager.py ./

CMD ["python3", "runner.py"]
