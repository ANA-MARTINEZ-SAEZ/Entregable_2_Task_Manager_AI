# Instrucciones para el agente - Proyecto Task Manager

## Contexto del proyecto

Este proyecto corresponde al entregable 1 del Programa Avanzado en Inteligencia Artificial para Programar.

El objetivo es desarrollar una API de gestión de tareas asignadas a usuarios.

Aunque el enunciado original menciona Flask, el proyecto se implementará con FastAPI, manteniendo los mismos objetivos funcionales y arquitectónicos:

- Arquitectura organizada por ficheros.
- Clase `Task`.
- Clase `TaskManager`.
- Persistencia en archivo JSON.
- Endpoints CRUD.
- Respuestas en formato JSON.
- Pruebas manuales en Swagger.
- Pruebas automáticas con pytest.

El documento principal de planificación es `plan.md`. Debe respetarse durante todo el desarrollo.

---

## Reglas generales de trabajo

- No rehacer el proyecto desde cero si ya existe código funcional.
- No eliminar archivos, clases, métodos o pruebas sin justificación.
- No cambiar la arquitectura definida en `plan.md` salvo que sea necesario y esté justificado.
- Mantener el código claro, sencillo 
- No usar base de datos. La persistencia debe hacerse en `data/tasks.json`.
- No añadir autenticación, JWT, usuarios reales ni funcionalidades futuras salvo que se pidan expresamente.

---

## Arquitectura obligatoria

El proyecto debe mantener esta separación:

- `app/models/task.py`: clase `Task`.
- `app/controllers/task_manager.py`: clase `TaskManager`.
- `app/routes/task_routes.py`: endpoints de la API.
- `app/schemas/task_schema.py`: esquemas Pydantic.
- `app/main.py`: instancia principal de FastAPI y registro de rutas.
- `data/tasks.json`: almacenamiento de tareas.
- `tests/test_tasks.py`: pruebas automáticas con pytest.

---

## Reglas para la clase Task

La clase `Task` debe representar una tarea con estos campos:

- `id`
- `title`
- `description`
- `priority`
- `effort_hours`
- `status`
- `assigned_to`

Debe incluir estos métodos:

- `to_dict()`
- `from_dict()`

El campo `id` debe generarse como UUID en formato string.

---

## Reglas para TaskManager

La clase `TaskManager` debe encargarse de:

- Cargar tareas desde `data/tasks.json`.
- Guardar tareas en `data/tasks.json`.
- Crear tareas.
- Buscar tareas por ID.
- Actualizar tareas.
- Eliminar tareas.

Las rutas no deben contener lógica de negocio compleja. Deben llamar a `TaskManager`.

---

## Reglas para FastAPI y Pydantic

Se deben usar esquemas Pydantic para validar entradas y salidas.

Valores válidos de `priority`:

- `baja`
- `media`
- `alta`
- `bloqueante`

Valores válidos de `status`:

- `pendiente`
- `en progreso`
- `en revisión`
- `completada`

El campo `effort_hours` debe ser decimal y no negativo.

---

## Endpoints obligatorios

La API debe incluir estos endpoints:

- `GET /tasks`
- `GET /tasks/{id}`
- `POST /tasks`
- `PUT /tasks/{id}`
- `DELETE /tasks/{id}`

Debe manejar errores correctamente:

- `404` cuando una tarea no exista.
- `422` cuando los datos enviados no sean válidos.
- `500` si existe un error interno de lectura o escritura del JSON.

---

## Pruebas

Deben existir pruebas con pytest para:

- Crear una tarea.
- Listar tareas.
- Obtener una tarea por ID.
- Actualizar una tarea.
- Eliminar una tarea.
- Comprobar error 404.
- Comprobar validaciones 422.

Las pruebas no deben romper ni depender innecesariamente de datos manuales del archivo `tasks.json`.

---

## Entrega

La entrega final debe incluir:

- Código fuente.
- `data/tasks.json`.
- `requirements.txt`.
- `README.md`.
- Pruebas.
- `plan.md`.

No debe incluir:

- `venv/`
- `__pycache__/`
- `.pytest_cache/`
