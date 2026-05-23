"""Modelo de dominio para representar tareas."""

from __future__ import annotations

from dataclasses import dataclass, field
from decimal import Decimal
from typing import Any
from uuid import uuid4


@dataclass
class Task:
    """Representa una tarea del sistema."""

    title: str
    description: str
    priority: str
    effort_hours: Decimal
    status: str
    assigned_to: str
    id: str = field(default_factory=lambda: str(uuid4()))

    def __post_init__(self) -> None:
        """Asegura tipos consistentes tras la construccion."""
        self.id = str(self.id)
        self.effort_hours = Decimal(str(self.effort_hours))

    def to_dict(self) -> dict[str, Any]:
        """Convierte la tarea a un diccionario serializable."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority,
            "effort_hours": float(self.effort_hours),
            "status": self.status,
            "assigned_to": self.assigned_to,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Task":
        """Crea una instancia de Task a partir de un diccionario."""
        return cls(
            id=str(data["id"]) if data.get("id") is not None else str(uuid4()),
            title=data["title"],
            description=data["description"],
            priority=data["priority"],
            effort_hours=Decimal(str(data["effort_hours"])),
            status=data["status"],
            assigned_to=data["assigned_to"],
        )
