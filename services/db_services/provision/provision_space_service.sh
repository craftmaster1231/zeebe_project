#!/bin/bash

# Set up a virtual environment
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
# Install dependencies
pip install -r requirements.txt

# Compile proto file
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. provision_space_service.proto

# Run the server
python provision_space_service.py

deactivate

