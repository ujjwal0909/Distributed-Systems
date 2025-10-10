import requests
import time

base_url = "http://localhost:8080"

def clear_queue():
    for tid in range(1, 5):
        requests.post(f"{base_url}/remove_track", json={"id": tid})

def test_metadata():
    clear_queue()
    track = {"id": 1, "title": "MetaSong", "artist": "Meta", "duration": 123}
    requests.post(f"{base_url}/add_track", json=track)
    time.sleep(1)
    resp = requests.get(f"{base_url}/metadata/1")
    assert resp.status_code == 200, "Metadata endpoint failed"
    data = resp.json()
    assert data["title"] == "MetaSong" and data["artist"] == "Meta" and data["duration"] == 123, "Metadata incorrect"
    print("test_metadata: PASS")

if __name__ == "__main__":
    test_metadata()
