FROM ghcr.io/zaproxy/zaproxy:stable

USER root

WORKDIR /zap

COPY engines/dast/runner.py .
COPY engines/dast/engine_manager.py .

ENTRYPOINT ["python3", "runner.py"]