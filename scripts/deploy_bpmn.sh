#!/bin/bash

# Zeebe Gateway address (modify if needed)
ZEEBE_GATEWAY="localhost:26500"
DEPLOYMENT_LOG="deployment_log.txt"
ERROR_LOG="error_log.txt"
FILES_PROCESSED=0

# Clear previous logs
> $DEPLOYMENT_LOG
> $ERROR_LOG

# Check if zbctl is installed
if ! command -v zbctl &> /dev/null
then
    echo "Error: zbctl is not installed or not in PATH." | tee -a $ERROR_LOG
    exit 1
fi

# Check if the bpmn directory exists and contains files
if [ ! -d "../bpmn" ] || [ -z "$(ls -A ../bpmn/*.bpmn 2>/dev/null)" ]; then
    echo "Error: No BPMN files found in ../bpmn directory." | tee -a $ERROR_LOG
    exit 1
fi

# Loop through all BPMN files in the bpmn/ directory
for file in ../bpmn/*.bpmn; do
    echo "Deploying $file to Zeebe..."

    # Deploy the BPMN file using zbctl
    zbctl --insecure --address $ZEEBE_GATEWAY deploy "$file" >> $DEPLOYMENT_LOG 2>> $ERROR_LOG

    # Check if deployment was successful
    if [ $? -eq 0 ]; then
        echo "$file deployed successfully." | tee -a $DEPLOYMENT_LOG
        FILES_PROCESSED=$((FILES_PROCESSED + 1))
    else
        echo "Failed to deploy $file. Check error log: $ERROR_LOG" | tee -a $ERROR_LOG
    fi
done

# Only show success message if files were processed
if [ $FILES_PROCESSED -gt 0 ]; then
    echo "All BPMN files processed successfully."
else
    echo "No BPMN files were processed."
fi

