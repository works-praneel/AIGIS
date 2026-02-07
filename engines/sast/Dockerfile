FROM python:3.10-slim

# OS-level tools
RUN apt-get update && apt-get install -y \
    cppcheck \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Python security tools
RUN pip install --no-cache-dir bandit semgrep

# Go toolchain for govulncheck
RUN curl -OL https://go.dev/dl/go1.22.1.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.22.1.linux-amd64.tar.gz \
    && rm go1.22.1.linux-amd64.tar.gz

ENV PATH="/usr/local/go/bin:${PATH}"

RUN go install golang.org/x/vuln/cmd/govulncheck@latest

WORKDIR /app
COPY runner.py engine_manager.py ./

CMD ["python", "runner.py"]
