from fastapi import FastAPI
from app.otel_instrumentation import setup_tracing
import logging

# Configure FastAPI
app = FastAPI(title="FastAPI OTel Demo", version="1.0.0")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize tracing (connects to OTel Collector)
setup_tracing(service_name="fastapi-demo")

@app.get("/hello")
def hello():
    """Simple example endpoint"""
    logger.info("Received /hello request")
    return {"message": "Hello from FastAPI with OpenTelemetry!"}

@app.get("/health")
def health():
    return {"status": "ok"}