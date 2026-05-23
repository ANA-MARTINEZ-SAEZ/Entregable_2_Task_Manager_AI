# Task Manager API

API para gestionar tareas asignadas a usuarios, desarrollada con **FastAPI**, persistencia en archivo **JSON** e integración con **IA generativa** (OpenAI).

Este proyecto corresponde al **Entregable 2** del Programa Avanzado en Inteligencia Artificial para Programar. Extiende el Entregable 1 añadiendo endpoints de IA sobre el modelo `Task`.

---

## Nota sobre FastAPI

Aunque el enunciado original menciona Flask, este proyecto se ha implementado con FastAPI por ser un framework moderno para construir APIs REST.

Se mantiene la arquitectura solicitada en la práctica:

- Rutas.
- Controladores.
- Servicios de IA.
- Clase `Task`.
- Clase `TaskManager`.
- Persistencia en archivo JSON.
- Endpoints CRUD.
- Endpoints de IA generativa.
- Respuestas en formato JSON.

---

## Entregable 2: IA generativa

El Entregable 2 añade capacidades de enriquecimiento de tareas mediante OpenAI:

- Generar descripciones profesionales.
- Clasificar tareas por categoría.
- Estimar horas de esfuerzo.
- Auditar riesgos y proponer mitigaciones.

Estos endpoints **no persisten** automáticamente en `data/tasks.json`. Devuelven la tarea enriquecida para que puedas revisarla y, si lo deseas, guardarla con el CRUD (`POST /tasks` o `PUT /tasks/{task_id}`).

---

## Nuevos campos del modelo Task

Además de los campos originales, `Task` incluye estos campos **opcionales**:

| Campo | Tipo | Descripción |
|---|---|---|
| `category` | `str \| None` | Categoría asignada por IA o manualmente |
| `risk_analysis` | `str \| None` | Análisis de riesgos generado por IA |
| `risk_mitigation` | `str \| None` | Plan de mitigación generado por IA |

Las tareas antiguas en `data/tasks.json` que no tengan estos campos siguen siendo compatibles.

---

## Tecnologías usadas

- Python
- FastAPI
- Uvicorn
- Pydantic
- OpenAI (API oficial)
- python-dotenv
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
│   │   ├── task_routes.py
│   │   └── ai_task_routes.py
│   ├── schemas/
│   │   └── task_schema.py
│   └── services/
│       └── ai_task_service.py
│
├── data/
│   └── tasks.json
│
├── tests/
│   ├── test_tasks.py
│   └── test_ai_tasks.py
│
├── .env.example
├── AGENTS.md
├── plan.md
├── requirements.txt
├── README.md
└── .gitignore
```

---

## Configuración de variables de entorno

1. Copia el archivo de ejemplo:

```bash
cp .env.example .env
```

2. Edita `.env` y configura tu clave de OpenAI:

```env
OPENAI_API_KEY=pon_aqui_tu_clave
OPENAI_MODEL=gpt-4o-mini
```

**Importante:** no subas claves reales al repositorio. El archivo `.env` está excluido en `.gitignore`. Usa `.env.example` solo como plantilla orientativa.

Sin `OPENAI_API_KEY`, los endpoints de IA devolverán un error 500 con un mensaje claro indicando que falta la configuración.

---

## Instalación en Mac/Linux

Desde la carpeta raíz del proyecto `task_manager_app`, ejecutar:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Si en Mac el comando `python` no funciona, usar:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

---

## Instalación en Windows

Desde la carpeta raíz del proyecto `task_manager_app`, ejecutar:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

---

## Ejecutar la API

Desde la carpeta raíz del proyecto `task_manager_app`, con el entorno virtual activado y el archivo `.env` configurado:

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

En Swagger encontrarás dos grupos de endpoints:

- **tasks**: CRUD clásico.
- **AI Tasks**: endpoints de IA generativa.

---

## Endpoints CRUD (Entregable 1)

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/tasks` | Obtener todas las tareas |
| GET | `/tasks/{task_id}` | Obtener una tarea por ID |
| POST | `/tasks` | Crear una nueva tarea |
| PUT | `/tasks/{task_id}` | Actualizar una tarea existente |
| DELETE | `/tasks/{task_id}` | Eliminar una tarea existente |

---

## Endpoints de IA (Entregable 2)

| Método | Endpoint | Descripción |
|---|---|---|
| POST | `/ai/tasks/describe` | Genera una descripción profesional |
| POST | `/ai/tasks/categorize` | Clasifica la tarea en una categoría |
| POST | `/ai/tasks/estimate` | Estima las horas de esfuerzo |
| POST | `/ai/tasks/audit` | Genera análisis de riesgos y plan de mitigación |

Categorías recomendadas para `categorize`: Frontend, Backend, Testing, Infra, Documentación, Gestión, Diseño, Datos, Otra.

---

## Ejemplos JSON para Swagger

### POST /ai/tasks/describe

```json
{
  "title": "Implementar login de usuarios",
  "description": "",
  "priority": "alta",
  "status": "pendiente",
  "assigned_to": "Ana"
}
```

### POST /ai/tasks/categorize

```json
{
  "title": "Crear tests unitarios del módulo de tareas",
  "description": "Cubrir TaskManager y rutas CRUD",
  "priority": "media",
  "effort_hours": 3,
  "status": "pendiente",
  "assigned_to": "Ana"
}
```

### POST /ai/tasks/estimate

```json
{
  "title": "Migrar persistencia a PostgreSQL",
  "description": "Evaluar impacto y planificar migración",
  "priority": "bloqueante",
  "status": "pendiente",
  "assigned_to": "Equipo Backend"
}
```

### POST /ai/tasks/audit

```json
{
  "title": "Desplegar API en producción",
  "description": "Configurar servidor, dominio y certificados SSL",
  "priority": "alta",
  "effort_hours": 12,
  "status": "en progreso",
  "assigned_to": "DevOps"
}
```

### POST /tasks (CRUD clásico)

```json
{
  "title": "Preparar entregable 2",
  "description": "Añadir endpoints de IA generativa con OpenAI",
  "priority": "alta",
  "effort_hours": 2.5,
  "status": "pendiente",
  "assigned_to": "Ana",
  "category": "Backend"
}
```

---

## Valores válidos

### Priority

- `baja`
- `media`
- `alta`
- `bloqueante`

### Status

- `pendiente`
- `en progreso`
- `en revisión`
- `completada`

---

## Persistencia de datos

Las tareas se guardan en:

```text
data/tasks.json
```

Si el archivo no existe, la aplicación lo crea automáticamente con una lista vacía:

```json
[]
```

---

## Ejecutar pruebas automáticas

Desde la carpeta raíz del proyecto `task_manager_app`, con el entorno virtual activado:

```bash
python -m pytest
```

Las pruebas de IA **no llaman a OpenAI**. Usan mocks para simular las respuestas del servicio.

Resultado esperado (aproximado):

```text
14 passed
```

Las pruebas comprueban:

- CRUD completo de tareas.
- Errores 404 y 422 del CRUD.
- Endpoints de IA: describe, categorize, estimate y audit.
- Validación de respuestas numéricas en `estimate`.
- Error 422 cuando la IA devuelve un esfuerzo no convertible.

---

## Archivos que no deben incluirse en la entrega

No deben incluirse en el ZIP final:

- `venv/`
- `__pycache__/`
- `.pytest_cache/`
- `.env`
- archivos `.pyc`

Estos archivos ya están contemplados en `.gitignore`.

---

## Entrega

La entrega final debe contener el proyecto completo con:

- Código fuente.
- Archivo `data/tasks.json`.
- Archivo `requirements.txt`.
- Archivo `.env.example`.
- Archivo `README.md`.
- Archivo `plan.md`.
- Pruebas automáticas.
- Estructura de carpetas del proyecto.

El proyecto debe comprimirse en formato `.zip` según el formato solicitado en la práctica.
