#!/bin/bash

# Base directory containing all worker directories
BASE_DIR=$(pwd)/../services/db_services/
PIDS=()  # Array to store worker process IDs

# Setup a common Python virtual environment
echo "Setting up common virtual environment..."
COMMON_VENV="$BASE_DIR/venv"
if [ ! -d "$COMMON_VENV" ]; then
  python3 -m venv "$COMMON_VENV"
fi
source "$COMMON_VENV/bin/activate"

# Install dependencies
echo "Installing dependencies..."
if [ -f "$BASE_DIR/requirements.txt" ]; then
  pip install --upgrade pip
  pip install -r "$BASE_DIR/requirements.txt"
else
  echo "No requirements.txt found. Make sure dependencies are manually managed."
fi

# Trap SIGINT (Ctrl+C) to kill all worker processes
trap 'echo "Stopping all services..."; for pid in "${PIDS[@]}"; do kill $pid 2>/dev/null; done; exit' SIGINT

# Start workers and output logs in real-time
echo "Starting all services..."
for dir in $(find ../services/db_services -type d -not -path "./venv*" -not -path "."); do
  if [ -f "$dir/run_server.sh" ]; then
    echo "Starting Service in $dir..."
    cd "$dir"
    # Compile proto file
    python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. my_service.proto &

    # Run the server
    python main.py &
    PIDS+=($!)  # Store the PID of the worker process
    cd "$BASE_DIR"
  fi
done

# Keep the script running to show real-time output from all workers
echo "All Services are running. Press Ctrl+C to stop."
wait

