# 🐳 Topic 07 — API Serving & Containerized Inference Concepts
> **Schedule:** Day 1 | 8:00 PM – 9:00 PM | Duration: 60 min
> **Folder:** `day1/07_api_serving_containers/`
> **Status:** 🔲 Pending Build

---

## 🎯 Learning Objectives
1. Wrap a trained ML model in a production-ready REST API using FastAPI
2. Understand Docker concepts: images, containers, layers, volumes, and networking
3. Write a production-grade Dockerfile for ML inference
4. Test inference endpoints with curl and validate responses

---

## 🧠 Core Concepts

### 1. Why API Serving?
| Problem with Direct Model Access | API Solution |
|----------------------------------|-------------|
| Language-locked (Python only) | REST is language-agnostic |
| No versioning | `/v1/predict`, `/v2/predict` routes |
| No input validation | Pydantic enforces schema |
| No horizontal scaling | Containers scale independently |
| No monitoring hook | Middleware captures every request |

### 2. FastAPI for ML — Key Components

#### Request / Response Schema (Pydantic)
```python
from pydantic import BaseModel, Field
from typing import List

class PredictRequest(BaseModel):
    age: int = Field(..., ge=18, le=120, description="Customer age")
    income: float = Field(..., gt=0, description="Annual income in USD")
    credit_score: int = Field(..., ge=300, le=850)
    employment_years: float = Field(..., ge=0)

class PredictResponse(BaseModel):
    prediction: int           # 0 = No Default, 1 = Default
    probability: float        # Probability of default
    confidence: str           # "High" / "Medium" / "Low"
    model_version: str
```

#### FastAPI App Structure
```python
from fastapi import FastAPI, HTTPException
from contextlib import asynccontextmanager
import joblib, logging

logger = logging.getLogger(__name__)
model = None  # Global model reference

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    logger.info("Loading model at startup...")
    model = joblib.load("models/model.pkl")
    logger.info("Model loaded successfully")
    yield
    logger.info("Shutting down...")

app = FastAPI(
    title="ML Inference API",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/v1/predict", response_model=PredictResponse)
async def predict(request: PredictRequest):
    try:
        features = [[request.age, request.income,
                     request.credit_score, request.employment_years]]
        prob = model.predict_proba(features)[0][1]
        pred = int(prob >= 0.5)
        confidence = "High" if abs(prob - 0.5) > 0.3 else "Medium" if abs(prob - 0.5) > 0.1 else "Low"
        return PredictResponse(
            prediction=pred,
            probability=round(prob, 4),
            confidence=confidence,
            model_version="1.0.0"
        )
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
```

### 3. Docker Fundamentals
**Analogy:** Image = recipe (blueprint), Container = dish (running instance)

#### Key Dockerfile Instructions
| Instruction | Purpose |
|-------------|---------|
| `FROM` | Base image (python:3.11-slim) |
| `WORKDIR` | Set working directory inside container |
| `COPY` | Copy files from host to image |
| `RUN` | Execute command during image build |
| `ENV` | Set environment variables |
| `EXPOSE` | Document which port the app listens on |
| `CMD` | Command to run when container starts |

#### Production Dockerfile
```dockerfile
# Use slim image to minimize size
FROM python:3.11-slim

# Metadata
LABEL maintainer="your-team@company.com"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Install dependencies FIRST (cache optimization)
# If code changes but requirements don't, this layer is cached
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app/ ./app/
COPY models/ ./models/

# Non-root user for security
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s \
  CMD curl -f http://localhost:8000/health || exit 1

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4. Docker Commands Reference
```bash
# Build image
docker build -t ml-api:1.0.0 .

# Run container
docker run -d -p 8000:8000 --name ml-api ml-api:1.0.0

# Test endpoint
curl -X POST http://localhost:8000/v1/predict \
  -H "Content-Type: application/json" \
  -d '{"age": 35, "income": 75000, "credit_score": 720, "employment_years": 5}'

# View logs
docker logs ml-api

# Stop and remove
docker stop ml-api && docker rm ml-api
```

### 5. Inference Architecture Patterns
| Pattern | Use Case | Latency | Throughput |
|---------|----------|---------|------------|
| **Synchronous REST** | Single predictions, real-time | Low (ms) | Medium |
| **Async Queue** | High-volume, non-urgent | High (sec) | High |
| **Batch API** | Bulk scoring (nightly) | Very high (min) | Very high |
| **Streaming** | Continuous event scoring | Ultra-low | Very high |

---

## 📊 Diagrams & Visuals Required

| # | Diagram | Type | Notebook Cell |
|---|---------|------|---------------|
| 1 | Client → API → Model → Response architecture | Annotated flow diagram | Cell 3 |
| 2 | Docker layer cake (FROM → COPY → RUN → CMD) | Stacked rectangle diagram | Cell 6 |
| 3 | Request lifecycle flowchart (validation → inference → response) | Flowchart | Cell 8 |
| 4 | Sync vs. Async vs. Batch inference comparison | Table + timeline diagram | Cell 10 |

---

## 🏋️ Activities

### Activity 1 — Build the FastAPI App (25 min)
- Load the model trained in Session 3
- Create `main.py`, `schemas.py`, `model_loader.py`
- Run with `uvicorn app.main:app --reload`
- Test with curl: send a valid request, then an invalid request
- Explore the auto-generated docs at `http://localhost:8000/docs`

### Activity 2 — Write the Dockerfile (15 min)
- Write the production Dockerfile from scratch
- Build the image: `docker build -t ml-api:v1 .`
- Run it: `docker run -p 8000:8000 ml-api:v1`
- Confirm: `curl http://localhost:8000/health` returns `{"status": "healthy"}`

### Activity 3 — Diagram the Build Process (code)
- Use matplotlib to draw the Docker layer cake showing which layers are cached vs. rebuilt when code changes

---

## 📝 Notebook Cell Plan

```
Cell 01 [MD]   → Session intro & motivation for API serving
Cell 02 [MD]   → REST API fundamentals (verbs, status codes, JSON)
Cell 03 [Code] → Architecture diagram (client → API → model → response)
Cell 04 [MD]   → FastAPI: why it's the modern standard
Cell 05 [Code] → Full FastAPI app code walkthrough
Cell 06 [MD]   → Docker: images vs containers, layer caching
Cell 07 [Code] → Docker layer cake diagram
Cell 08 [Code] → Production Dockerfile walkthrough
Cell 09 [MD]   → Docker commands reference
Cell 10 [Code] → Inference pattern comparison diagram
Cell 11 [MD]   → Key Takeaways + Quiz
```

---

## 📁 Files to Create

```
day1/07_api_serving_containers/
├── README.md
├── notebook.ipynb
└── app/
    ├── main.py
    ├── schemas.py
    ├── model_loader.py
    ├── requirements.txt
    └── Dockerfile
```

---

## 📝 Key Takeaways
- FastAPI is the gold standard for Python ML APIs: async, auto-documented, type-safe
- Docker guarantees reproducibility across environments — no more "works on my machine"
- Always load the model once at startup, not per-request (avoid 200ms model load per call)
- Always expose a `/health` endpoint — load balancers and orchestrators depend on it
- Copy `requirements.txt` before app code to maximize Docker layer cache hits

---

## ❓ Quiz Questions
1. What is the difference between a Docker image and a Docker container?
2. Why do we `COPY requirements.txt` before `COPY app/` in the Dockerfile?
3. What does Pydantic provide that plain Python dicts don't?
4. What is the difference between sync and async FastAPI routes?
5. Why should the ML model be loaded at app startup instead of per-request?

---

## 📖 Further Reading
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Docker Best Practices for Python](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [BentoML — ML Serving Framework](https://docs.bentoml.com/)
- [Seldon Core — Production ML Serving on Kubernetes](https://docs.seldon.io/)
