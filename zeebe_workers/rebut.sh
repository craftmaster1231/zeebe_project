#!/bin/bash

# Container name
CONTAINER_NAME="zeebe"

# Check if the container is running
if docker ps -q -f name=$CONTAINER_NAME; then
    echo "Clearing Zeebe data in container: $CONTAINER_NAME"
    
    # Clear Zeebe data inside the container
    docker exec $CONTAINER_NAME rm -rf /usr/local/zeebe/data/*
    
    # Restart the container
    echo "Restarting Zeebe..."
    docker restart $CONTAINER_NAME
    
    echo "Zeebe data cleared and container restarted successfully."
else
    echo "Error: Container $CONTAINER_NAME is not running."
    exit 1
fi