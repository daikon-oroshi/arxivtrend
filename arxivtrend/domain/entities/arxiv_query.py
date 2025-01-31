from typing import Optional, Dict
from datetime import date
from pydantic import BaseModel, field_validator


# 本当は value object
class ArxivQuery(BaseModel):
    search_q: str
    submitted_begin: Optional[date] = date(1991, 1, 1)
    submitted_end: Optional[date] = date.today()
    category: str

    @classmethod
    @field_validator("submitted_begin")
    def default_submitted_begin(cls, v: Optional[date]) -> date:
        if v is None:
            # Beginning of the year when the arxiv service was launched
            v = date(1991, 1, 1)
        return v

    @classmethod
    @field_validator("submitted_end")
    def span_is_valid(cls, v: Optional[date], values: Dict) -> date:
        # default value
        if v is None:
            v = date.today()
        if v < values["submitted_begin"]:
            raise ValueError(
                "submitted_begin must"
                + "be earlier than submitted_end."
            )
        return v
