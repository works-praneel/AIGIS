FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    cppcheck \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first
COPY engines/sast/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Go
RUN curl -OL https://go.dev/dl/go1.22.1.linux-amd64.tar.gz \
    && tar -C /usr/local -xzf go1.22.1.linux-amd64.tar.gz \
    && rm go1.22.1.linux-amd64.tar.gz

ENV GOPATH=/go
ENV PATH="/usr/local/go/bin:/go/bin:${PATH}"

RUN go install golang.org/x/vuln/cmd/govulncheck@latest

# Copy SAST engine files
COPY engines/sast/runner.py .
COPY engines/sast/engine_manager.py .

# Copy config folder from root
COPY engines/config ./config

CMD ["python", "runner.py"]