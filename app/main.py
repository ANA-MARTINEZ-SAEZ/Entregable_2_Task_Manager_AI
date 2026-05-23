"""Configuracion principal de la aplicacion FastAPI."""

from dotenv import load_dotenv
from fastapi import FastAPI

from app.routes.ai_task_routes import router as ai_task_router
from app.routes.task_routes import router as task_router

load_dotenv()

app = FastAPI(
    title="Task Manager API",
    description=(
        "API para gestionar tareas asignadas a usuarios usando FastAPI, "
        "persistencia en JSON e integración con IA generativa."
    ),
    version="2.0.0",
)

app.include_router(task_router)
app.include_router(ai_task_router)
