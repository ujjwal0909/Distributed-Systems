
# Distributed Music Queue System

## Quick Start Guide

All commands below are run from the project root directory (the folder containing this README). You do NOT need to change directories.

### 1. Build and Start the System

```powershell
docker compose -f layered-rest/docker-compose.yml up --build
```

To scale the number of FastAPI nodes, add the `--scale node=<number_of_nodes>` option. For example, to run 3 nodes:

```powershell
docker compose -f layered-rest/docker-compose.yml up --build --scale node=3
```

This will start multiple FastAPI nodes, Nginx (load balancer), and Redis (shared queue backend).


### 2. Access the API



## Web GUI (Recommended)

Once running, the easiest way to interact and test the API is via the FastAPI Swagger UI:

```
http://localhost:8080/
```

This will automatically redirect to `/docs`, the interactive API documentation and tester. You can try out all endpoints, see schemas, and get example requests and responses.

---



## Command Line API Access
You can also interact with the API from the command line. Both curl (Linux/macOS/WSL/Git Bash) and PowerShell (Windows) examples are provided. Replace `123` with your actual track id. Run these in a separate terminal while the containers are running.

**Tip:** Use the GUI first to see the required fields and try out requests interactively.

Add a track to the queue:
```sh
# curl:
curl -X POST "http://localhost:8080/add_track" -H "Content-Type: application/json" -d '{"id": 123, "title": "Song Title", "artist": "Artist Name", "duration": 200}'
# PowerShell:
Invoke-WebRequest -Uri "http://localhost:8080/add_track" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"id": 123, "title": "Song Title", "artist": "Artist Name", "duration": 200}'
```

Remove a track from the queue:
```sh
# curl:
curl -X POST "http://localhost:8080/remove_track" -H "Content-Type: application/json" -d '{"id": 123}'
# PowerShell:
Invoke-WebRequest -Uri "http://localhost:8080/remove_track" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"id": 123}'
```

Vote for a track (moves it up in the queue):
```sh
# curl:
curl -X POST "http://localhost:8080/vote?id=123&up=true" -H "Content-Type: application/json" -d '{"id": 123}'
# PowerShell:
Invoke-WebRequest -Uri "http://localhost:8080/vote?id=123&up=true" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"id": 123}'
```

**Note:** Voting increases the track's votes and reorders the queue so higher-voted tracks play sooner.


Get the current queue:
```sh
# curl:
curl http://localhost:8080/queue
# PowerShell:
Invoke-WebRequest -Uri "http://localhost:8080/queue" -Method GET
```

Get the track metadata:
```sh
# curl:
curl http://localhost:8080/metadata/123
# PowerShell:
Invoke-WebRequest -Uri "http://localhost:8080/metadata/123" -Method GET
```

Get the play history (tracks played via play_next):
```sh
# curl:
curl http://localhost:8080/history
# PowerShell:
Invoke-WebRequest -Uri "http://localhost:8080/history" -Method GET
```

Play the next song (removes from queue, adds to history):
```sh
# curl:
curl -X POST http://localhost:8080/play_next
# PowerShell:
Invoke-WebRequest -Uri "http://localhost:8080/play_next" -Method POST
```

**Note:** Only tracks played via `play_next` are added to the play history. Use this endpoint to simulate playing songs and building up the history.

### 3. Run the Automated Test Suite

To validate all functional requirements, run in a separate terminal while the containers are runnning in the other terminal:

```powershell
python layered-rest/tests/run_all_tests.py
```

This will execute all test scripts and print a summary of results. All tests should pass if the system is running.


### 4. Stopping the System

To stop all containers you can use control+c in the terminal they're running or in a separate terminal run:

```powershell
docker compose -f layered-rest/docker-compose.yml down
```

---

For more details, see the code and test scripts in the `layered-rest` directory.
