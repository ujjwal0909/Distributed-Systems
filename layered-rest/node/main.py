import os
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Models
class Track(BaseModel):
    id: int
    title: str
    artist: str
    duration: int  # seconds
    votes: int = 0

class TrackAction(BaseModel):
    id: int

# In-memory storage
queue: List[Track] = []
history: List[Track] = []

def get_peers():
    peers = os.getenv("PEER_NODES", "")
    return [p.strip() for p in peers.split(",") if p.strip()]

def broadcast_queue():
    peers = get_peers()
    for peer in peers:
        try:
            requests.post(f"{peer}/sync", json=[t.dict() for t in queue], timeout=1)
        except Exception:
            pass  # Ignore errors for now

@app.post("/add_track")
def add_track(track: Track):
    queue.append(track)
    broadcast_queue()
    return {"message": "Track added", "queue": queue}

@app.post("/remove_track")
def remove_track(action: TrackAction):
    global queue
    queue = [t for t in queue if t.id != action.id]
    broadcast_queue()
    return {"message": "Track removed", "queue": queue}

@app.post("/vote")
def vote_track(action: TrackAction, up: bool = True):
    for t in queue:
        if t.id == action.id:
            t.votes += 1 if up else -1
    queue.sort(key=lambda x: -x.votes)
    broadcast_queue()
    return {"queue": queue}

@app.get("/queue")
def get_queue():
    return queue

@app.get("/metadata/{track_id}")
def get_metadata(track_id: int):
    for t in queue:
        if t.id == track_id:
            return t
    raise HTTPException(status_code=404, detail="Track not found")

@app.post("/play_next")
def play_next():
    if not queue:
        raise HTTPException(status_code=400, detail="Queue empty")
    track = queue.pop(0)
    history.append(track)
    broadcast_queue()
    return {"now_playing": track}

@app.get("/history")
def get_history():
    return history

# Sync endpoint for receiving queue updates from peers
@app.post("/sync")
def sync_queue(new_queue: List[Track]):
    global queue
    queue = [Track(**t.dict()) if isinstance(t, Track) else Track(**t) for t in new_queue]
    return {"message": "Queue synchronized", "queue": queue}
