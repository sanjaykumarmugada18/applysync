"""Manual application HTTP contracts, independent of open database sessions."""

from datetime import date, datetime
import re
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, StringConstraints, field_validator

ApplicationText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1, max_length=200)]


class ApplicationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    company: ApplicationText
    role: ApplicationText
    applied_on: date

    @field_validator("applied_on", mode="before")
    @classmethod
    def require_date_string(cls, value):
        # JSON dates are YYYY-MM-DD, not numeric timestamps or datetime strings.
        if not isinstance(value, str) or not re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value):
            raise ValueError("Use a date in YYYY-MM-DD format.")
        return value


class ApplicationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    company: str
    role: str
    applied_on: date
    created_at: datetime


class ApplicationPage(BaseModel):
    items: list[ApplicationRead]
    limit: int
    offset: int
