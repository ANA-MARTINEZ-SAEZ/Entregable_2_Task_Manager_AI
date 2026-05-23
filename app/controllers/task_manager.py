"""Controlador para gestionar tareas en archivo JSON."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from app.models.task import Task


class TaskManager:
    """Gestiona operaciones CRUD de tareas sobre `data/tasks.json`."""

    def __init__(self, data_file: Path | None = None) -> None:
        project_root = Path(__file__).resolve().parents[2]
        self.data_file = data_file or (project_root / "data" / "tasks.json")

    def load_tasks(self) -> list[Task]:
        """Carga tareas desde JSON y las convierte a objetos Task."""
        self.data_file.parent.mkdir(parents=True, exist_ok=True)

        if not self.data_file.exists():
            self.data_file.write_text("[]", encoding="utf-8")
            return []

        file_content = self.data_file.read_text(encoding="utf-8").strip()
        if not file_content:
            return []

        try:
            raw_data = json.loads(file_content)
        except json.JSONDecodeError as exc:
            raise ValueError("El archivo tasks.json tiene un formato JSON invalido.") from exc

        if not isinstance(raw_data, list):
            raise ValueError("El contenido de tasks.json debe ser una lista de tareas.")

        try:
            return [Task.from_dict(item) for item in raw_data]
        except (TypeError, KeyError, ValueError) as exc:
            raise ValueError("Una o mas tareas en tasks.json tienen formato invalido.") from exc

    def save_tasks(self, tasks: list[Task]) -> None:
        """Guarda una lista de objetos Task en JSON legible."""
        serializable_tasks = [task.to_dict() for task in tasks]
        self.data_file.parent.mkdir(parents=True, exist_ok=True)
        self.data_file.write_text(
            json.dumps(serializable_tasks, indent=4, ensure_ascii=False),
            encoding="utf-8",
        )

    def create_task(self, task: Task) -> Task:
        """Crea una nueva tarea y la persiste en el JSON."""
        tasks = self.load_tasks()
        tasks.append(task)
        self.save_tasks(tasks)
        return task

    def get_task_by_id(self, task_id: str) -> Task | None:
        """Busca una tarea por su identificador."""
        tasks = self.load_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: str, updated_data: dict[str, Any]) -> Task | None:
        """Actualiza los campos recibidos de una tarea existente."""
        tasks = self.load_tasks()
        for task in tasks:
            if task.id != task_id:
                continue

            for field_name, value in updated_data.items():
                if field_name != "id" and hasattr(task, field_name):
                    setattr(task, field_name, value)

            self.save_tasks(tasks)
            return task

        return None

    def delete_task(self, task_id: str) -> bool:
        """Elimina una tarea por ID si existe."""
        tasks = self.load_tasks()
        for index, task in enumerate(tasks):
            if task.id == task_id:
                tasks.pop(index)
                self.save_tasks(tasks)
                return True
        return False
