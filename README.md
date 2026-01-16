# Simple Flask OpenShift App

A modular Python Flask application demonstrating containerization and deployment on Red Hat OpenShift with HPA auto-scaling.

## Features

- ✅ REST API with modular blueprints
- ✅ Health check endpoint
- ✅ Items CRUD operations
- ✅ Load testing endpoints for HPA testing
- ✅ File read/write operations
- ✅ Horizontal Pod Autoscaler (HPA)
- ✅ Round-robin load balancing

## Project Structure

```
simple-flask-openshift-app/
├── app.py                      # Main Flask application
├── routes/
│   ├── __init__.py             # Blueprint exports
│   ├── main.py                 # Home & health endpoints
│   ├── items.py                # Items CRUD endpoints
│   ├── load_testing.py         # HPA load testing endpoints
│   └── file_operations.py      # File read/write endpoints
├── scripts/
│   └── load_generator.sh       # Load testing script
├── openshift/
│   ├── imagestream.yaml        # Image storage
│   ├── buildconfig.yaml        # Build from Git
│   ├── deployment.yaml         # Deployment config
│   ├── service.yaml            # Internal service
│   ├── route.yaml              # External route
│   └── hpa.yaml                # Horizontal Pod Autoscaler
├── Dockerfile
├── requirements.txt
└── README.md
```

## API Endpoints

### Main Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message with API documentation |
| GET | `/health` | Health check |

### Items Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/items` | List all items |
| POST | `/items` | Create a new item |
| GET | `/items/<id>` | Get item by ID |
| DELETE | `/items/<id>` | Delete item by ID |

### Load Testing Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/load/memory/<mb>` | Allocate MB of memory |
| POST | `/load/memory/clear` | Clear allocated memory |
| GET | `/load/status` | Get memory allocation status |

### File Operations Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/file/write` | Write content to a file |
| GET | `/file/read/<filename>` | Read file content |
| GET | `/file/list` | List all files |
| DELETE | `/file/delete/<filename>` | Delete a file |

## Local Development

### Setup

```bash
# Create virtual environment
uv venv --python 3.12

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt
```

### Run

```bash
python app.py
```

The app will be available at `http://localhost:8080`.

## Docker

### Build

```bash
docker build -t flask-app .
```

### Run

```bash
docker run -p 8080:8080 flask-app
```

## OpenShift Deployment

### Deploy All Resources

```bash
# Login to OpenShift
oc login --token=<token> --server=<server>

# Create project
oc new-project flask-demo

# Apply all OpenShift configs
oc apply -f openshift/

# Start a build
oc start-build simple-flask-app --follow
```

### Useful Commands

```bash
# Check resources
oc get pods,svc,route,hpa -l app=simple-flask-app

# View logs
oc logs -f deployment/simple-flask-app

# Watch HPA
oc get hpa -w

# Trigger new build
oc start-build simple-flask-app --follow
```

## Usage Examples

### Main Endpoints

```bash
# Get welcome message
curl http://localhost:8080/
# Response: {"app_id": "...", "message": "Welcome to Simple Flask App!", "endpoints": {...}}

# Health check
curl http://localhost:8080/health
# Response: {"status": "healthy"}
```

### Items CRUD

```bash
# List all items
curl http://localhost:8080/items
# Response: {"items": []}

# Create an item
curl -X POST -H "Content-Type: application/json" \
  -d '{"name": "my item"}' \
  http://localhost:8080/items
# Response: {"id": 1, "name": "my item"}

# Get item by ID
curl http://localhost:8080/items/1
# Response: {"id": 1, "name": "my item"}

# Delete item
curl -X DELETE http://localhost:8080/items/1
# Response: {"message": "Item deleted", "item": {"id": 1, "name": "my item"}}
```

### Load Testing (for HPA)

```bash
# Allocate 50MB of memory
curl -X POST http://localhost:8080/load/memory/50
# Response: {"allocated_mb": 50, "app_id": "...", "chunks": 1, "message": "Allocated 50MB"}

# Check memory status
curl http://localhost:8080/load/status
# Response: {"allocated_mb": 50, "app_id": "...", "chunks": 1, "timestamp": "..."}

# Clear all memory
curl -X POST http://localhost:8080/load/memory/clear
# Response: {"app_id": "...", "cleared_mb": 50, "message": "Memory cleared"}
```

### File Operations

```bash
# Write a file
curl -X POST -H "Content-Type: application/json" \
  -d '{"filename": "test.txt", "content": "Hello, World!"}' \
  http://localhost:8080/file/write
# Response: {"filepath": "/data/test.txt", "message": "File 'test.txt' written successfully", "size_bytes": 13}

# Read a file
curl http://localhost:8080/file/read/test.txt
# Response: {"content": "Hello, World!", "filename": "test.txt", "size_bytes": 13}

# List all files
curl http://localhost:8080/file/list
# Response: {"data_path": "/data", "files": [{"filename": "test.txt", "size_bytes": 13}], "total_files": 1}

# Delete a file
curl -X DELETE http://localhost:8080/file/delete/test.txt
# Response: {"app_id": "...", "message": "File 'test.txt' deleted successfully"}
```

## Testing HPA Auto-Scaling

### 1. Apply HPA

```bash
oc apply -f openshift/hpa.yaml
```

### 2. Watch Pods and HPA

```bash
# Terminal 1: Watch pods
oc get pods -l app=simple-flask-app -w

# Terminal 2: Watch HPA
oc get hpa simple-flask-app -w
```

### 3. Generate Load

Use the load generator script:

```bash
chmod +x scripts/load_generator.sh
./scripts/load_generator.sh
```

Or manually:

```bash
# Allocate memory on multiple pods
for i in {1..20}; do
  curl -X POST http://<route-url>/load/memory/10
  sleep 0.5
done
```

### 4. Clear Load and Watch Scale Down

```bash
# Clear memory
for i in {1..10}; do
  curl -X POST http://<route-url>/load/memory/clear
done
```

## HPA Configuration

| Setting | Value | Description |
|---------|-------|-------------|
| Min Replicas | 2 | Minimum pods |
| Max Replicas | 10 | Maximum pods |
| CPU Target | 80% | Scale up when CPU > 80% |
| Memory Target | 80% | Scale up when memory > 80% |
| Scale Up Window | 10s | Quick scale up |
| Scale Down Window | 10s | Quick scale down |

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `APP_ID` | UUID | Unique instance identifier |
| `DATA_PATH` | `/data` | File storage path |

## License

MIT
