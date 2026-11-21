
"""Notification microservice - entry point."""

import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from py_eureka_client import eureka_client

from app.routers import notification

PORT = int(os.getenv("PORT", "8084"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Register the service in Eureka
    await eureka_client.init_async(
        eureka_server="http://localhost:8761/eureka/",
        app_name="NOTIFICATION",
        instance_id=f"notification:localhost:{PORT}",
        instance_host="localhost",
        instance_ip="127.0.0.1",
        instance_port=PORT,
        home_page_url=f"http://localhost:{PORT}/",
        status_page_url=f"http://localhost:{PORT}/info",
        health_check_url=f"http://localhost:{PORT}/health",
    )

    print("NOTIFICATION successfully registered with Eureka!")

    yield

    # Stop Eureka client
    await eureka_client.stop_async()


app = FastAPI(
    title="Notification Microservice API",
    version="1.0.0",
    description=(
        "Notification microservice (Python / FastAPI, no database). "
        "Only the hello endpoint is implemented; the notification logic is to be developed by students."
    ),
    contact={"name": "Badia Abouhdid"},
    servers=[{"url": f"http://localhost:{PORT}", "description": "Local"}],
    docs_url="/swagger-ui",
    openapi_url="/v3/api-docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)


# ---- Health check ----
@app.get("/health")
async def health():
    return {
        "status": "UP",
        "service": "NOTIFICATION"
    }


# ---- Service information ----
@app.get("/info")
async def info():
    return {
        "app": "NOTIFICATION",
        "description": "Notification microservice",
        "version": "1.0.0"
    }


# ---- Notification routes ----
app.include_router(notification.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=PORT, reload=True)
