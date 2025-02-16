from typing import List
from datetime import date
from pydantic import BaseModel
from .arxiv_query import ArxivQuery
from .token import Token
import arxiv


class ArxivSummaryEntity(BaseModel):
    entry_id: str
    updated: date
    published: date
    title: str
    authors: List[str]
    summary: str
    categories: List[str]
    tokens: List[Token]

    @classmethod
    def from_arxiv_result(
        cls,
        result: arxiv.Result
    ) -> "ArxivSummaryEntity":
        return ArxivSummaryEntity(
            entry_id=result.entry_id,
            updated=result.updated.date(),
            published=result.published.date(),
            title=result.title,
            authors=[a.name for a in result.authors],
            summary=result.summary,
            categories=result.categories,
            tokens=[]
        )


class ArxivResultEntity(BaseModel):
    query: ArxivQuery
    results: List[ArxivSummaryEntity]
