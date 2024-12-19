#!/bin/bash

# Base directory containing all worker directories
BASE_DIR=$(pwd)
COMMON_LOG="$BASE_DIR/common_log.log"

# Clear the common log file
> "$COMMON_LOG"

# Setup a common Python virtual environment
echo "Setting up common virtual environment..."
echo "Setting up common virtual environment..." >> "$COMMON_LOG"
COMMON_VENV="$BASE_DIR/venv"
if [ ! -d "$COMMON_VENV" ]; then
  python3 -m venv "$COMMON_VENV"
fi
source "$COMMON_VENV/bin/activate"

# Install dependencies
echo "Installing dependencies..."
echo "Installing dependencies..." >> "$COMMON_LOG"
if [ -f "$BASE_DIR/requirements.txt" ]; then
  pip install --upgrade pip >> "$COMMON_LOG" 2>&1
  pip install -r "$BASE_DIR/requirements.txt" >> "$COMMON_LOG" 2>&1
else
  echo "No requirements.txt found. Make sure dependencies are manually managed." >> "$COMMON_LOG"
fi

# Iterate over directories containing `main.py` and exclude `venv`
for dir in $(find . -type d -not -path "./venv*" -not -path "."); do
  if [ -f "$dir/main.py" ]; then
    echo "Processing directory: $dir"
    echo "Processing directory: $dir" >> "$COMMON_LOG"
    
    # Run the worker
    cd "$dir"
    echo "Starting Zeebe worker in $dir..."
    echo "Starting Zeebe worker in $dir..." >> "$COMMON_LOG"
    python main.py >> "$COMMON_LOG" 2>&1 &
    WORKER_PID=$!

    # Wait for 0.5 seconds to see if the worker starts correctly
    sleep 0.5

    # Check if the worker is still running
    if ps -p $WORKER_PID > /dev/null; then
      echo "Worker in $dir started successfully."
      echo "Worker in $dir started successfully." >> "$COMMON_LOG"
    else
      echo "Worker in $dir failed to start. Check $dir/worker.log for details."
      echo "Worker in $dir failed to start. Check $dir/worker.log for details." >> "$COMMON_LOG"
    fi

    cd "$BASE_DIR"  # Return to the base directory
    echo "Completed processing $dir."
    echo "Completed processing $dir." >> "$COMMON_LOG"
    echo "------------------------------"
    echo "------------------------------" >> "$COMMON_LOG"
  fi
done

# Deactivate virtual environment
deactivate

echo "All workers processed."
echo "All workers processed." >> "$COMMON_LOG"

