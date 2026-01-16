#!/bin/bash

# Load File Script - Creates multiple large files via API
# Usage: ./load_file.sh <number_of_files> <size_in_mb>

BASE_URL="http://simple-flask-app-flask-demo.apps.ravichaos.aws.rhperfscale.org"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check arguments
if [ $# -ne 2 ]; then
    echo -e "${RED}Usage: $0 <number_of_files> <size_in_mb>${NC}"
    echo "Example: $0 5 10  # Creates 5 files of 10MB each"
    exit 1
fi

NUM_FILES=$1
SIZE_MB=$2

echo "============================================"
echo "  File Load Generator"
echo "============================================"
echo "Target: $BASE_URL"
echo "Files to create: $NUM_FILES"
echo "Size per file: ${SIZE_MB}MB"
echo "Total size: $((NUM_FILES * SIZE_MB))MB"
echo "============================================"
echo ""

# Create temp directory
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

for i in $(seq 1 $NUM_FILES); do
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    filename="load_file_${i}_${SIZE_MB}mb.txt"
    
    echo -e "${YELLOW}[$timestamp] Creating file $i/$NUM_FILES: $filename (${SIZE_MB}MB)...${NC}"
    
    # Generate content and write to temp file
    content_file="$TEMP_DIR/content_$i.txt"
    head -c $((SIZE_MB * 1048576)) /dev/urandom | base64 > "$content_file"
    
    # Create JSON payload file
    payload_file="$TEMP_DIR/payload_$i.json"
    printf '{"filename": "%s", "content": "' "$filename" > "$payload_file"
    cat "$content_file" >> "$payload_file"
    printf '"}' >> "$payload_file"
    
    # Send request using file
    response=$(curl -s -X POST "$BASE_URL/file/write" \
        -H "Content-Type: application/json" \
        -d @"$payload_file")
    
    # Clean up temp files for this iteration
    rm -f "$content_file" "$payload_file"
    
    # Check response
    if echo "$response" | grep -q "successfully"; then
        echo -e "${GREEN}  ✓ Created: $filename${NC}"
        echo "  Response: $(echo $response | jq -c '{message, size_bytes}' 2>/dev/null || echo $response)"
    else
        echo -e "${RED}  ✗ Failed: $filename${NC}"
        echo "  Error: $response"
    fi
    
    echo ""
done

echo "============================================"
echo -e "${GREEN}Complete! Created $NUM_FILES files.${NC}"
echo "============================================"

# Show file list
echo -e "\n=== Files in /data ==="
curl -s "$BASE_URL/file/list" | jq '.files[] | "\(.filename) - \(.size_bytes) bytes"' 2>/dev/null
