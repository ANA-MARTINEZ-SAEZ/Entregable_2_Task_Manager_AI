"""Servicio centralizado de IA generativa para tareas."""

from __future__ import annotations

import os
import re
from decimal import Decimal, InvalidOperation
from typing import Any

from openai import AzureOpenAI, OpenAI

VALID_CATEGORIES = (
    "Frontend",
    "Backend",
    "Testing",
    "Infra",
    "Documentación",
    "Gestión",
    "Diseño",
    "Datos",
    "Otra",
)

AZURE_ENV_VARS = (
    "AZURE_OPENAI_API_KEY",
    "AZURE_OPENAI_ENDPOINT",
    "AZURE_OPENAI_DEPLOYMENT",
)


class AITaskServiceError(Exception):
    """Error controlado del servicio de IA."""


def _is_azure_configured() -> bool:
    """Indica si hay alguna variable de Azure OpenAI informada."""
    return any(os.getenv(var) for var in AZURE_ENV_VARS)


def _get_azure_config() -> dict[str, str]:
    """Valida y devuelve la configuracion de Azure OpenAI."""
    config = {
        "api_key": os.getenv("AZURE_OPENAI_API_KEY"),
        "endpoint": os.getenv("AZURE_OPENAI_ENDPOINT"),
        "deployment": os.getenv("AZURE_OPENAI_DEPLOYMENT"),
        "api_version": os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-15-preview"),
    }

    missing = [
        env_name
        for env_name, value in (
            ("AZURE_OPENAI_API_KEY", config["api_key"]),
            ("AZURE_OPENAI_ENDPOINT", config["endpoint"]),
            ("AZURE_OPENAI_DEPLOYMENT", config["deployment"]),
        )
        if not value
    ]
    if missing:
        raise AITaskServiceError(
            "Configuración de Azure OpenAI incompleta. "
            f"Faltan estas variables en .env: {', '.join(missing)}"
        )

    return config


def _get_llm_client() -> tuple[OpenAI | AzureOpenAI, str]:
    """Obtiene el cliente de IA y el modelo o deployment a utilizar."""
    if _is_azure_configured():
        config = _get_azure_config()
        client = AzureOpenAI(
            api_key=config["api_key"],
            api_version=config["api_version"],
            azure_endpoint=config["endpoint"],
        )
        return client, config["deployment"]

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise AITaskServiceError(
            "No hay configuración de IA disponible. "
            "Configura las variables AZURE_OPENAI_* o OPENAI_API_KEY en tu archivo .env."
        )

    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    return OpenAI(api_key=api_key), model


def _call_llm(system_prompt: str, user_prompt: str) -> str:
    """Realiza una llamada al modelo de IA y devuelve el texto generado."""
    client, model = _get_llm_client()

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
    except Exception as exc:
        provider = "Azure OpenAI" if _is_azure_configured() else "OpenAI"
        raise AITaskServiceError(f"Error al comunicarse con {provider}: {exc}") from exc

    content = response.choices[0].message.content
    if not content:
        raise AITaskServiceError("El servicio de IA devolvió una respuesta vacía.")

    return content.strip()


def _format_task_context(task_data: dict[str, Any]) -> str:
    """Construye un resumen legible de los datos de la tarea."""
    lines = [
        f"Título: {task_data.get('title', '')}",
        f"Prioridad: {task_data.get('priority', '')}",
        f"Estado: {task_data.get('status', '')}",
        f"Asignado a: {task_data.get('assigned_to', '')}",
    ]

    optional_fields = {
        "Descripción": task_data.get("description"),
        "Horas de esfuerzo": task_data.get("effort_hours"),
        "Categoría": task_data.get("category"),
    }
    for label, value in optional_fields.items():
        if value not in (None, ""):
            lines.append(f"{label}: {value}")

    return "\n".join(lines)


def generate_description(task_data: dict[str, Any]) -> str:
    """Genera una descripción profesional a partir de los datos de la tarea."""
    system_prompt = (
        "Eres un asistente experto en gestión de proyectos de software. "
        "Genera descripciones claras, profesionales y concisas de tareas. "
        "Responde únicamente con el texto de la descripción, sin encabezados ni listas."
    )
    user_prompt = (
        "Genera una descripción profesional para la siguiente tarea:\n\n"
        f"{_format_task_context(task_data)}"
    )
    return _call_llm(system_prompt, user_prompt)


def categorize_task(task_data: dict[str, Any]) -> str:
    """Clasifica la tarea en una de las categorías recomendadas."""
    categories_text = ", ".join(VALID_CATEGORIES)
    system_prompt = (
        "Eres un asistente experto en clasificación de tareas de desarrollo de software. "
        f"Clasifica cada tarea en exactamente una de estas categorías: {categories_text}. "
        "Responde únicamente con el nombre exacto de la categoría, sin explicaciones."
    )
    user_prompt = (
        "Clasifica la siguiente tarea:\n\n"
        f"{_format_task_context(task_data)}"
    )
    category = _call_llm(system_prompt, user_prompt).strip()

    for valid_category in VALID_CATEGORIES:
        if category.lower() == valid_category.lower():
            return valid_category

    return category


def _parse_effort_hours(raw_value: str) -> Decimal:
    """Convierte la respuesta del LLM a un valor numérico de horas."""
    cleaned = raw_value.strip().replace(",", ".")
    match = re.search(r"\d+(?:\.\d+)?", cleaned)
    if not match:
        raise ValueError(f"No se pudo convertir la estimación a número: {raw_value!r}")

    try:
        effort = Decimal(match.group())
    except InvalidOperation as exc:
        raise ValueError(f"Valor numérico inválido: {raw_value!r}") from exc

    if effort < 0:
        raise ValueError("Las horas de esfuerzo no pueden ser negativas.")

    return effort


def estimate_effort(task_data: dict[str, Any]) -> Decimal:
    """Estima las horas de esfuerzo necesarias para completar la tarea."""
    system_prompt = (
        "Eres un asistente experto en estimación de esfuerzo en proyectos de software. "
        "Estima las horas necesarias para completar la tarea. "
        "Responde únicamente con un número decimal (por ejemplo: 4 o 2.5), sin texto adicional."
    )
    user_prompt = (
        "Estima las horas de esfuerzo para la siguiente tarea:\n\n"
        f"{_format_task_context(task_data)}"
    )
    raw_response = _call_llm(system_prompt, user_prompt)
    return _parse_effort_hours(raw_response)


def analyze_risks(task_data: dict[str, Any]) -> str:
    """Genera un análisis de riesgos para la tarea."""
    system_prompt = (
        "Eres un asistente experto en análisis de riesgos de proyectos de software. "
        "Identifica riesgos técnicos, de plazo, de calidad y de dependencias. "
        "Responde con un análisis claro y estructurado en texto continuo o párrafos breves."
    )
    user_prompt = (
        "Analiza los riesgos de la siguiente tarea:\n\n"
        f"{_format_task_context(task_data)}"
    )
    return _call_llm(system_prompt, user_prompt)


def generate_risk_mitigation(task_data: dict[str, Any], risk_analysis: str) -> str:
    """Genera un plan de mitigación basado en la tarea y su análisis de riesgos."""
    system_prompt = (
        "Eres un asistente experto en gestión de riesgos de proyectos de software. "
        "Propón acciones concretas y prácticas para mitigar los riesgos identificados. "
        "Responde con un plan claro y accionable."
    )
    user_prompt = (
        "Genera un plan de mitigación para la siguiente tarea:\n\n"
        f"{_format_task_context(task_data)}\n\n"
        f"Análisis de riesgos previo:\n{risk_analysis}"
    )
    return _call_llm(system_prompt, user_prompt)
