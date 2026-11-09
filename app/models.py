from __future__ import annotations

from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6, max_length=128)


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    role: str


class ReservationCreate(BaseModel):
    guest_name: str = Field(..., min_length=2, max_length=80)
    property_id: str = Field(..., min_length=2, max_length=20)
    room_number: str = Field(..., min_length=1, max_length=20)
    check_in: date
    check_out: date
    partner: str = Field(default="Direct", min_length=2, max_length=50)
    status: str = Field(default="Confirmed")

    @field_validator("check_out")
    @classmethod
    def validate_check_out(cls, value: date, info):
        if "check_in" in info.data and value <= info.data["check_in"]:
            raise ValueError("check_out must be after check_in")
        return value


class ReservationUpdate(BaseModel):
    guest_name: Optional[str] = Field(default=None, min_length=2, max_length=80)
    property_id: Optional[str] = Field(default=None, min_length=2, max_length=20)
    room_number: Optional[str] = Field(default=None, min_length=1, max_length=20)
    check_in: Optional[date] = None
    check_out: Optional[date] = None
    partner: Optional[str] = Field(default=None, min_length=2, max_length=50)
    status: Optional[str] = None

    @field_validator("check_out")
    @classmethod
    def validate_check_out(cls, value: Optional[date], info):
        if value is None:
            return value
        if "check_in" in info.data and info.data["check_in"] is not None and value <= info.data["check_in"]:
            raise ValueError("check_out must be after check_in")
        return value
