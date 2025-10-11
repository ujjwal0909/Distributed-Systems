# Distributed Music Queue System

This project implements a distributed music queue system using **two distinct system architectures**:

- **Layered/Resource-Based Architecture (REST/HTTP):**
  - Implemented in the `layered-rest` directory using FastAPI and HTTP (RESTful) endpoints.
  - Nodes are stateless FastAPI apps, with Nginx as a load balancer and Redis as a shared backend for distributed state.
  - Communication model: HTTP/REST.

- **Microservices Architecture (gRPC):**
  - Implemented in the `microservices-grpc` directory using Python, gRPC, and Redis.
  - Each node is a gRPC microservice, communicating via gRPC and sharing state through Redis.
  - Communication model: gRPC.

Both systems support autoscaling (multiple nodes), distributed synchronization, and are fully containerized with Docker Compose. Automated test runners are provided for each architecture.

---

## System Architecture Overview

- **Layered/Resource-Based (REST/HTTP):** Stateless FastAPI nodes, Nginx load balancing, Redis backend, HTTP/REST communication.
- **Microservices (gRPC):** Python gRPC services, Redis backend, gRPC communication.
- **Redis Backend:** All nodes in both architectures share a single Redis instance for queue, history, and metadata storage.
- **Docker Compose Orchestration:** All services (nodes, Redis, Nginx, test-runner) are orchestrated via Docker Compose, with healthchecks and service dependencies for reliable startup.
- **Automated Test Runner:** Test scripts are run inside a dedicated container, ensuring tests execute in the same network as the services, using Compose DNS for service discovery.

## Quick Start Guide

All commands below are run from the project root directory (the folder containing this README). You do NOT need to change directories.

---

### Layered/Resource-Based Architecture (REST/HTTP)

**Build and Start the System:**

```powershell
docker compose -f layered-rest/docker-compose.yml up --build --scale node=3
```

This starts 3 FastAPI nodes, Nginx (load balancer), and Redis (shared backend). Adjust the number after `--scale node=` as needed for autoscaling.

**Access the REST API:**

- Web GUI: Open [http://localhost:8080/](http://localhost:8080/) in your browser. This redirects to `/docs`, the interactive FastAPI Swagger UI for exploring and testing endpoints.
- Command Line: Use `curl` or PowerShell's `Invoke-WebRequest` to interact with the API. See below for examples.

**Example API Requests:**

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

Vote for a track:
```sh
# curl:
curl -X POST "http://localhost:8080/vote?id=123&up=true" -H "Content-Type: application/json" -d '{"id": 123}'
# PowerShell:
Invoke-WebRequest -Uri "http://localhost:8080/vote?id=123&up=true" -Method POST -Headers @{ "Content-Type" = "application/json" } -Body '{"id": 123}'
```

Get the current queue:
```sh
curl http://localhost:8080/queue
Invoke-WebRequest -Uri "http://localhost:8080/queue" -Method GET
```

Get track metadata:
```sh
curl http://localhost:8080/metadata/123
Invoke-WebRequest -Uri "http://localhost:8080/metadata/123" -Method GET
```

Get play history:
```sh
curl http://localhost:8080/history
Invoke-WebRequest -Uri "http://localhost:8080/history" -Method GET
```

Play the next song:
```sh
curl -X POST http://localhost:8080/play_next
Invoke-WebRequest -Uri "http://localhost:8080/play_next" -Method POST
```

**Run the REST Automated Test Suite:**

```powershell
docker compose -f layered-rest/docker-compose.yml run --rm test-runner
```

This executes all REST test scripts inside a container, using Compose DNS to reach the API via Nginx. All tests should pass if the system is running.

**Stop the REST System:**

```powershell
docker compose -f layered-rest/docker-compose.yml down
```

---

### Microservices Architecture (gRPC)

**First-Time Setup: Generate gRPC Python Files**

If you do not see `queue_pb2.py` and `queue_pb2_grpc.py` in `microservices-grpc/queue-service/` and `microservices-grpc/tests/`, you must generate them from `queue.proto` before running tests or the client locally (outside Docker). This is not needed if you only use Docker Compose, as the Docker build handles it automatically.

To generate the files manually:

```powershell
cd microservices-grpc/queue-service
python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. queue.proto
```

Repeat this in the `microservices-grpc/tests/` directory if you want to run tests directly from there.

You need `grpcio` and `grpcio-tools` installed:
```powershell
pip install grpcio grpcio-tools
```


**Build and Start the System:**

```powershell
docker compose -f microservices-grpc/docker-compose.yml up --build --scale queue-service=5 -d
```

This starts 5 gRPC queue-service nodes and a shared Redis backend. Adjust the number after `--scale` as needed.

**Run the gRPC Automated Test Suite:**

```powershell
docker compose -f microservices-grpc/docker-compose.yml run --rm test-runner
```

This executes all gRPC test scripts inside a container, using Compose DNS to reach the gRPC services. All tests should pass if the system is running.

**Manual gRPC Interaction:**

Use the provided Python client script inside a running queue-service container for all manual gRPC actions. This ensures proper networking and service discovery.

#### Example: Add, Play, and View History (gRPC)


Below are examples for every available gRPC client command. Run these from the project root.

1. **Add a track:**
   ```powershell
   docker compose -f microservices-grpc/docker-compose.yml exec queue-service python client.py add --id 123 --title "Song Title" --artist "Artist Name" --duration 200
   ```
2. **Play the next track:**
   ```powershell
   docker compose -f microservices-grpc/docker-compose.yml exec queue-service python client.py play
   ```
3. **View play history:**
   ```powershell
   docker compose -f microservices-grpc/docker-compose.yml exec queue-service python client.py history
   ```
4. **Get the current queue:**
   ```powershell
   docker compose -f microservices-grpc/docker-compose.yml exec queue-service python client.py queue
   ```
5. **Get track metadata:**
   ```powershell
   docker compose -f microservices-grpc/docker-compose.yml exec queue-service python client.py metadata --id 123
   ```
6. **Vote for a track:**
   ###### Upvote
   ```powershell
   docker compose -f microservices-grpc/docker-compose.yml exec queue-service python client.py vote --id 123 --up true
   ```
   ###### Downvote
   ```powershell
   docker compose -f microservices-grpc/docker-compose.yml exec queue-service python client.py vote --id 123 --up false
   ```
7. **Remove a track:**
   ```powershell
   docker compose -f microservices-grpc/docker-compose.yml exec queue-service python client.py remove --id 123
   ```
---
