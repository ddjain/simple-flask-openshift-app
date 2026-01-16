# simple-flask-openshift-app

Python Flask application created to demonstrate containerization and deployment on Red Hat OpenShift.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message with app info |
| GET | `/health` | Health check |
| GET | `/items` | List all items |
| POST | `/items` | Create a new item |
| POST | `/load/memory/<mb>` | Allocate MB of memory (for HPA testing) |
| POST | `/load/memory/clear` | Clear allocated memory |
| GET | `/load/status` | Get current memory allocation status |

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
# Create project
oc new-project flask-demo

# Apply all OpenShift configs
oc apply -f openshift/

# Start a build
oc start-build simple-flask-app --follow
```

### OpenShift Resources

| File | Resource | Description |
|------|----------|-------------|
| `imagestream.yaml` | ImageStream | Stores built container images |
| `buildconfig.yaml` | BuildConfig | Builds from Git using Dockerfile |
| `deployment.yaml` | Deployment | Deploys pods with health checks |
| `service.yaml` | Service | Internal networking (ClusterIP) |
| `route.yaml` | Route | External access with round-robin LB |
| `hpa.yaml` | HPA | Auto-scales pods based on CPU/memory |

## Usage Examples

### Basic Endpoints

```bash
# Welcome message
curl http://localhost:8080/
# Response: {"app_id": "...", "message": "Welcome to Simple Flask App!", ...}

# Health check
curl http://localhost:8080/health
# Response: {"status": "healthy"}

# Get all items
curl http://localhost:8080/items
# Response: {"items": []}

# Create an item
curl -X POST -H "Content-Type: application/json" \
  -d '{"name": "my item"}' \
  http://localhost:8080/items
# Response: {"id": 1, "name": "my item"}
```

### Load Testing Endpoints (for HPA Testing)

```bash
# Allocate 50MB of memory
curl -X POST http://localhost:8080/load/memory/50
# Response: {"allocated_mb": 50, "app_id": "...", "chunks": 1, "message": "Allocated 50MB of memory"}

# Check current memory allocation
curl http://localhost:8080/load/status
# Response: {"allocated_mb": 50, "app_id": "...", "chunks": 1, "timestamp": "..."}

# Clear all allocated memory
curl -X POST http://localhost:8080/load/memory/clear
# Response: {"app_id": "...", "cleared_mb": 50, "message": "Memory cleared"}
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

### 3. Generate Memory Load

```bash
# Allocate memory across multiple pods to trigger scaling
for i in {1..10}; do
  curl -X POST http://<route-url>/load/memory/50
  sleep 1
done
```

### 4. Watch Pods Scale Up

The HPA will automatically scale up pods when memory utilization exceeds the threshold.

### 5. Clear Memory and Watch Scale Down

```bash
# Clear memory on all pods
for i in {1..10}; do
  curl -X POST http://<route-url>/load/memory/clear
done
```

## Project Structure

```
simple-flask-openshift-app/
├── app.py                  # Main Flask application
├── load_testing.py         # Load testing endpoints (Blueprint)
├── Dockerfile              # Container build instructions
├── requirements.txt        # Python dependencies
├── README.md
└── openshift/
    ├── imagestream.yaml    # Image storage
    ├── buildconfig.yaml    # Build configuration
    ├── deployment.yaml     # Deployment with resources
    ├── service.yaml        # Internal service
    ├── route.yaml          # External route (round-robin)
    └── hpa.yaml            # Horizontal Pod Autoscaler
```
