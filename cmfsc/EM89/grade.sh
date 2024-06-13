#!/bin/bash

NEW_DIR="new"

# Ensure the new directory exists
mkdir -p $NEW_DIR

for file in $NEW_DIR/*.py; do
    if [ -f "$file" ]; then
        id=$(basename "$file" .py)
        curl -X GET "http://localhost:8000/execute/$id"
    fi
done

