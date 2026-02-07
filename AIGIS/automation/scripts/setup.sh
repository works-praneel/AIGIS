#!/bin/bash
echo "🚀 Initializing AIGIS Environment..."

# Create necessary folders if they don't exist
mkdir -p data reports

# Build the core service
docker-compose build

echo "✅ Setup Complete. Run 'docker-compose up' to start."