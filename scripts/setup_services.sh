#!/bin/bash

# Base directory containing all worker directories
BASE_DIR=$(dirname "$0")/../services/db_services/
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
trap 'echo "Stopping all services..."; for pid in "${PIDS[@]}"; do kill $pid 2>/dev/null; done; wait; exit' SIGINT

# Start workers and output logs in real-time
echo "Starting all services..."
for dir in $(find "$BASE_DIR" -mindepth 1 -maxdepth 1 -type d -not -path "$COMMON_VENV*" -not -path "$BASE_DIR" -not -path "."); do
  if [ -f "$dir/run_server.sh" ]; then
    echo "Starting Service in $dir..."
    cd "$dir" || continue
    
    # Compile proto files safely
    if [ -f "my_service.proto" ]; then
      python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. my_service.proto
    fi

    # Run the server
    if python main.py & then
      PIDS+=($!)  # Store the PID of the worker process
      echo "Service in $dir started successfully."
    else
      echo "Failed to start service in $dir."
    fi
    cd - > /dev/null  # Return to the previous directory without error if already there
  fi
done

# Keep the script running to show real-time output from all workers
echo "All Services are running. Press Ctrl+C to stop."
wait

