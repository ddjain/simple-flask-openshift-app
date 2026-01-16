#!/bin/bash

# Load Generator Script for HPA Testing
# Continuously sends memory allocation requests with random values (1-15 MB)
# Rarely clears memory (approximately 1 in 20 calls)

BASE_URL="http://simple-flask-app-flask-demo.apps.ravichaos.aws.rhperfscale.org"

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "============================================"
echo "  HPA Load Generator - Simple Flask App"
echo "============================================"
echo "Target: $BASE_URL"
echo "Memory range: 1-15 MB"
echo "Clear probability: ~5% (1 in 20)"
echo "Press Ctrl+C to stop"
echo "============================================"
echo ""

counter=0

while true; do
    counter=$((counter + 1))
    timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    
    # Generate random number 1-20 to decide action
    action_roll=$((RANDOM % 50 + 1))
    
    if [ $action_roll -eq 1 ]; then
        # ~5% chance: Clear memory
        echo -e "${RED}[$timestamp] [$counter] Clearing memory...${NC}"
        response=$(curl -s -X POST "$BASE_URL/load/memory/clear")
        echo -e "  Response: $response"
    else
        # ~95% chance: Allocate random memory (1-15 MB)
        random_mb=$((RANDOM % 5 + 1))
        echo -e "${GREEN}[$timestamp] [$counter] Allocating ${random_mb}MB...${NC}"
        response=$(curl -s -X POST "$BASE_URL/load/memory/$random_mb")
        echo -e "  Response: $response"
    fi
    
    # Random sleep between 0.5 and 2 seconds
    sleep_time=$(awk "BEGIN {printf \"%.1f\", 0.5 + rand() * 1.5}")
    echo -e "${YELLOW}  Sleeping ${sleep_time}s...${NC}"
    sleep $sleep_time
    echo ""
done
