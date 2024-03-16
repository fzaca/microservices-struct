#!/bin/sh

MAX_ATTEMPTS=10
ATTEMPT=0

CONFIG_FILE="services.yml"

# Check if Kong is available
wait_for_kong() {
    while ! curl -s http://kong:8001 > /dev/null; do
        echo "Waiting for Kong to be available..."
        sleep 5
    done
}

if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file $CONFIG_FILE not found."
    exit 1
fi

# Comprueba si los volúmenes están presentes
if [ "$(docker volume ls -q -f name=kong_data)" ]; then
    exit 1
fi

echo "Running the initialization for the first time..."

# Install required packages
apk --no-cache add curl
pip install pyyaml

# Wait for Kong to be available
wait_for_kong

# Parse configuration file and create services and routes
python3 create_services.py "$CONFIG_FILE"