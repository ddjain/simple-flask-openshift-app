# simple-flask-openshift-app

Python Flask application created to demonstrate containerization and deployment on Red Hat OpenShift.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| GET | `/items` | List all items |
| POST | `/items` | Create a new item |

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

## Usage Examples

```bash
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
