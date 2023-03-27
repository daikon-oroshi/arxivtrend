from typing import List
from datetime import date
from pydantic import BaseModel
from .arxiv_query import ArxivQueryEntity


class ArxivSummaryEntity(BaseModel):
    entry_id: str
    updated: date
    published: date
    title: str
    authors: List[str]
    summary: str
    categories: List[str]


class ArxivResultEntity(BaseModel):
    query: ArxivQueryEntity
    results: List[ArxivSummaryEntity]
