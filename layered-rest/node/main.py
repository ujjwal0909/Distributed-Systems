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

@app.post("/add_track")
def add_track(track: Track):
    queue.append(track)
    return {"message": "Track added", "queue": queue}

@app.post("/remove_track")
def remove_track(action: TrackAction):
    global queue
    queue = [t for t in queue if t.id != action.id]
    return {"message": "Track removed", "queue": queue}

@app.post("/vote")
def vote_track(action: TrackAction, up: bool = True):
    for t in queue:
        if t.id == action.id:
            t.votes += 1 if up else -1
    queue.sort(key=lambda x: -x.votes)
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
    return {"now_playing": track}

@app.get("/history")
def get_history():
    return history
