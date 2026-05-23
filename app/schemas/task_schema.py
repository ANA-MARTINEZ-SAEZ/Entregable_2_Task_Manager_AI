"""Esquemas Pydantic para validar datos de tareas."""

from decimal import Decimal
from typing import Literal, Optional

from pydantic import BaseModel, Field, field_validator

PriorityValue = Literal["baja", "media", "alta", "bloqueante"]
StatusValue = Literal["pendiente", "en progreso", "en revisión", "completada"]


class TaskCreate(BaseModel):
    """Datos requeridos para crear una tarea."""

    title: str
    description: str
    priority: PriorityValue
    effort_hours: Decimal = Field(ge=0)
    status: StatusValue
    assigned_to: str

    @field_validator("title", "assigned_to")
    @classmethod
    def validate_non_empty_text(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Este campo no debe estar vacío.")
        return value


class TaskUpdate(BaseModel):
    """Datos opcionales para actualizar una tarea."""

    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[PriorityValue] = None
    effort_hours: Optional[Decimal] = Field(default=None, ge=0)
    status: Optional[StatusValue] = None
    assigned_to: Optional[str] = None

    @field_validator("title", "assigned_to")
    @classmethod
    def validate_optional_non_empty_text(cls, value: Optional[str]) -> Optional[str]:
        if value is not None and not value.strip():
            raise ValueError("Este campo no debe estar vacío.")
        return value


class TaskResponse(BaseModel):
    """Datos devueltos por la API para una tarea."""

    id: str
    title: str
    description: str
    priority: PriorityValue
    effort_hours: Decimal = Field(ge=0)
    status: StatusValue
    assigned_to: str