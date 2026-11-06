"""Ejecuta los 20 pasos del examen contra la API (TestClient, sin servidor)."""
from fastapi.testclient import TestClient
from app.main import app

c = TestClient(app)
J = {"Content-Type": "application/json"}
c.post("/api/_reset")
out = {}
r = c.get("/api/rooms?limit=5"); out[1] = r.headers["x-total-count"]
r = c.get("/api/rooms?parent_id=6&min_quantity=11"); out[2] = r.headers["x-total-count"]
out[3] = c.get("/api/rooms?limit=101").status_code
out[4] = len(c.get("/api/rooms?limit=100&offset=80").json())
r = c.post("/api/rooms", json={"parent_id": 2, "title": "Nuevo", "quantity": 4, "code": "NEW-1"})
out[5] = f"{r.status_code}, id={r.json().get('id')}, Location={'sí' if 'location' in r.headers else 'no'}"
r = c.post("/api/rooms", json={"parent_id": 3, "title": "Copia", "quantity": 2, "code": "new-1"})
out[6] = f"{r.status_code}, id={r.json().get('id') if r.status_code==201 else '-'}"
out[7] = c.post("/api/rooms", json={"parent_id": 1, "title": "X", "quantity": "muchos", "code": "BAD-1"}).status_code
out[8] = c.post("/api/rooms", json={"parent_id": 99, "title": "X", "quantity": 1, "code": "BAD-2"}).status_code
out[9] = c.put("/api/rooms/500", json={"parent_id": 1, "title": "Put", "quantity": 3, "code": "PUT-500"}).status_code
r = c.post("/api/rooms", json={"parent_id": 1, "title": "Otro", "quantity": 6, "code": "NEW-2"})
out[10] = f"{r.status_code}, id={r.json().get('id')}"
out[11] = c.patch("/api/rooms/1", json={"quantity": 9}).status_code
out[12] = c.get("/api/rooms/1").json()["quantity"]
out[13] = c.delete("/api/rooms/2").status_code
out[14] = c.delete("/api/rooms/2").status_code
out[15] = c.get("/api/floors/99/rooms").status_code
out[16] = c.delete("/api/floors/5").status_code
out[17] = c.get("/api/rooms?parent_id=5").headers["x-total-count"]
out[18] = c.get("/api/rooms?min_quantity=20").headers["x-total-count"]
r = c.options("/api/rooms", headers={"Origin": "http://localhost:5173", "Access-Control-Request-Method": "POST"})
out[19] = r.headers.get("access-control-allow-origin", "ninguno") + f" (status {r.status_code})"
r = c.options("/api/rooms", headers={"Origin": "http://localhost:3000", "Access-Control-Request-Method": "POST"})
out[20] = r.headers.get("access-control-allow-origin", "ninguno") + f" (status {r.status_code})"
for k, v in out.items():
    print(k, "|", v)
# comprobaciones extra
assert "internal_note" not in c.get("/api/rooms/1").text