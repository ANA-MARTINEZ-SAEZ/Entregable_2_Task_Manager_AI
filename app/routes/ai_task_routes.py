"""Rutas de IA generativa para enriquecer tareas."""

from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from app.schemas.task_schema import TaskAIInput, TaskResponse
from app.services import ai_task_service

router = APIRouter(prefix="/ai/tasks", tags=["AI Tasks"])


def _build_task_response(task_data: TaskAIInput, **updates: object) -> dict:
    """Construye la respuesta enriquecida manteniendo los datos originales."""
    response = task_data.model_dump()
    response.update(updates)

    if not response.get("id"):
        response["id"] = str(uuid4())
    if response.get("description") is None:
        response["description"] = ""
    if response.get("effort_hours") is None:
        response["effort_hours"] = Decimal("0")
    else:
        response["effort_hours"] = float(response["effort_hours"])

    return response


@router.post("/describe", response_model=TaskResponse)
def describe_task(task_data: TaskAIInput) -> dict:
    """Genera una descripción profesional para la tarea recibida."""
    try:
        description = ai_task_service.generate_description(task_data.model_dump())
    except ai_task_service.AITaskServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    return _build_task_response(task_data, description=description)


@router.post("/categorize", response_model=TaskResponse)
def categorize_task(task_data: TaskAIInput) -> dict:
    """Clasifica la tarea en una categoría mediante IA."""
    try:
        category = ai_task_service.categorize_task(task_data.model_dump())
    except ai_task_service.AITaskServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    return _build_task_response(task_data, category=category)


@router.post("/estimate", response_model=TaskResponse)
def estimate_task_effort(task_data: TaskAIInput) -> dict:
    """Estima las horas de esfuerzo de la tarea mediante IA."""
    try:
        effort_hours = ai_task_service.estimate_effort(task_data.model_dump())
    except ai_task_service.AITaskServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(exc),
        ) from exc

    return _build_task_response(task_data, effort_hours=effort_hours)


@router.post("/audit", response_model=TaskResponse)
def audit_task(task_data: TaskAIInput) -> dict:
    """Genera análisis de riesgos y plan de mitigación para la tarea."""
    task_dict = task_data.model_dump()

    try:
        risk_analysis = ai_task_service.analyze_risks(task_dict)
        risk_mitigation = ai_task_service.generate_risk_mitigation(task_dict, risk_analysis)
    except ai_task_service.AITaskServiceError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    return _build_task_response(
        task_data,
        risk_analysis=risk_analysis,
        risk_mitigation=risk_mitigation,
    )
