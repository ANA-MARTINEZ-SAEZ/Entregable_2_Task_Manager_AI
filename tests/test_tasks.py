"""Pruebas automáticas de la API de tareas con pytest."""

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.controllers.task_manager import TaskManager
from app.main import app
from app.routes import task_routes


@pytest.fixture
def client(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    """Crea un cliente de pruebas con almacenamiento JSON temporal."""
    temp_data_file = tmp_path / "tasks.json"
    temp_data_file.write_text("[]", encoding="utf-8")

    test_manager = TaskManager(data_file=temp_data_file)
    monkeypatch.setattr(task_routes, "task_manager", test_manager)

    with TestClient(app) as test_client:
        yield test_client


def build_valid_task_payload() -> dict:
    """Devuelve un payload válido para crear tareas."""
    return {
        "title": "Preparar entrega",
        "description": "Completar entregable de API",
        "priority": "alta",
        "effort_hours": 4.5,
        "status": "pendiente",
        "assigned_to": "Ana",
    }


def test_create_task_success(client: TestClient) -> None:
    response = client.post("/tasks", json=build_valid_task_payload())

    assert response.status_code == 201
    data = response.json()
    assert "id" in data
    assert data["title"] == "Preparar entrega"


def test_get_tasks_list(client: TestClient) -> None:
    client.post("/tasks", json=build_valid_task_payload())

    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1


def test_get_task_by_id(client: TestClient) -> None:
    create_response = client.post("/tasks", json=build_valid_task_payload())
    task_id = create_response.json()["id"]

    response = client.get(f"/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json()["id"] == task_id


def test_update_task_success(client: TestClient) -> None:
    create_response = client.post("/tasks", json=build_valid_task_payload())
    task_id = create_response.json()["id"]

    update_payload = {"status": "en progreso", "effort_hours": 6}
    response = client.put(f"/tasks/{task_id}", json=update_payload)

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "en progreso"
    assert float(data["effort_hours"]) == 6.0


def test_delete_task_success(client: TestClient) -> None:
    create_response = client.post("/tasks", json=build_valid_task_payload())
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    assert delete_response.status_code == 200
    assert delete_response.json()["message"] == "Tarea eliminada correctamente."

    get_response = client.get(f"/tasks/{task_id}")
    assert get_response.status_code == 404


def test_get_task_not_found_returns_404(client: TestClient) -> None:
    response = client.get("/tasks/id-inexistente")
    assert response.status_code == 404


def test_create_task_invalid_priority_returns_422(client: TestClient) -> None:
    payload = build_valid_task_payload()
    payload["priority"] = "urgente"

    response = client.post("/tasks", json=payload)
    assert response.status_code == 422


def test_create_task_invalid_status_returns_422(client: TestClient) -> None:
    payload = build_valid_task_payload()
    payload["status"] = "iniciada"

    response = client.post("/tasks", json=payload)
    assert response.status_code == 422


def test_create_task_negative_effort_hours_returns_422(client: TestClient) -> None:
    payload = build_valid_task_payload()
    payload["effort_hours"] = -2

    response = client.post("/tasks", json=payload)
    assert response.status_code == 422
