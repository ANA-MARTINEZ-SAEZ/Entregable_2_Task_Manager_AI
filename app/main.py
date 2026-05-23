"""Configuracion principal de la aplicacion FastAPI."""

from fastapi import FastAPI
from app.routes.task_routes import router as task_router

app = FastAPI(
    title="Task Manager API",
    description="API para gestionar tareas asignadas a usuarios usando FastAPI y persistencia en JSON.",
    version="1.0.0",
)

app.include_router(task_router)
