# Backend Examen v5 - El Hotel (FastAPI)

## Ejecutar
```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
Docs interactivas: http://localhost:8000/docs

## Reproducir los 20 pasos
```bash
python run_steps.py
```
(Hace POST /api/_reset y ejecuta los pasos en orden.)