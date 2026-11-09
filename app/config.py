from __future__ import annotations

from functools import lru_cache
import os

from dotenv import load_dotenv

load_dotenv()


@lru_cache
def get_settings():
    return {
        "app_name": "Boracay Resort Management",
        "jwt_secret": os.getenv("JWT_SECRET_KEY", "dev-secret-change-me"),
        "jwt_algorithm": os.getenv("JWT_ALGORITHM", "HS256"),
        "token_ttl_minutes": int(os.getenv("JWT_TTL_MINUTES", "480")),
        "demo_user": os.getenv("DEMO_USERNAME", "resortadmin"),
        "demo_password": os.getenv("DEMO_PASSWORD", "ChangeMe123!"),
    }
