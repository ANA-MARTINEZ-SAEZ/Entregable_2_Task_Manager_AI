# Historial de preguntas y respuestas

Este documento resume las preguntas que me has ido haciendo en esta sesión y las respuestas que te he dado.

---

## 1) Estructura inicial del proyecto

**Pregunta:**  
Leer `plan.md` y `AGENTS.md` y crear solo la estructura base (carpetas y ficheros iniciales), sin lógica.

**Respuesta:**  
Se creó la estructura base completa en `task_manager_app`:

- `app/`, `app/models/`, `app/controllers/`, `app/routes/`, `app/schemas/`
- `data/`, `tests/`
- `__init__.py` necesarios
- `README.md`, `requirements.txt`, `.gitignore`, `data/tasks.json`

Con contenido mínimo inicial y sin lógica de negocio.

---

## 2) Fase 2: Modelo `Task`

**Pregunta:**  
Ejecutar solo Fase 2 implementando `app/models/task.py`.

**Respuesta:**  
Se implementó la clase `Task` con:

- Campos requeridos: `id`, `title`, `description`, `priority`, `effort_hours`, `status`, `assigned_to`
- `id` UUID string automático si no se proporciona
- `effort_hours` como `Decimal`
- Métodos `to_dict()` y `from_dict()`

Sin tocar TaskManager, rutas ni esquemas.

---

## 3) Fase 3: Esquemas Pydantic

**Pregunta:**  
Ejecutar solo Fase 3 en `app/schemas/task_schema.py`.

**Respuesta:**  
Se implementaron:

- `TaskCreate`
- `TaskUpdate` (campos opcionales)
- `TaskResponse`

Con validaciones:

- `priority`: `baja`, `media`, `alta`, `bloqueante`
- `status`: `pendiente`, `en progreso`, `en revisión`, `completada`
- `effort_hours >= 0`
- `title` no vacío
- `assigned_to` no vacío

---

## 4) Fase 4: Clase `TaskManager`

**Pregunta:**  
Ejecutar solo Fase 4 en `app/controllers/task_manager.py`.

**Respuesta:**  
Se implementó `TaskManager` con métodos:

- `load_tasks()`
- `save_tasks(tasks)`
- `create_task(task)`
- `get_task_by_id(task_id)`
- `update_task(task_id, updated_data)`
- `delete_task(task_id)`

Características:

- Usa `pathlib`
- Persiste solo en `data/tasks.json`
- Crea `tasks.json` con `[]` si no existe
- Devuelve `[]` si archivo vacío
- Lanza excepción controlada si JSON inválido
- Guarda JSON con indentación legible

---

## 5) Fase 5: Configuración FastAPI

**Pregunta:**  
Ejecutar solo Fase 5 en `app/main.py`.

**Respuesta:**  
Se configuró FastAPI con:

- Título: `Task Manager API`
- Descripción solicitada
- Versión: `1.0.0`

Y registro del router preparado para la siguiente fase.

---

## 6) Fase 6: Rutas y endpoints CRUD

**Pregunta:**  
Ejecutar solo Fase 6 implementando `app/routes/task_routes.py` y revisar `app/main.py`.

**Respuesta:**  
Se implementaron endpoints:

- `GET /tasks`
- `GET /tasks/{task_id}`
- `POST /tasks`
- `PUT /tasks/{task_id}`
- `DELETE /tasks/{task_id}`

Incluyendo:

- Uso de `TaskManager`
- Uso de `TaskCreate`, `TaskUpdate`, `TaskResponse`
- Uso de `Task`
- `HTTPException` para `404`
- Manejo de errores internos como `500`

Y en `app/main.py` se registró el router para que las rutas queden accesibles directamente en `/tasks`.

---

## 7) Fase 8: Pruebas automáticas con pytest

**Pregunta:**  
Ejecutar solo Fase 8 en `tests/test_tasks.py`.

**Respuesta:**  
Se creó batería de 9 tests con `pytest` + `TestClient` para:

1. Crear tarea
2. Listar tareas
3. Obtener tarea por ID
4. Actualizar tarea
5. Eliminar tarea
6. 404 para tarea inexistente
7. 422 por `priority` inválida
8. 422 por `status` inválido
9. 422 por `effort_hours` negativo

Se usó `tmp_path` + `monkeypatch` para no depender de `data/tasks.json` real y mantener aislamiento.

---

## 8) Fase 9: README

**Pregunta:**  
Ejecutar solo Fase 9 completando `README.md`.

**Respuesta:**  
Se completó `README.md` con:

- Descripción del proyecto
- Nota de uso de FastAPI
- Tecnologías
- Estructura
- Instalación en Mac/Linux y Windows
- Ejecución de API
- Swagger
- Endpoints
- JSON de ejemplo
- Valores válidos
- Ejecución de pruebas y resultado esperado (`9 passed`)
- Persistencia en `data/tasks.json`
- Exclusiones para entrega (`venv/`, `__pycache__/`, `.pytest_cache/`, `.pyc`)

---

## 9) Revisión final previa a entrega

**Pregunta:**  
Hacer revisión final del cumplimiento del entregable sin modificar código.

**Respuesta:**  
Se reportó:

- Cumplimiento general de arquitectura, modelos, controlador, rutas, validaciones, tests, README, `requirements.txt` y `.gitignore`
- Riesgos menores detectados:
  - Posible confusión de ruta/carpeta final al generar ZIP
  - Punto técnico sobre serialización decimal como `float`
  - Recomendación de verificar localmente el `9 passed` antes de cerrar entrega

---

## 10) Solicitud actual

**Pregunta:**  
Crear un fichero `.md` con todas las preguntas y respuestas.

**Respuesta:**  
Documento creado en:

- `task_manager_app/preguntas_respuestas.md`

