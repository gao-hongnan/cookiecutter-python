{% if cookiecutter.use_fastapi %}"""FastAPI application for {{ cookiecutter.project_name }}."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(
    title="{{ cookiecutter.project_name }}",
    description="{{ cookiecutter.project_description }}",
    version="0.1.0",
)


@app.get("/")
async def root() -> JSONResponse:
    """Root endpoint with a greeting."""
    return JSONResponse({"message": "Hello from {{ cookiecutter.project_name }}"})


@app.get("/health")
async def health() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse({"status": "healthy"})
{% endif %}
