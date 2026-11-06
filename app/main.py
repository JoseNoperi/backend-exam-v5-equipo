from fastapi import FastAPI, Request, Response, HTTPException, Query
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, StrictInt, StrictStr, Field
from typing import Optional

ALLOWED_ORIGIN = "http://localhost:3000"

app = FastAPI(title="Hotel API v5")

FLOORS: dict = {}
ROOMS: dict = {}
STATE = {"next_id": 1}


def seed():
    FLOORS.clear()
    ROOMS.clear()
    names = {1: "Piso 1", 2: "Piso 2", 3: "Piso 3", 4: "Piso 4", 5: "Piso 5", 6: "Penthouse"}
    for k, v in names.items():
        FLOORS[k] = {"id": k, "name": v}
    for i in range(1, 146):
        title = f"Vista al jardín {i}" if i % 3 == 0 else (f"Suite {i}" if i % 3 == 1 else f"Sencilla {i}")
        ROOMS[i] = {
            "id": i,
            "parent_id": (i * 5 % 6) + 1,
            "title": title,
            "quantity": ((i * 13 + 14) % 20) + 1,
            "code": f"ROO-{i:04d}",
            "internal_note": f"cc-{i * 7}",
        }
    STATE["next_id"] = max(ROOMS) + 1


seed()


class RoomIn(BaseModel):
    parent_id: StrictInt
    title: StrictStr = Field(min_length=1)
    quantity: StrictInt = Field(ge=1)
    code: StrictStr = Field(min_length=1)


def public(r: dict) -> dict:
    return {k: v for k, v in r.items() if k != "internal_note"}


# ---------- CORS (manual: el preflight debe responder 204) ----------
@app.middleware("http")
async def cors(request: Request, call_next):
    origin = request.headers.get("origin")
    allowed = origin == ALLOWED_ORIGIN
    if request.method == "OPTIONS" and "access-control-request-method" in request.headers:
        resp = Response(status_code=204)
        if allowed:
            resp.headers["Access-Control-Allow-Origin"] = origin
            resp.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            resp.headers["Access-Control-Allow-Headers"] = request.headers.get(
                "access-control-request-headers", "Content-Type")
            resp.headers["Vary"] = "Origin"
        return resp
    resp = await call_next(request)
    if allowed:
        resp.headers["Access-Control-Allow-Origin"] = origin
        resp.headers["Access-Control-Expose-Headers"] = "X-Total-Count, Location"
        resp.headers["Vary"] = "Origin"
    return resp


@app.exception_handler(RequestValidationError)
async def validation_handler(request, exc):
    return JSONResponse(status_code=422, content={"detail": "Validation error"})


# ---------- validación común: esquema (ya hecho por pydantic) -> padre -> código duplicado ----------
def check_body(body: RoomIn, exclude_id: Optional[int] = None):
    if body.parent_id not in FLOORS:
        raise HTTPException(422, "parent_id no existe")
    for r in ROOMS.values():
        if r["code"] == body.code and r["id"] != exclude_id:
            raise HTTPException(409, "code duplicado")


@app.post("/api/_reset", status_code=204)
def reset():
    seed()
    return Response(status_code=204)


@app.post("/api/rooms", status_code=201)
def create_room(body: RoomIn, response: Response):
    check_body(body)
    rid = STATE["next_id"]
    STATE["next_id"] += 1
    ROOMS[rid] = {"id": rid, **body.model_dump(), "internal_note": ""}
    response.headers["Location"] = f"/api/rooms/{rid}"
    return public(ROOMS[rid])


@app.get("/api/rooms")
def list_rooms(
    response: Response,
    parent_id: Optional[int] = None,
    min_quantity: Optional[int] = None,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    items = sorted(ROOMS.values(), key=lambda r: r["id"])
    if parent_id is not None:
        items = [r for r in items if r["parent_id"] == parent_id]
    if min_quantity is not None:
        items = [r for r in items if r["quantity"] >= min_quantity]
    response.headers["X-Total-Count"] = str(len(items))
    return [public(r) for r in items[offset:offset + limit]]


@app.get("/api/rooms/{rid}")
def get_room(rid: int):
    if rid not in ROOMS:
        raise HTTPException(404, "No encontrada")
    return public(ROOMS[rid])


@app.put("/api/rooms/{rid}")
def put_room(rid: int, body: RoomIn, response: Response):
    check_body(body, exclude_id=rid)
    existed = rid in ROOMS
    note = ROOMS[rid]["internal_note"] if existed else ""
    ROOMS[rid] = {"id": rid, **body.model_dump(), "internal_note": note}
    if rid >= STATE["next_id"]:
        STATE["next_id"] = rid + 1
    if not existed:
        response.status_code = 201
        response.headers["Location"] = f"/api/rooms/{rid}"
    return public(ROOMS[rid])


@app.patch("/api/rooms/{rid}")
def patch_room(rid: int):
    return Response(status_code=405, headers={"Allow": "GET, PUT, DELETE"})


@app.delete("/api/rooms/{rid}", status_code=204)
def delete_room(rid: int):
    if rid not in ROOMS:
        raise HTTPException(404, "No encontrada")
    del ROOMS[rid]
    return Response(status_code=204)


@app.get("/api/floors/{fid}/rooms")
def floor_rooms(fid: int):
    if fid not in FLOORS:
        raise HTTPException(404, "Piso no encontrado")
    return [public(r) for r in sorted(ROOMS.values(), key=lambda r: r["id"]) if r["parent_id"] == fid]


@app.delete("/api/floors/{fid}", status_code=204)
def delete_floor(fid: int):
    if fid not in FLOORS:
        raise HTTPException(404, "Piso no encontrado")
    if any(r["parent_id"] == fid for r in ROOMS.values()):
        raise HTTPException(409, "El piso tiene habitaciones")
    del FLOORS[fid]
    return Response(status_code=204)