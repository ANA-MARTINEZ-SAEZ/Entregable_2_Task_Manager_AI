"""Rutas CRUD para gestionar tareas."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.controllers.task_manager import TaskManager
from app.models.task import Task
from app.schemas.task_schema import TaskCreate, TaskResponse, TaskUpdate

router = APIRouter(tags=["tasks"])
task_manager = TaskManager()


@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks() -> list[dict]:
    """Devuelve el listado completo de tareas."""
    try:
        tasks = task_manager.load_tasks()
        return [task.to_dict() for task in tasks]
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al leer tareas: {exc}",
        ) from exc


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(task_id: str) -> dict:
    """Devuelve una tarea por su identificador."""
    try:
        task = task_manager.get_task_by_id(task_id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al leer tareas: {exc}",
        ) from exc

    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada.")
    return task.to_dict()


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate) -> dict:
    """Crea una nueva tarea."""
    try:
        task = Task(**task_data.model_dump())
        created_task = task_manager.create_task(task)
        return created_task.to_dict()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al guardar la tarea: {exc}",
        ) from exc


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: str, task_data: TaskUpdate) -> dict:
    """Actualiza una tarea existente."""
    updated_data = task_data.model_dump(exclude_unset=True, exclude_none=True)

    try:
        updated_task = task_manager.update_task(task_id, updated_data)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al actualizar la tarea: {exc}",
        ) from exc

    if updated_task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada.")
    return updated_task.to_dict()


@router.delete("/tasks/{task_id}")
def delete_task(task_id: str) -> dict[str, str]:
    """Elimina una tarea existente."""
    try:
        deleted = task_manager.delete_task(task_id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error interno al eliminar la tarea: {exc}",
        ) from exc

    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tarea no encontrada.")
    return {"message": "Tarea eliminada correctamente."}
