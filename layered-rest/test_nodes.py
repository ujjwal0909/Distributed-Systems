import requests
import time

# This script tests the distributed queue system via the Nginx load balancer
# Usage: python test_nodes.py

base_url = "http://localhost:8080"

# Add a track
track = {
    "id": 1,
    "title": "Test Song",
    "artist": "Test Artist",
    "duration": 180,
    "votes": 0
}

print(f"Adding track to {base_url}")
resp = requests.post(f"{base_url}/add_track", json=track)
try:
    print("Add response:", resp.json())
except Exception as e:
    print(f"Add response not JSON: {resp.text}\nError: {e}")

# Wait for sync
print("Waiting for sync...")
time.sleep(5)

# Check queue multiple times to hit different nodes via load balancer
seen_with_track = 0
seen_without_track = 0
for i in range(10):
    try:
        resp = requests.get(f"{base_url}/queue")
        queue = resp.json()
        has_track = any(t["id"] == 1 for t in queue)
        if has_track:
            seen_with_track += 1
        else:
            seen_without_track += 1
        print(f"Queue at {base_url} (request {i+1}): {queue}")
    except Exception as e:
        print(f"Error checking {base_url}: {e}")
    time.sleep(0.5)

print(f"\nSummary: {seen_with_track} responses had the track, {seen_without_track} did not.")
