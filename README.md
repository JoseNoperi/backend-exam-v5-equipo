# Backend Examen v5 - El Hotel

API REST en **FastAPI** para gestionar pisos y habitaciones de un hotel.
Examen de Programación Backend con Frameworks (061CE038), variante 5.

**Equipo 5**
- Jose Alberto Noperi Beltran (@JoseNoperi)
- Julian Enrique Vizcarra Perez (@loter231)
- Paulino Antonio Manzano Segura (@PaulinoSeg)

## Requisitos
- Python 3.10 o superior
- pip

## Instalación y ejecución
```bash
python -m venv .venv
source .venv/bin/activate        # fish: source .venv/bin/activate.fish
                                 # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --port 8000
```
El servidor queda en http://localhost:8000. Documentación interactiva en http://localhost:8000/docs.

## Endpoints
| Método | Ruta | Descripción |
|---|---|---|
| POST | `/api/rooms` | Crea una habitación (201 + `Location`) |
| GET | `/api/rooms` | Lista con filtros `parent_id`, `min_quantity`, paginación `limit`/`offset` y `X-Total-Count` |
| GET | `/api/rooms/{id}` | Obtiene una habitación (200 / 404) |
| PUT | `/api/rooms/{id}` | Reemplaza (200) o crea con ese id (201) |
| PATCH | `/api/rooms/{id}` | No soportado (siempre 405) |
| DELETE | `/api/rooms/{id}` | Borra (204 / 404) |
| GET | `/api/floors/{id}/rooms` | Habitaciones de un piso (200 / 404) |
| DELETE | `/api/floors/{id}` | Borra un piso sin hijos (204); con hijos 409; inexistente 404 |
| POST | `/api/_reset` | Restaura los datos iniciales y el contador de ids (204) |

## Reglas principales
- Validación en orden: esquema (422) → piso existente (422) → código duplicado (409).
- El `code` distingue mayúsculas de minúsculas (`ABC` ≠ `abc`).
- Los ids nunca se reutilizan; el contador sigue después del id más alto.
- Ninguna respuesta incluye `internal_note`.
- CORS: solo se permite el origen `http://localhost:3000` (preflight responde 204).
- Los datos viven en memoria.

## Verificación
```bash
python run_steps.py
```
Ejecuta `POST /api/_reset` y los 20 pasos del examen en orden. Los resultados están en `EXAM.md`.

## Estructura
```
app/main.py        # API completa
app/__init__.py
run_steps.py       # reproduce los 20 pasos
requirements.txt
EXAM.md            # resultados y bitácora de IA
```

## Probar contra el servidor encendido

Con la API corriendo en el puerto 8000, en otra terminal:

```bash
# Reiniciar los datos (204)
curl -i -X POST http://localhost:8000/api/_reset

# Paso 1: total de habitaciones (X-Total-Count: 145)
curl -i "http://localhost:8000/api/rooms?limit=5"

# Paso 3: límite fuera de rango (422)
curl -i "http://localhost:8000/api/rooms?limit=101"

# Paso 5: crear habitación (201, id 146, con Location)
curl -i -X POST http://localhost:8000/api/rooms \
  -H "Content-Type: application/json" \
  -d '{"parent_id": 2, "title": "Nuevo", "quantity": 4, "code": "NEW-1"}'

# Paso 11: PATCH no soportado (405)
curl -i -X PATCH http://localhost:8000/api/rooms/1 \
  -H "Content-Type: application/json" -d '{"quantity": 9}'

# Paso 20: CORS con el origen permitido (204 + Access-Control-Allow-Origin)
curl -i -X OPTIONS http://localhost:8000/api/rooms \
  -H "Origin: http://localhost:3000" \
  -H "Access-Control-Request-Method: POST"
```

Los 20 pasos completos se ejecutan de una vez con `python run_steps.py`.
Documentación interactiva: http://localhost:8000/docs