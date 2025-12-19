from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    # Startup
    logger.info("Starting Intellica Backend...")
    # TODO: Initialize database connections
    # TODO: Load ML models
    # TODO: Connect to MQTT broker
    yield
    # Shutdown
    logger.info("Shutting down Intellica Backend...")
    # TODO: Close database connections
    # TODO: Disconnect from MQTT broker

app = FastAPI(
    title="Intellica API",
    description="AI-Powered Sənaye Optimallaşma Platforması",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "Intellica Backend is running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "services": {
            "api": "operational",
            "database": "pending",  # TODO: Check database connection
            "redis": "pending",     # TODO: Check Redis connection
            "rabbitmq": "pending"   # TODO: Check RabbitMQ connection
        }
    }

# TODO: Import and include API routers
# from api.v1 import machines, sensors, recommendations, defects, analytics
# app.include_router(machines.router, prefix="/api/v1/machines", tags=["machines"])
# app.include_router(sensors.router, prefix="/api/v1/sensors", tags=["sensors"])
# app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["recommendations"])
# app.include_router(defects.router, prefix="/api/v1/defects", tags=["defects"])
# app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)