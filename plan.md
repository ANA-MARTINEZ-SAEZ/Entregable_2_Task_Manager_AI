# Plan de Trabajo - Proyecto Task Manager con FastAPI

## 1. Enfoque general

El objetivo es desarrollar una API para gestionar tareas asignadas a usuarios.

Aunque el enunciado original menciona Flask, el proyecto se implementará con FastAPI por ser un framework moderno para crear APIs REST. Objetivos principales:

- Arquitectura organizada por ficheros.
- Clase `Task`.
- Clase `TaskManager`.
- Persistencia en archivo JSON.
- Endpoints CRUD.
- Respuestas en formato JSON.
- Pruebas manuales en Swagger.
- Pequeña batería de pruebas automáticas con `pytest`.

---

## 2. Estructura del proyecto

```text
task_manager_app/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py
│   │
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── task_manager.py
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── task_routes.py
│   │
│   └── schemas/
│       ├── __init__.py
│       └── task_schema.py
│
├── data/
│   └── tasks.json
│
├── tests/
│   ├── __init__.py
│   └── test_tasks.py
│
├── .gitignore
├── requirements.txt
└── README.md
```

Nota: la carpeta `venv/` se creará para trabajar en local, pero no se incluirá en la entrega final.

---

## 3. Fase 1: configuración inicial

Tareas:

- Crear la carpeta raíz `task_manager_app/`.
- Crear el entorno virtual.
- Instalar dependencias.
- Crear `requirements.txt`.
- Crear `.gitignore`.

Comandos iniciales:

```bash
python -m venv venv
```

Activación en Windows:

```bash
venv\Scripts\activate
```

Activación en Mac/Linux:

```bash
source venv/bin/activate
```

Instalación de dependencias:

```bash
pip install fastapi uvicorn pytest httpx
pip freeze > requirements.txt
```

Contenido recomendado de `.gitignore`:

```text
venv/
__pycache__/
*.pyc
.pytest_cache/
```

---

## 4. Fase 2: modelo Task

Archivo:

```text
app/models/task.py
```

Responsabilidad:

- Representar una tarea.
- Convertir una tarea a diccionario.
- Crear una tarea desde un diccionario.

Campos de la tarea:

- `id`
- `title`
- `description`
- `priority`
- `effort_hours`
- `status`
- `assigned_to`

Valores válidos:

```text
priority: baja, media, alta, bloqueante
status: pendiente, en progreso, en revisión, completada
```

Métodos:

- `to_dict()`
- `from_dict()`

Decisiones:

- El campo `id` se generará como UUID en formato string.
- El campo `effort_hours` será decimal.
- El campo `assigned_to` será texto libre.

---

## 5. Fase 3: esquemas Pydantic

Archivo:

```text
app/schemas/task_schema.py
```

Responsabilidad:

- Validar los datos de entrada.
- Definir los datos de salida.
- Documentar automáticamente la API en Swagger.

Esquemas previstos:

- `TaskCreate`: datos necesarios para crear una tarea.
- `TaskUpdate`: datos permitidos para actualizar una tarea.
- `TaskResponse`: datos devueltos al cliente.

Validaciones:

- `priority` solo podrá tener los valores permitidos.
- `status` solo podrá tener los valores permitidos.
- `effort_hours` deberá ser un número decimal igual o mayor que 0.
- `title` no deberá estar vacío.

---

## 6. Fase 4: clase TaskManager

Archivo:

```text
app/controllers/task_manager.py
```

Responsabilidad:

- Leer tareas desde `data/tasks.json`.
- Guardar tareas en `data/tasks.json`.
- Gestionar las operaciones CRUD.

Métodos:

- `load_tasks()`
- `save_tasks()`
- `create_task()`
- `get_task_by_id()`
- `update_task()`
- `delete_task()`

Decisiones:

- Si `tasks.json` no existe, se creará automáticamente.
- Si no hay tareas, el archivo tendrá una lista vacía:

```json
[]
```

- El `TaskManager` trabajará con objetos `Task`.
- Las rutas llamarán al `TaskManager`, evitando poner lógica de negocio directamente en los endpoints.

---

## 7. Fase 5: configuración de FastAPI

Archivo:

```text
app/main.py
```

Responsabilidad:

- Crear la instancia principal de FastAPI.
- Registrar las rutas de tareas.
- Configurar título y descripción de la API.

Ejemplo de ejecución:

```bash
uvicorn app.main:app --reload
```

URL de Swagger:

```text
http://localhost:8000/docs
```

---

## 8. Fase 6: rutas y endpoints

Archivo:

```text
app/routes/task_routes.py
```

Endpoints necesarios:

| Método | Endpoint | Acción |
|---|---|---|
| GET | `/tasks` | Leer todas las tareas |
| GET | `/tasks/{id}` | Leer una tarea específica |
| POST | `/tasks` | Crear una tarea |
| PUT | `/tasks/{id}` | Actualizar una tarea |
| DELETE | `/tasks/{id}` | Eliminar una tarea |

Manejo de errores:

| Caso | Respuesta |
|---|---|
| Tarea no encontrada | 404 |
| Datos inválidos | 422 |
| Error interno al leer o guardar JSON | 500 |

Formato estándar de error:

```json
{
  "detail": "Mensaje del error"
}
```

---

## 9. Fase 7: pruebas manuales

Las pruebas manuales se harán desde Swagger:

```text
http://localhost:8000/docs
```

Pruebas mínimas:

- Crear una tarea con `POST /tasks`.
- Listar todas las tareas con `GET /tasks`.
- Consultar una tarea concreta con `GET /tasks/{id}`.
- Actualizar una tarea con `PUT /tasks/{id}`.
- Eliminar una tarea con `DELETE /tasks/{id}`.
- Verificar que `data/tasks.json` se actualiza correctamente.
- Probar errores con un `id` inexistente.
- Probar validaciones con estados o prioridades no válidas.

---

## 10. Fase 8: pruebas automáticas con pytest

Archivo:

```text
tests/test_tasks.py
```

Objetivo:

Crear una pequeña batería de pruebas automáticas para comprobar que la API funciona correctamente y dejar una base preparada para futuros entregables.

Pruebas previstas:

- Crear tarea correctamente.
- Obtener listado de tareas.
- Obtener tarea por `id`.
- Actualizar tarea existente.
- Eliminar tarea existente.
- Devolver error 404 si la tarea no existe.
- Devolver error 422 si `priority` no es válida.
- Devolver error 422 si `status` no es válido.
- Devolver error 422 si `effort_hours` es negativo.

Comando para ejecutar las pruebas:

```bash
pytest
```

---

## 11. Fase 9: README

Archivo:

```text
README.md
```

Debe incluir:

- Descripción breve del proyecto.
- Tecnologías usadas.
- Estructura de carpetas.
- Instrucciones para crear y activar el entorno virtual.
- Instalación de dependencias.
- Ejecución del servidor.
- Acceso a Swagger.
- Ejecución de pruebas con `pytest`.
- Ejemplos básicos de uso de los endpoints.

---

## 12. Fase 10: entrega final

Nombre de la carpeta de entrega:

```text
m2_proyecto_nombre_apellido/
```

Contenido de la entrega:

```text
m2_proyecto_nombre_apellido/
├── app/
├── data/
├── tests/
├── .gitignore
├── requirements.txt
└── README.md
```

No incluir:

```text
venv/
__pycache__/
.pytest_cache/
```

Comprimir en ZIP:

```text
m2_proyecto_nombre_apellido.zip
```

---

## 13. Criterios de finalización

El proyecto se considerará terminado cuando:

- La estructura de carpetas esté creada correctamente.
- Exista la clase `Task` con `to_dict()` y `from_dict()`.
- Exista la clase `TaskManager` con carga, guardado y CRUD.
- Los endpoints funcionen correctamente.
- Los datos se guarden en `data/tasks.json`.
- Las validaciones principales estén implementadas.
- Swagger permita probar la API.
- Las pruebas de `pytest` se ejecuten correctamente.
- El README explique cómo ejecutar y probar el proyecto.
- La entrega esté preparada en formato ZIP.
