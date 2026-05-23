"""Pruebas automáticas de los endpoints de IA con mocks."""

from decimal import Decimal

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services import ai_task_service


@pytest.fixture
def client() -> TestClient:
    """Cliente de pruebas para los endpoints de IA."""
    with TestClient(app) as test_client:
        yield test_client


def build_ai_task_payload() -> dict:
    """Devuelve un payload base para probar endpoints de IA."""
    return {
        "title": "Implementar login de usuarios",
        "description": "",
        "priority": "alta",
        "status": "pendiente",
        "assigned_to": "Ana",
    }


def test_describe_task_returns_generated_description(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def mock_generate_description(task_data: dict) -> str:
        return "Descripción generada por IA para la tarea de login."

    monkeypatch.setattr(ai_task_service, "generate_description", mock_generate_description)

    response = client.post("/ai/tasks/describe", json=build_ai_task_payload())

    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Descripción generada por IA para la tarea de login."
    assert data["title"] == "Implementar login de usuarios"


def test_categorize_task_returns_generated_category(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def mock_categorize_task(task_data: dict) -> str:
        return "Backend"

    monkeypatch.setattr(ai_task_service, "categorize_task", mock_categorize_task)

    response = client.post("/ai/tasks/categorize", json=build_ai_task_payload())

    assert response.status_code == 200
    data = response.json()
    assert data["category"] == "Backend"


def test_estimate_task_returns_numeric_effort_hours(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def mock_estimate_effort(task_data: dict) -> Decimal:
        return Decimal("6.5")

    monkeypatch.setattr(ai_task_service, "estimate_effort", mock_estimate_effort)

    response = client.post("/ai/tasks/estimate", json=build_ai_task_payload())

    assert response.status_code == 200
    data = response.json()
    assert float(data["effort_hours"]) == 6.5
    assert isinstance(data["effort_hours"], (int, float))


def test_audit_task_returns_risk_fields(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def mock_analyze_risks(task_data: dict) -> str:
        return "Riesgo de retraso por dependencias externas."

    def mock_generate_risk_mitigation(task_data: dict, risk_analysis: str) -> str:
        assert risk_analysis == "Riesgo de retraso por dependencias externas."
        return "Coordinar con el equipo de infraestructura y definir hitos intermedios."

    monkeypatch.setattr(ai_task_service, "analyze_risks", mock_analyze_risks)
    monkeypatch.setattr(ai_task_service, "generate_risk_mitigation", mock_generate_risk_mitigation)

    payload = build_ai_task_payload()
    payload["description"] = "Implementar autenticación JWT en la API."
    payload["effort_hours"] = 8

    response = client.post("/ai/tasks/audit", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert data["risk_analysis"] == "Riesgo de retraso por dependencias externas."
    assert data["risk_mitigation"] == (
        "Coordinar con el equipo de infraestructura y definir hitos intermedios."
    )


def test_estimate_task_invalid_llm_response_returns_422(
    client: TestClient,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def mock_estimate_effort(task_data: dict) -> Decimal:
        raise ValueError("No se pudo convertir la estimación a número: 'muchas horas'")

    monkeypatch.setattr(ai_task_service, "estimate_effort", mock_estimate_effort)

    response = client.post("/ai/tasks/estimate", json=build_ai_task_payload())

    assert response.status_code == 422
