#!/bin/bash

# Create a virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Compile gateway.proto to Python if needed
if [ -f "gateway.proto" ]; then
    python3 -m grpc_tools.protoc -I . --python_out=. --grpc_python_out=. gateway.proto
fi

# Run the gRPC server
python3 main.py

