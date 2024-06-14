#!/bin/bash

MANAGE_SERVER_IP="管理服务器的IP地址"
NEW_DIR="new"

# Ensure the new directory exists
mkdir -p $NEW_DIR

# Fetch new code
response=$(curl -s -w "%{http_code}" -o $NEW_DIR/new_code.py http://$MANAGE_SERVER_IP/new)

# Check HTTP response code
if [ "$response" -eq 200 ]; then
    echo "New code fetched successfully."
elif [ "$response" -eq 204 ]; then
    echo "No new code available."
else
    echo "Failed to fetch new code. HTTP response code: $response"
fi

