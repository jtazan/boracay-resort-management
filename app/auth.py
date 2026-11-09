from __future__ import annotations

from datetime import datetime, timedelta, timezone
from hashlib import sha256
from secrets import compare_digest
from typing import Any

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.config import get_settings

security = HTTPBearer()


def hash_password(password: str) -> str:
    return sha256(password.encode("utf-8")).hexdigest()


def validate_demo_credentials(username: str, password: str) -> bool:
    settings = get_settings()
    if username != settings["demo_user"]:
        return False
    return compare_digest(hash_password(password), hash_password(settings["demo_password"]))


def create_access_token(username: str, role: str = "admin") -> str:
    settings = get_settings()
    now = datetime.now(timezone.utc)
    payload = {
        "sub": username,
        "role": role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings["token_ttl_minutes"])).timestamp()),
    }
    return jwt.encode(payload, settings["jwt_secret"], algorithm=settings["jwt_algorithm"])


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            credentials.credentials,
            get_settings()["jwt_secret"],
            algorithms=[get_settings()["jwt_algorithm"]],
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc

    username = payload.get("sub")
    role = payload.get("role", "admin")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token is missing subject")

    return {"username": username, "role": role}
