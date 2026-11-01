{% if cookiecutter.use_fastapi %}"""FastAPI application for {{ cookiecutter.project_name }}."""

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from {{ cookiecutter.package_name }} import __version__

app = FastAPI(
    title="{{ cookiecutter.project_name }}",
    description="{{ cookiecutter.project_description }}",
    version=__version__,
)


@app.get("/")
async def root() -> JSONResponse:
    """Root endpoint with a greeting."""
    return JSONResponse({"message": "Hello from {{ cookiecutter.project_name }}"})


@app.get("/health")
async def health() -> JSONResponse:
    """Health check endpoint."""
    return JSONResponse({"status": "healthy"})
{%- endif %}
