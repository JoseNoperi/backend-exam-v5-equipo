# Examen v5 - (Equipo 5)

Integrantes: (nombre completo y usuario de GitHub de cada uno)

Framework y cómo ejecutar: FastAPI - `uvicorn app.main:app --port 8000`

| Paso | Lo que obtuvimos |
| ---- | ---------------- |
| 1 | X-Total-Count = 145 |
| 2 | X-Total-Count = 11 |
| 3 | 422 |
| 4 | 65 registros |
| 5 | 201, id 146, Location: sí |
| 6 | 201, id 147 |
| 7 | 422 |
| 8 | 422 |
| 9 | 201 |
| 10 | 201, id 501 |
| 11 | 405 |
| 12 | quantity = 8 |
| 13 | 204 |
| 14 | 404 |
| 15 | 404 |
| 16 | 409 |
| 17 | X-Total-Count = 23 |
| 18 | X-Total-Count = 8 |
| 19 | ninguno |
| 20 | http://localhost:3000 |

## Bitácora de IA
1. Herramientas usadas: Claude (Anthropic) para generar la API en FastAPI y el script de pasos.
2. Algo que la IA hizo mal o no podía saber: (EDITEN: p. ej. el CORSMiddleware estándar responde 200 al preflight y el contrato pide 204; la IA no conocía nuestro contrato/ficha.)
3. Cómo lo verificamos: (EDITEN: corrimos `run_steps.py` y también las peticiones con curl contra uvicorn real.)