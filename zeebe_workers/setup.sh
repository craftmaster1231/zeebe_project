#!/bin/bash

# Setup Python virtual environment
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r worker/requirements.txt

# Run the Zeebe worker
echo "Starting Zeebe worker..."
python worker/main.py
