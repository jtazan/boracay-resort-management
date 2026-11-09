from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.auth import create_access_token, get_current_user, validate_demo_credentials
from app.models import LoginRequest, TokenResponse
from app.store import (
    cancel_reservation,
    create_reservation,
    get_alerts,
    get_dashboard_summary,
    get_network_segments,
    get_properties,
    get_reservations,
    update_reservation,
)

app = FastAPI(
    title="Boracay Resort Management",
    version="1.0.0",
    description="Cloud-managed hospitality operations dashboard for Boracay Island Resort Group",
)

BASE_DIR = Path(__file__).resolve().parent.parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content={
            "error": "Validation failed",
            "message": "The request payload is invalid.",
            "details": exc.errors(),
        },
    )


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.__class__.__name__,
            "message": exc.detail,
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "error": "InternalServerError",
            "message": "An unexpected error occurred. Please try again later.",
        },
    )


@app.get("/")
async def root() -> FileResponse:
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/api/health")
async def health() -> dict:
    return {
        "status": "ok",
        "service": "Boracay Resort Management",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.post("/api/auth/login", response_model=TokenResponse)
async def login(payload: LoginRequest):
    if not validate_demo_credentials(payload.username, payload.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    token = create_access_token(payload.username, role="admin")
    return TokenResponse(access_token=token, role="admin")


@app.get("/api/dashboard")
async def dashboard(user: dict = Depends(get_current_user)) -> dict:
    return get_dashboard_summary()


@app.get("/api/properties")
async def list_properties(user: dict = Depends(get_current_user)) -> list[dict]:
    return get_properties()


@app.get("/api/network-segments")
async def network_segments(user: dict = Depends(get_current_user)) -> list[dict]:
    return get_network_segments()


@app.get("/api/reservations")
async def list_reservations(user: dict = Depends(get_current_user)) -> list[dict]:
    return get_reservations()


@app.get("/api/alerts")
async def list_alerts(user: dict = Depends(get_current_user)) -> list[dict]:
    return get_alerts()


@app.post("/api/reservations", status_code=201)
async def create_reservation_route(payload: "ReservationCreate", user: dict = Depends(get_current_user)) -> dict:
    try:
        return create_reservation(payload.model_dump())
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc


@app.put("/api/reservations/{reservation_id}")
async def update_reservation_route(reservation_id: str, payload: "ReservationUpdate", user: dict = Depends(get_current_user)) -> dict:
    try:
        return update_reservation(reservation_id, payload.model_dump(exclude_unset=True))
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Reservation not found") from exc
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@app.delete("/api/reservations/{reservation_id}")
async def delete_reservation_route(reservation_id: str, user: dict = Depends(get_current_user)) -> dict:
    try:
        return cancel_reservation(reservation_id)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Reservation not found") from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
