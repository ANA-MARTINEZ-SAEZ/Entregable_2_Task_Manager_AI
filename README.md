# Task Manager API

API para gestionar tareas asignadas a usuarios, desarrollada con **FastAPI** y persistencia en archivo **JSON**.

Este proyecto corresponde al entregable 1 del Programa Avanzado en Inteligencia Artificial para Programar.

---

## Nota sobre FastAPI

Aunque el enunciado original menciona Flask, este proyecto se ha implementado con FastAPI por ser un framework moderno para construir APIs REST.

Se mantiene la arquitectura solicitada en la práctica:

- Rutas.
- Controladores.
- Clase `Task`.
- Clase `TaskManager`.
- Persistencia en archivo JSON.
- Endpoints CRUD.
- Respuestas en formato JSON.

---

## Tecnologías usadas

- Python
- FastAPI
- Uvicorn
- Pydantic
- Pytest
- JSON

---

## Estructura del proyecto

```text
task_manager_app/
│
├── app/
│   ├── main.py
│   ├── models/
│   │   └── task.py
│   ├── controllers/
│   │   └── task_manager.py
│   ├── routes/
│   │   └── task_routes.py
│   └── schemas/
│       └── task_schema.py
│
├── data/
│   └── tasks.json
│
├── tests/
│   └── test_tasks.py
│
├── AGENTS.md
├── plan.md
├── requirements.txt
├── README.md
└── .gitignore
```

Descripción de carpetas principales:

- `app/`: código principal de la aplicación.
- `app/models/`: contiene la clase de dominio `Task`.
- `app/controllers/`: contiene la clase `TaskManager`, encargada de la lógica de gestión de tareas.
- `app/routes/`: contiene los endpoints de la API.
- `app/schemas/`: contiene los esquemas Pydantic para validación de datos.
- `data/`: contiene el archivo `tasks.json`, usado como almacenamiento.
- `tests/`: contiene las pruebas automáticas con pytest.

---

## Instalación en Mac/Linux

Desde la carpeta raíz del proyecto `task_manager_app`, ejecutar:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Si en Mac el comando `python` no funciona, usar:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## Instalación en Windows

Desde la carpeta raíz del proyecto `task_manager_app`, ejecutar:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Ejecutar la API

Desde la carpeta raíz del proyecto `task_manager_app`, ejecutar:

```bash
uvicorn app.main:app --reload
```

Si todo es correcto, la terminal mostrará un mensaje indicando que el servidor está disponible en:

```text
http://127.0.0.1:8000
```

---

## Acceso a Swagger

FastAPI genera automáticamente una interfaz Swagger para probar la API.

Abrir en el navegador:

```text
http://127.0.0.1:8000/docs
```

---

## Endpoints disponibles

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/tasks` | Obtener todas las tareas |
| GET | `/tasks/{task_id}` | Obtener una tarea por ID |
| POST | `/tasks` | Crear una nueva tarea |
| PUT | `/tasks/{task_id}` | Actualizar una tarea existente |
| DELETE | `/tasks/{task_id}` | Eliminar una tarea existente |

---

## Ejemplo JSON para crear una tarea

Endpoint:

```text
POST /tasks
```

Cuerpo de la petición:

```json
{
  "title": "Preparar entregable 1",
  "description": "Crear API de gestión de tareas con FastAPI",
  "priority": "alta",
  "effort_hours": 2.5,
  "status": "pendiente",
  "assigned_to": "Ana"
}
```

---

## Valores válidos

### Priority

El campo `priority` solo admite estos valores:

- `baja`
- `media`
- `alta`
- `bloqueante`

### Status

El campo `status` solo admite estos valores:

- `pendiente`
- `en progreso`
- `en revisión`
- `completada`

---

## Persistencia de datos

Las tareas se guardan en el archivo:

```text
data/tasks.json
```

Si el archivo no existe, la aplicación lo crea automáticamente con una lista vacía:

```json
[]
```

---

## Ejecutar pruebas automáticas

Desde la carpeta raíz del proyecto `task_manager_app`, con el entorno virtual activado, ejecutar:

```bash
python -m pytest
```

Si todo está correcto, el resultado esperado será similar a:

```text
9 passed
```

Las pruebas comprueban:

- Creación de tareas.
- Listado de tareas.
- Consulta de tarea por ID.
- Actualización de tareas.
- Eliminación de tareas.
- Error 404 para tareas inexistentes.
- Error 422 para prioridad no válida.
- Error 422 para estado no válido.
- Error 422 para horas de esfuerzo negativas.

---

## Archivos que no deben incluirse en la entrega

No deben incluirse en el ZIP final:

- `venv/`
- `__pycache__/`
- `.pytest_cache/`
- archivos `.pyc`

Estos archivos ya están contemplados en `.gitignore`.

---

## Entrega

La entrega final debe contener el proyecto completo con:

- Código fuente.
- Archivo `data/tasks.json`.
- Archivo `requirements.txt`.
- Archivo `README.md`.
- Archivo `plan.md`.
- Pruebas automáticas.
- Estructura de carpetas del proyecto.

El proyecto debe comprimirse en formato `.zip` según el formato solicitado en la práctica.
