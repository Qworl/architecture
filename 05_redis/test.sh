#!/bin/bash

set -e  # Останавливаем скрипт при любой ошибке

echo "Getting token..."
TOKEN=$(curl -s --max-time 5 -X POST "http://0.0.0.0:8000/token" \
    -H "Content-Type: application/x-www-form-urlencoded" \
    -d "username=admin&password=secret" | jq -r '.access_token')

if [ -z "$TOKEN" ]; then
    echo "Failed to get token"
    exit 1
fi

echo "Token received successfully"
echo "----------------------------------------"

mkdir -p results

run_test() {
    local threads=$1
    local connections=$1
    local endpoint=$2
    local output_file="results/redis_wrk_${endpoint}_${threads}t_${connections}c.txt"
    
    echo "Running test for $endpoint with $threads threads and $connections connections..."
    echo "Command: wrk -t$threads -c$connections -d10s -H \"Authorization: Bearer $TOKEN\" http://0.0.0.0:8000/users/$endpoint"
    
    timeout 15 wrk -t$threads -c$connections -d10s \
        -H "Authorization: Bearer $TOKEN" \
        "http://0.0.0.0:8000/users/$endpoint" > "$output_file" 2>&1
    
    if [ $? -eq 124 ]; then
        echo "Test timed out after 15 seconds"
        echo "TIMEOUT" > "$output_file"
    fi
    
    echo "Results saved to $output_file"
    echo "----------------------------------------"
}

echo "Starting performance tests..."
echo "----------------------------------------"

echo "Testing /list endpoint..."
run_test 1 "list"
run_test 5 "list"
run_test 10 "list"

echo "Testing /details endpoint..."
run_test 1 "details?user_id=1"
run_test 5 "details?user_id=1"
run_test 10 "details?user_id=1"

echo "All tests completed. Results are in the 'results' directory." 