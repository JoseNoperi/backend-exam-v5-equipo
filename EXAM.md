# Examen v5 - (Equipo 5)

Integrantes: 
Jose Alberto Noperi Beltran (JoseNoperi)
Julian Enrique Vizcarra Perez (loter231)
Paulino Antonio Manzano Segura (PaulinoSeg)

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
1. Herramientas usadas: Claude (Anthropic). Lo usamos para generar la primera versión de la API en FastAPI (`app/main.py`), el script `run_steps.py` que reproduce los 20 pasos y los borradores del README y de este archivo. Pasamos el PDF del examen completo como contexto. Las respuestas de la Parte 2 las discutimos entre los integrantes antes de decidirlas.

2. Algo que la IA hizo mal o no podía saber:
   - **Instrucciones de entorno:** la IA nos dio `source .venv/bin/activate`, que es para bash/zsh. Usamos fish, así que falló y hubo que usar `activate.fish`. Tampoco sabía que nuestro sistema (Arch) bloquea `pip install` global (error `externally-managed-environment`), por lo que dependimos del entorno virtual.
   - **Archivos vacíos:** al copiar los archivos generados, `app/main.py`, `README.md` y `EXAM.md` quedaron en 0 líneas. `uvicorn` falló con `Attribute "app" not found` hasta que lo detectamos con `wc -l`.
   - **CORS:** el `CORSMiddleware` estándar de FastAPI responde 200 al preflight y nuestro contrato pide 204, por lo que se implementó a mano.
   - **Validación estricta:** el contrato exige 422 ante un tipo incorrecto (paso 7). Con los tipos por defecto de pydantic, un `"5"` entre comillas se habría convertido en entero, así que se usaron `StrictInt` y `StrictStr`.
   - **Versiones:** la IA probó el código con versiones anteriores a las nuestras (instalamos FastAPI 0.162 y Python 3.14). Por eso volvimos a correrlo en nuestro entorno antes de confiar en él.
   - **Lo que no podía saber:** nuestro contrato, nuestra ficha y las reglas de este equipo solo existen en el PDF. Una API genérica no los cumple.

3. Cómo lo verificamos:
   - Ejecutamos `python run_steps.py` en nuestro entorno, que hace `POST /api/_reset` y corre los 20 pasos en orden. Comparamos los 20 resultados contra los valores esperados del contrato y la semilla.
   - Levantamos `uvicorn` y probamos con `curl` contra el servidor real: `GET /api/rooms?limit=2` dio 200 con `x-total-count: 145` y sin `internal_note`; el `OPTIONS` con `Origin: http://localhost:3000` dio 204 con `access-control-allow-origin: http://localhost:3000`; el `PATCH` dio 405.
   - Comprobamos a mano las reglas que dependen del orden: `new-1` frente a `NEW-1` crea un registro nuevo (mayúsculas distintas), el PUT del paso 9 crea el id 500 y el POST siguiente recibe el 501, y el padre inexistente da 422 antes del chequeo de código duplicado.
   - Revisamos con `git status` que `.venv/` no se subiera al repositorio.